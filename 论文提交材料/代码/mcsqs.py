#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcsqs - Monte Carlo Special Quasirandom Structure Generator
Python implementation based on ATAT by Axel van de Walle

This module generates Special Quasirandom Structures (SQS) that mimic
the local correlation functions of a perfectly random solid solution.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any
import random
import math


@dataclass
class Structure:
    """Represents a crystal structure with cell vectors and atom positions."""
    cell: np.ndarray = field(default_factory=lambda: np.eye(3))
    atom_pos: np.ndarray = field(default_factory=lambda: np.array([]).reshape(0, 3))
    atom_type: np.ndarray = field(default_factory=lambda: np.array([], dtype=int))
    
    def copy(self) -> 'Structure':
        return Structure(
            cell=self.cell.copy(),
            atom_pos=self.atom_pos.copy(),
            atom_type=self.atom_type.copy()
        )


@dataclass
class MultiCluster:
    """Represents a cluster with multiple sites and correlation function index."""
    clus: np.ndarray = field(default_factory=lambda: np.array([]).reshape(0, 3))
    func: np.ndarray = field(default_factory=lambda: np.array([], dtype=int))
    eci: float = 0.0


def generate_trigo_corr_functions(n_components: int) -> np.ndarray:
    """
    Generate trigonometric correlation functions.
    
    For a binary system: Pi_0 = [1, -1] (point correlation)
    For a ternary system: Pi_0 = [1, -0.5, -0.5], Pi_1 = [0, sqrt(3)/2, -sqrt(3)/2]
    """
    if n_components < 2:
        return np.array([[1.0]])
    
    n_func = n_components - 1
    corr_func = np.zeros((n_func, n_components))
    
    if n_components == 2:
        corr_func[0, 0] = 1.0
        corr_func[0, 1] = -1.0
    else:
        for k in range(n_func):
            for sigma in range(n_components):
                corr_func[k, sigma] = np.cos(2 * np.pi * (k + 1) * sigma / n_components)
    
    return corr_func


def calc_cluster_diameter(cluster: np.ndarray) -> float:
    """Calculate the maximum distance between any two points in a cluster."""
    if len(cluster) <= 1:
        return 0.0
    
    max_dist = 0.0
    for i in range(len(cluster)):
        for j in range(i + 1, len(cluster)):
            dist = np.linalg.norm(cluster[i] - cluster[j])
            max_dist = max(max_dist, dist)
    return max_dist


def calc_objective_function(corr: np.ndarray, target_corr: np.ndarray,
                            sqs_tol: float, weight_dist: float,
                            weight_nbpt: float, weight_decay: float,
                            diameters: np.ndarray, nb_points: np.ndarray) -> float:
    """
    Calculate the objective function for SQS optimization.
    """
    dcorr = np.abs(corr - target_corr)
    
    max_nbpt = int(np.max(nb_points)) if len(nb_points) > 0 else 2
    maxdist = np.zeros(max_nbpt - 1)
    
    for t in range(len(corr)):
        if nb_points[t] >= 2:
            idx = int(nb_points[t]) - 2
            if idx < len(maxdist):
                maxdist[idx] = max(maxdist[idx], diameters[t])
    
    d0 = np.min(diameters) if len(diameters) > 0 else 1.0
    maxdist = maxdist + d0
    
    for t in range(len(corr)):
        if dcorr[t] > sqs_tol:
            idx = int(nb_points[t]) - 2
            if 0 <= idx < len(maxdist):
                maxdist[idx] = min(diameters[t], maxdist[idx])
    
    for p in range(1, len(maxdist)):
        maxdist[p] = min(maxdist[p], maxdist[p-1])
    
    d1 = np.min(maxdist) if len(maxdist) > 0 else d0
    
    obj_dev = 0.0
    den = 0.0
    
    for t in range(len(corr)):
        if diameters[t] >= d1 - 1e-10:
            w = np.exp(-weight_decay * diameters[t] / d0) * (weight_nbpt ** (nb_points[t] - 2))
            obj_dev += dcorr[t] * w
            den += w
    
    if den < 1e-10 or obj_dev < 1e-10:
        return -np.inf
    
    obj_dev /= den
    
    obj = obj_dev
    for p in range(len(maxdist)):
        obj -= weight_dist * (weight_nbpt ** p) * maxdist[p] / d0
    
    return obj


class MCSQS:
    """
    Monte Carlo Special Quasirandom Structure Generator.
    
    This class implements the mcsqs algorithm to generate structures
    that best match the correlation functions of a random alloy.
    """
    
    def __init__(self, seed: int = None):
        """Initialize the SQS generator."""
        self.rng = random.Random(seed)
        self.np_rng = np.random.default_rng(seed)
        
        self.lattice = Structure()
        self.clusters: List[MultiCluster] = []
        self.target_corr: np.ndarray = None
        self.corr_func_table: np.ndarray = None
        
        self.sqs_tol = 1e-3
        self.weight_dist = 1.0
        self.weight_nbpt = 1.0
        self.weight_decay = 0.0
        self.temperature = 1.0
        
        self.diameters: np.ndarray = None
        self.nb_points: np.ndarray = None
        
        self.site_type_list: List[List[int]] = []
        self.sym_type_prob: List[np.ndarray] = []
        self.sym_to_type: List[int] = []
        
        self.best_structure: Structure = None
        self.best_corr: np.ndarray = None
        self.best_obj: float = np.inf
        
        self.n_iterations = 50000
        self.log_interval = 10000
        
        self._atom_pos_frac: np.ndarray = None
        self._inv_cell: np.ndarray = None
        self._neighbor_table: Dict = None
    
    def set_lattice(self, cell: np.ndarray, atom_pos: np.ndarray,
                    atom_type: np.ndarray, atom_prob: List[np.ndarray],
                    site_type_list: List[List[int]]):
        """Set the base lattice structure."""
        self.lattice.cell = np.array(cell, dtype=float)
        self.lattice.atom_pos = np.array(atom_pos, dtype=float)
        self.lattice.atom_type = np.array(atom_type, dtype=int)
        self.site_type_list = site_type_list
        self.sym_type_prob = [np.array(p, dtype=float) for p in atom_prob]
        
        self.sym_to_type = list(range(len(atom_type)))
        
        max_comp = max(len(st) for st in site_type_list) if site_type_list else 2
        self.corr_func_table = generate_trigo_corr_functions(max_comp)
        
        self._inv_cell = np.linalg.inv(self.lattice.cell)
        self._atom_pos_frac = np.dot(self._inv_cell, self.lattice.atom_pos.T).T
    
    def add_cluster(self, cluster: np.ndarray, func_indices: np.ndarray = None):
        """Add a cluster for correlation calculation."""
        if func_indices is None:
            func_indices = np.zeros(len(cluster), dtype=int)
        
        mcluster = MultiCluster(
            clus=np.array(cluster, dtype=float),
            func=np.array(func_indices, dtype=int)
        )
        self.clusters.append(mcluster)
    
    def _calculate_cluster_properties(self):
        """Calculate diameters and point counts for all clusters."""
        n = len(self.clusters)
        self.diameters = np.zeros(n)
        self.nb_points = np.zeros(n, dtype=int)
        
        for i, mcluster in enumerate(self.clusters):
            self.diameters[i] = calc_cluster_diameter(mcluster.clus)
            self.nb_points[i] = len(mcluster.clus)
    
    def set_target_correlations(self, target_corr: np.ndarray = None):
        """Set target correlations. If None, calculate for random alloy."""
        if target_corr is not None:
            self.target_corr = np.array(target_corr)
        else:
            self.target_corr = np.zeros(len(self.clusters))
    
    def generate_supercell(self, n_atoms: int) -> Structure:
        """Generate a supercell with approximately n_atoms."""
        n_base = len(self.lattice.atom_pos)
        vol_factor = max(1, n_atoms // n_base)
        
        size = int(round(vol_factor ** (1/3)))
        if size < 1:
            size = 1
        
        smat = np.eye(3) * size
        supercell = np.dot(self.lattice.cell, smat)
        
        new_pos = []
        new_types = []
        
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    offset = np.array([i, j, k])
                    for pos, atype in zip(self.lattice.atom_pos, self.lattice.atom_type):
                        frac_pos = np.dot(self._inv_cell, pos) + offset
                        new_pos.append(np.dot(supercell, frac_pos / size))
                        new_types.append(atype)
        
        structure = Structure(
            cell=supercell,
            atom_pos=np.array(new_pos),
            atom_type=np.array(new_types)
        )
        
        return structure
    
    def _build_neighbor_table(self, structure: Structure, max_dist: float):
        """Build a neighbor lookup table for fast atom finding."""
        self._neighbor_table = {}
        inv_cell = np.linalg.inv(structure.cell)
        
        frac_pos = np.dot(inv_cell, structure.atom_pos.T).T
        
        for i, fp in enumerate(frac_pos):
            key = tuple(np.round(fp, 4))
            self._neighbor_table[key] = i
    
    def _find_atom_fast(self, frac_pos: np.ndarray, tol: float = 1e-4) -> int:
        """Fast atom finding using hash table."""
        wrapped = frac_pos - np.floor(frac_pos)
        key = tuple(np.round(wrapped, 4))
        return self._neighbor_table.get(key, -1)
    
    def calculate_correlations(self, structure: Structure) -> np.ndarray:
        """Calculate all correlation functions for a structure."""
        n_clusters = len(self.clusters)
        correlations = np.zeros(n_clusters)
        
        inv_cell = np.linalg.inv(structure.cell)
        frac_pos = np.dot(inv_cell, structure.atom_pos.T).T
        
        pos_hash = {}
        for i, fp in enumerate(frac_pos):
            wrapped = fp - np.floor(fp)
            key = tuple(np.round(wrapped, 5))
            pos_hash[key] = i
        
        for t, mcluster in enumerate(self.clusters):
            if len(mcluster.clus) == 0:
                continue
            
            if len(mcluster.clus) == 1:
                total_corr = 0.0
                for i in range(len(structure.atom_pos)):
                    atom_type = structure.atom_type[i]
                    func_idx = mcluster.func[0] if len(mcluster.func) > 0 else 0
                    if func_idx < self.corr_func_table.shape[0] and atom_type < self.corr_func_table.shape[1]:
                        total_corr += self.corr_func_table[func_idx, atom_type]
                correlations[t] = total_corr / len(structure.atom_pos) if len(structure.atom_pos) > 0 else 0.0
                continue
            
            total_corr = 0.0
            count = 0
            
            n_sites = len(mcluster.clus)
            base_pos = mcluster.clus[0]
            offsets = np.zeros((n_sites, 3))
            for i in range(1, n_sites):
                offsets[i] = mcluster.clus[i] - base_pos
            
            frac_offsets = np.dot(inv_cell, offsets.T).T
            
            for base_idx in range(len(structure.atom_pos)):
                base_frac = frac_pos[base_idx]
                
                cluster_corr = 1.0
                valid = True
                atom_indices = [base_idx]
                
                for i in range(1, n_sites):
                    target_frac = base_frac + frac_offsets[i]
                    wrapped = target_frac - np.floor(target_frac)
                    key = tuple(np.round(wrapped, 5))
                    
                    if key in pos_hash:
                        atom_indices.append(pos_hash[key])
                    else:
                        valid = False
                        break
                
                if valid:
                    for i, atom_idx in enumerate(atom_indices):
                        atom_type = structure.atom_type[atom_idx]
                        func_idx = mcluster.func[i] if i < len(mcluster.func) else 0
                        
                        if func_idx < self.corr_func_table.shape[0]:
                            n_comp = self.corr_func_table.shape[1]
                            if atom_type < n_comp:
                                cluster_corr *= self.corr_func_table[func_idx, atom_type]
                    
                    total_corr += cluster_corr
                    count += 1
            
            correlations[t] = total_corr / count if count > 0 else 0.0
        
        return correlations
    
    def run(self, n_atoms: int = 16, verbose: bool = True) -> Structure:
        """
        Run the SQS optimization.
        """
        structure = self.generate_supercell(n_atoms)
        n_atoms_actual = len(structure.atom_pos)
        
        atom_types = structure.atom_type.copy()
        
        type_groups = {}
        for i, t in enumerate(atom_types):
            if t not in type_groups:
                type_groups[t] = []
            type_groups[t].append(i)
        
        for t in type_groups:
            self.rng.shuffle(type_groups[t])
        
        for t, indices in type_groups.items():
            if t < len(self.sym_type_prob):
                prob = self.sym_type_prob[t]
                n_comp = len(prob)
                n_atoms_type = len(indices)
                
                counts = [int(round(n_atoms_type * p)) for p in prob]
                diff = n_atoms_type - sum(counts)
                if diff != 0:
                    counts[0] += diff
                
                type_assignments = []
                for comp, count in enumerate(counts):
                    type_assignments.extend([comp] * count)
                self.rng.shuffle(type_assignments)
                
                for i, idx in enumerate(indices):
                    if i < len(type_assignments):
                        atom_types[idx] = type_assignments[i]
        
        structure.atom_type = atom_types.copy()
        
        corr = self.calculate_correlations(structure)
        obj = calc_objective_function(
            corr, self.target_corr, self.sqs_tol,
            self.weight_dist, self.weight_nbpt, self.weight_decay,
            self.diameters, self.nb_points
        )
        
        self.best_structure = structure.copy()
        self.best_corr = corr.copy()
        self.best_obj = obj
        
        if verbose:
            print(f"Initial objective: {obj:.6f}")
            print(f"Number of atoms: {n_atoms_actual}")
        
        type_beg = np.zeros(n_atoms_actual, dtype=int)
        type_end = np.zeros(n_atoms_actual, dtype=int)
        
        for i in range(n_atoms_actual):
            for t, indices in type_groups.items():
                if i in indices:
                    type_beg[i] = min(indices)
                    type_end[i] = max(indices) + 1
                    break
        
        for iteration in range(self.n_iterations):
            at1 = self.rng.randint(0, n_atoms_actual - 1)
            nbat = type_end[at1] - type_beg[at1]
            
            if nbat <= 1:
                continue
            
            at2 = type_beg[at1] + self.rng.randint(0, nbat - 1)
            while at2 == at1:
                at2 = type_beg[at1] + self.rng.randint(0, nbat - 1)
            
            if structure.atom_type[at1] == structure.atom_type[at2]:
                continue
            
            structure.atom_type[at1], structure.atom_type[at2] = \
                structure.atom_type[at2], structure.atom_type[at1]
            
            new_corr = self.calculate_correlations(structure)
            new_obj = calc_objective_function(
                new_corr, self.target_corr, self.sqs_tol,
                self.weight_dist, self.weight_nbpt, self.weight_decay,
                self.diameters, self.nb_points
            )
            
            delta_obj = new_obj - obj
            
            if delta_obj < 0 or self.rng.random() < np.exp(-delta_obj / self.temperature):
                corr = new_corr
                obj = new_obj
                
                if obj < self.best_obj:
                    self.best_structure = structure.copy()
                    self.best_corr = corr.copy()
                    self.best_obj = obj
                    
                    if verbose and (iteration + 1) % self.log_interval == 0:
                        print(f"Iteration {iteration + 1}: objective = {obj:.6f}")
            else:
                structure.atom_type[at1], structure.atom_type[at2] = \
                    structure.atom_type[at2], structure.atom_type[at1]
        
        if verbose:
            print(f"\nFinal objective: {self.best_obj:.6f}")
        
        return self.best_structure
    
    def get_results(self) -> Dict[str, Any]:
        """Get the results of the SQS optimization."""
        return {
            'structure': self.best_structure,
            'correlations': self.best_corr,
            'target_correlations': self.target_corr,
            'objective': self.best_obj,
            'mismatches': self.best_corr - self.target_corr if self.best_corr is not None else None
        }


def create_fcc_lattice(a: float = 4.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create an FCC lattice with lattice parameter a."""
    cell = np.array([
        [0.0, a/2, a/2],
        [a/2, 0.0, a/2],
        [a/2, a/2, 0.0]
    ])
    
    atom_pos = np.array([
        [0.0, 0.0, 0.0]
    ])
    
    atom_type = np.array([0])
    
    return cell, atom_pos, atom_type


def create_bcc_lattice(a: float = 2.87) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create a BCC lattice with lattice parameter a."""
    cell = np.array([
        [a, 0.0, 0.0],
        [0.0, a, 0.0],
        [0.0, 0.0, a]
    ])
    
    atom_pos = np.array([
        [0.0, 0.0, 0.0],
        [a/2, a/2, a/2]
    ])
    
    atom_type = np.array([0, 0])
    
    return cell, atom_pos, atom_type


def generate_pair_clusters(cell: np.ndarray, atom_pos: np.ndarray,
                           max_distance: float) -> List[np.ndarray]:
    """Generate all pair clusters up to a maximum distance."""
    clusters = []
    n_atoms = len(atom_pos)
    inv_cell = np.linalg.inv(cell)
    
    frac_pos = np.dot(inv_cell, atom_pos.T).T
    
    max_images = int(np.ceil(max_distance / np.min(np.linalg.norm(cell, axis=0)))) + 1
    
    for i in range(n_atoms):
        for j in range(n_atoms):
            for dx in range(-max_images, max_images + 1):
                for dy in range(-max_images, max_images + 1):
                    for dz in range(-max_images, max_images + 1):
                        if i == j and dx == 0 and dy == 0 and dz == 0:
                            continue
                        
                        offset = np.array([dx, dy, dz])
                        frac_j = frac_pos[j] + offset
                        pos_j_image = np.dot(cell, frac_j)
                        dist = np.linalg.norm(pos_j_image - atom_pos[i])
                        
                        if dist <= max_distance and dist > 0.1:
                            cluster = np.array([
                                atom_pos[i],
                                pos_j_image
                            ])
                            clusters.append((dist, cluster))
    
    clusters.sort(key=lambda x: x[0])
    
    unique_clusters = []
    seen_dists = set()
    for dist, cluster in clusters:
        dist_key = round(dist, 4)
        if dist_key not in seen_dists:
            seen_dists.add(dist_key)
            unique_clusters.append(cluster)
    
    return unique_clusters


def demo_binary_alloy():
    """
    Demonstration: Generate SQS for a binary alloy (e.g., Cu-Au).
    """
    print("=" * 60)
    print("SQS Generation Demo: Binary FCC Alloy (Cu-Au type)")
    print("=" * 60)
    
    a = 4.0
    cell, atom_pos, atom_type = create_fcc_lattice(a)
    
    print(f"\nFCC lattice parameter: {a} Angstrom")
    print(f"Cell vectors:\n{cell}")
    
    sqs = MCSQS(seed=42)
    
    composition = np.array([0.5, 0.5])
    atom_prob = [composition]
    
    site_type_list = [[0, 1]]
    
    sqs.set_lattice(cell, atom_pos, atom_type, atom_prob, site_type_list)
    
    max_pair_dist = a * 1.5
    pair_clusters = generate_pair_clusters(cell, atom_pos, max_pair_dist)
    
    print(f"\nGenerated {len(pair_clusters)} unique pair clusters up to {max_pair_dist:.2f} Angstrom")
    
    for cluster in pair_clusters[:6]:
        sqs.add_cluster(cluster)
    
    sqs._calculate_cluster_properties()
    
    sqs.set_target_correlations()
    
    print(f"\nNumber of clusters: {len(sqs.clusters)}")
    print(f"Target correlations: all zeros (random alloy)")
    
    print("\n" + "-" * 60)
    print("Running Monte Carlo SQS optimization...")
    print("-" * 60)
    
    best_structure = sqs.run(n_atoms=16, verbose=True)
    
    results = sqs.get_results()
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\nBest objective function: {results['objective']:.6f}")
    print(f"\nNumber of atoms in SQS: {len(best_structure.atom_pos)}")
    
    print("\nCorrelation function comparison:")
    print(f"{'Cluster':<10} {'Calculated':<15} {'Target':<15} {'Mismatch':<15}")
    print("-" * 55)
    for i, (c, tc) in enumerate(zip(results['correlations'], results['target_correlations'])):
        print(f"{i:<10} {c:<15.6f} {tc:<15.6f} {c-tc:<15.6f}")
    
    atom_counts = {}
    for at in best_structure.atom_type:
        atom_counts[at] = atom_counts.get(at, 0) + 1
    print(f"\nAtom type distribution: {atom_counts}")
    
    return results


def demo_ternary_alloy():
    """
    Demonstration: Generate SQS for a ternary alloy.
    """
    print("\n" + "=" * 60)
    print("SQS Generation Demo: Ternary FCC Alloy")
    print("=" * 60)
    
    a = 4.0
    cell, atom_pos, atom_type = create_fcc_lattice(a)
    
    sqs = MCSQS(seed=123)
    
    composition = np.array([1/3, 1/3, 1/3])
    atom_prob = [composition]
    
    site_type_list = [[0, 1, 2]]
    
    sqs.set_lattice(cell, atom_pos, atom_type, atom_prob, site_type_list)
    
    max_pair_dist = a * 1.2
    pair_clusters = generate_pair_clusters(cell, atom_pos, max_pair_dist)
    
    for cluster in pair_clusters[:5]:
        sqs.add_cluster(cluster)
    
    sqs._calculate_cluster_properties()
    
    sqs.set_target_correlations()
    
    print(f"\nNumber of clusters: {len(sqs.clusters)}")
    print(f"Composition: 1/3 each of three species")
    
    print("\n" + "-" * 60)
    print("Running Monte Carlo SQS optimization...")
    print("-" * 60)
    
    best_structure = sqs.run(n_atoms=27, verbose=True)
    
    results = sqs.get_results()
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\nBest objective function: {results['objective']:.6f}")
    print(f"\nNumber of atoms in SQS: {len(best_structure.atom_pos)}")
    
    atom_counts = {}
    for at in best_structure.atom_type:
        atom_counts[at] = atom_counts.get(at, 0) + 1
    print(f"Atom type distribution: {atom_counts}")
    
    return results


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("#  MCSQS - Special Quasirandom Structure Generator")
    print("#  Python Implementation")
    print("#" * 60)
    
    results_binary = demo_binary_alloy()
    
    results_ternary = demo_ternary_alloy()
    
    print("\n" + "=" * 60)
    print("All demonstrations completed successfully!")
    print("=" * 60)
