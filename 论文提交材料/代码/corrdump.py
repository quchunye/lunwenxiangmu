#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corrdump - Correlation Function Calculator
Python implementation based on ATAT by Axel van de Walle

This module calculates correlation functions for crystal structures,
essential for cluster expansion methods in alloy theory.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any
import re
from collections import defaultdict


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
    multiplicity: int = 1


class CorrFuncTable:
    """
    Correlation function table for different component systems.
    
    Uses trigonometric basis functions:
    - Binary: Pi_0 = [1, -1]
    - Ternary: Pi_0 = [1, -0.5, -0.5], Pi_1 = [1, -0.5, -0.5]
    """
    
    def __init__(self, n_components: int = 2):
        self.n_components = n_components
        self.table = self._generate_table()
    
    def _generate_table(self) -> np.ndarray:
        if self.n_components < 2:
            return np.array([[1.0]])
        
        n_func = self.n_components - 1
        table = np.zeros((n_func, self.n_components))
        
        if self.n_components == 2:
            table[0, 0] = 1.0
            table[0, 1] = -1.0
        else:
            for k in range(n_func):
                for sigma in range(self.n_components):
                    table[k, sigma] = np.cos(2 * np.pi * (k + 1) * sigma / self.n_components)
        
        return table
    
    def __call__(self, func_idx: int, species: int) -> float:
        if func_idx < 0 or func_idx >= self.table.shape[0]:
            return 1.0
        if species < 0 or species >= self.table.shape[1]:
            return 1.0
        return self.table[func_idx, species]
    
    def __getitem__(self, key: Tuple[int, int]) -> float:
        return self.__call__(*key)


def wrap_position(pos: np.ndarray, cell: np.ndarray) -> np.ndarray:
    """Wrap a position into the unit cell."""
    inv_cell = np.linalg.inv(cell)
    frac = np.dot(inv_cell, pos)
    frac = frac - np.floor(frac)
    return np.dot(cell, frac)


def find_atom_index(pos: np.ndarray, atom_positions: np.ndarray, 
                    cell: np.ndarray, tol: float = 1e-6) -> int:
    """Find the index of an atom at a given position."""
    if len(atom_positions) == 0:
        return -1
    inv_cell = np.linalg.inv(cell)
    frac_pos = np.dot(inv_cell, pos)
    
    for i, atom_pos in enumerate(atom_positions):
        frac_atom = np.dot(inv_cell, atom_pos)
        diff = frac_pos - frac_atom
        diff = diff - np.round(diff)
        if np.all(np.abs(diff) < tol):
            return i
    return -1


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


def generate_trigo_corr_functions(n_components: int) -> np.ndarray:
    """Generate trigonometric correlation functions."""
    table = CorrFuncTable(n_components)
    return table.table


class SpaceGroup:
    """Represents the space group symmetry operations."""
    
    def __init__(self):
        self.point_ops: List[np.ndarray] = [np.eye(3)]
        self.translations: List[np.ndarray] = [np.zeros(3)]
        self.cell: np.ndarray = np.eye(3)
    
    def add_operation(self, op: np.ndarray, trans: np.ndarray):
        self.point_ops.append(op)
        self.translations.append(trans)


def find_spacegroup(cell: np.ndarray, atom_pos: np.ndarray, 
                    atom_type: np.ndarray, tol: float = 1e-3) -> SpaceGroup:
    """
    Find the space group of a structure.
    Returns symmetry operations.
    """
    sg = SpaceGroup()
    sg.cell = cell
    
    identity = np.eye(3)
    sg.point_ops = [identity]
    sg.translations = [np.zeros(3)]
    
    inv_cell = np.linalg.inv(cell)
    frac_pos = np.dot(inv_cell, atom_pos.T).T
    
    n_atoms = len(atom_pos)
    
    for i in range(24):
        angle = i * 15 * np.pi / 180
        
        for axis_idx in range(3):
            axis = np.zeros(3)
            axis[axis_idx] = 1
            
            c, s = np.cos(angle), np.sin(angle)
            K = np.array([
                [0, -axis[2], axis[1]],
                [axis[2], 0, -axis[0]],
                [-axis[1], axis[0], 0]
            ])
            rot = np.eye(3) + s * K + (1 - c) * np.dot(K, K)
            
            if not np.allclose(rot, identity, atol=tol):
                is_symmetry = True
                for j, (pos, atype) in enumerate(zip(frac_pos, atom_type)):
                    new_pos = np.dot(rot, pos)
                    new_pos = new_pos - np.floor(new_pos)
                    
                    found = False
                    for k, (pos2, atype2) in enumerate(zip(frac_pos, atom_type)):
                        if atype == atype2:
                            diff = new_pos - pos2
                            diff = diff - np.round(diff)
                            if np.all(np.abs(diff) < tol):
                                found = True
                                break
                    
                    if not found:
                        is_symmetry = False
                        break
                
                if is_symmetry:
                    sg.point_ops.append(rot)
                    sg.translations.append(np.zeros(3))
    
    return sg


def find_equivalent_clusters(cluster: np.ndarray, cell: np.ndarray,
                             point_ops: List[np.ndarray], 
                             translations: List[np.ndarray]) -> List[np.ndarray]:
    """Find all symmetry-equivalent clusters."""
    equiv_clusters = []
    
    for op, trans in zip(point_ops, translations):
        new_cluster = np.array([np.dot(op, pos) + trans for pos in cluster])
        wrapped_cluster = np.array([wrap_position(pos, cell) for pos in new_cluster])
        
        sorted_indices = np.lexsort((wrapped_cluster[:, 2], 
                                     wrapped_cluster[:, 1], 
                                     wrapped_cluster[:, 0]))
        sorted_cluster = wrapped_cluster[sorted_indices]
        
        is_new = True
        for existing in equiv_clusters:
            if np.allclose(sorted_cluster, existing, atol=1e-6):
                is_new = False
                break
        
        if is_new:
            equiv_clusters.append(sorted_cluster)
    
    return equiv_clusters


def calc_multiplicity(cluster: np.ndarray, cell: np.ndarray,
                      point_ops: List[np.ndarray], 
                      translations: List[np.ndarray]) -> int:
    """Calculate the multiplicity of a cluster."""
    equiv = find_equivalent_clusters(cluster, cell, point_ops, translations)
    return len(equiv)


class CorrDump:
    """
    Correlation Function Calculator.
    
    This class calculates correlation functions for crystal structures,
    which are essential for cluster expansion methods.
    """
    
    def __init__(self, n_components: int = 2):
        self.corr_func_table = CorrFuncTable(n_components)
        self.lattice: Optional[Structure] = None
        self.space_group: Optional[SpaceGroup] = None
        self.clusters: List[MultiCluster] = []
        self.zero_tolerance = 1e-3
        self._inv_cell: Optional[np.ndarray] = None
        self._frac_pos: Optional[np.ndarray] = None
    
    def set_lattice(self, cell: np.ndarray, atom_pos: np.ndarray, 
                    atom_type: np.ndarray):
        """Set the lattice structure."""
        self.lattice = Structure(
            cell=np.array(cell, dtype=float),
            atom_pos=np.array(atom_pos, dtype=float),
            atom_type=np.array(atom_type, dtype=int)
        )
        self._inv_cell = np.linalg.inv(self.lattice.cell)
        self._frac_pos = np.dot(self._inv_cell, self.lattice.atom_pos.T).T
        
        self.space_group = find_spacegroup(
            self.lattice.cell, 
            self.lattice.atom_pos, 
            self.lattice.atom_type
        )
    
    def generate_clusters(self, max_cluster_size: int = 4, 
                          max_distances: Dict[int, float] = None):
        """
        Generate clusters up to a given size and maximum distances.
        
        Args:
            max_cluster_size: Maximum number of atoms in a cluster
            max_distances: Dictionary mapping cluster size to max distance
        """
        if max_distances is None:
            max_distances = {2: 6.0, 3: 4.0, 4: 3.0}
        
        self.clusters = []
        
        for size in range(2, max_cluster_size + 1):
            max_dist = max_distances.get(size, 3.0)
            self._generate_clusters_of_size(size, max_dist)
    
    def _generate_clusters_of_size(self, size: int, max_distance: float):
        """Generate clusters of a specific size."""
        if self.lattice is None:
            return
        
        n_atoms = len(self.lattice.atom_pos)
        inv_cell = np.linalg.inv(self.lattice.cell)
        
        max_images = int(np.ceil(max_distance / np.min(np.linalg.norm(self.lattice.cell, axis=0)))) + 1
        
        all_pairs = []
        for i in range(n_atoms):
            for j in range(n_atoms):
                for dx in range(-max_images, max_images + 1):
                    for dy in range(-max_images, max_images + 1):
                        for dz in range(-max_images, max_images + 1):
                            if i == j and dx == 0 and dy == 0 and dz == 0:
                                continue
                            
                            offset = np.array([dx, dy, dz])
                            frac_j = self._frac_pos[j] + offset
                            pos_j_image = np.dot(self.lattice.cell, frac_j)
                            dist = np.linalg.norm(pos_j_image - self.lattice.atom_pos[i])
                            
                            if dist <= max_distance and dist > 0.1:
                                all_pairs.append((dist, i, j, offset))
        
        all_pairs.sort(key=lambda x: x[0])
        
        unique_pairs = []
        seen_dists = set()
        for dist, i, j, offset in all_pairs:
            dist_key = round(dist, 4)
            if dist_key not in seen_dists:
                seen_dists.add(dist_key)
                unique_pairs.append((dist, i, j, offset))
        
        for dist, i, j, offset in unique_pairs:
            frac_j = self._frac_pos[j] + offset
            pos_j_image = np.dot(self.lattice.cell, frac_j)
            
            cluster = MultiCluster(
                clus=np.array([self.lattice.atom_pos[i], pos_j_image]),
                func=np.array([0, 0], dtype=int),
                eci=0.0,
                multiplicity=1
            )
            cluster.diameter = dist
            self.clusters.append(cluster)
    
    def add_cluster(self, cluster: np.ndarray, func_indices: np.ndarray = None,
                    eci: float = 0.0):
        """Add a cluster manually."""
        if func_indices is None:
            func_indices = np.zeros(len(cluster), dtype=int)
        
        mcluster = MultiCluster(
            clus=np.array(cluster, dtype=float),
            func=np.array(func_indices, dtype=int),
            eci=eci,
            multiplicity=1
        )
        mcluster.diameter = calc_cluster_diameter(cluster)
        self.clusters.append(mcluster)
    
    def calculate_correlations(self, structure: Structure) -> np.ndarray:
        """
        Calculate all correlation functions for a structure.
        
        Args:
            structure: The structure to calculate correlations for
            
        Returns:
            Array of correlation function values
        """
        if len(self.clusters) == 0:
            return np.array([])
        
        correlations = np.zeros(len(self.clusters))
        
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
                    total_corr += self.corr_func_table(func_idx, atom_type)
                correlations[t] = total_corr / len(structure.atom_pos)
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
                        cluster_corr *= self.corr_func_table(func_idx, atom_type)
                    
                    total_corr += cluster_corr
                    count += 1
            
            correlations[t] = total_corr / count if count > 0 else 0.0
        
        return correlations
    
    def calculate_energy(self, structure: Structure, 
                        correlations: np.ndarray = None) -> float:
        """
        Calculate the energy of a structure using ECIs.
        
        E = sum(ECI_i * correlation_i)
        """
        if correlations is None:
            correlations = self.calculate_correlations(structure)
        
        energy = 0.0
        for i, mcluster in enumerate(self.clusters):
            energy += mcluster.eci * correlations[i]
        
        return energy
    
    def write_clusters(self, filename: str):
        """Write clusters to a file."""
        with open(filename, 'w') as f:
            for mcluster in self.clusters:
                f.write(f"{len(mcluster.clus)}\n")
                for i, pos in enumerate(mcluster.clus):
                    func_idx = mcluster.func[i] if i < len(mcluster.func) else 0
                    f.write(f"{pos[0]:.6f} {pos[1]:.6f} {pos[2]:.6f} {func_idx}\n")
                f.write(f"{mcluster.eci:.6f}\n")
    
    def read_clusters(self, filename: str):
        """Read clusters from a file."""
        self.clusters = []
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            try:
                n_sites = int(line)
                cluster = []
                func_indices = []
                
                for j in range(n_sites):
                    i += 1
                    if i >= len(lines):
                        break
                    parts = lines[i].strip().split()
                    if len(parts) >= 3:
                        pos = [float(x) for x in parts[:3]]
                        cluster.append(pos)
                        if len(parts) > 3:
                            func_indices.append(int(parts[3]))
                        else:
                            func_indices.append(0)
                
                i += 1
                eci = 0.0
                if i < len(lines):
                    try:
                        eci = float(lines[i].strip())
                    except ValueError:
                        pass
                
                if cluster:
                    self.add_cluster(np.array(cluster), np.array(func_indices, dtype=int), eci)
            except ValueError:
                pass
            i += 1


def demo_corrdump():
    """Demonstration of CorrDump functionality."""
    print("=" * 60)
    print("CorrDump Demo: Correlation Function Calculator")
    print("=" * 60)
    
    cell = np.array([
        [0.0, 2.0, 2.0],
        [2.0, 0.0, 2.0],
        [2.0, 2.0, 0.0]
    ])
    
    atom_pos = np.array([
        [0.0, 0.0, 0.0]
    ])
    atom_type = np.array([0])
    
    print(f"\nFCC lattice:")
    print(f"Cell vectors:\n{cell}")
    
    corrdump = CorrDump(n_components=2)
    corrdump.set_lattice(cell, atom_pos, atom_type)
    
    print(f"\nGenerating pair clusters...")
    corrdump.generate_clusters(max_cluster_size=2, max_distances={2: 6.0})
    
    print(f"Number of clusters generated: {len(corrdump.clusters)}")
    
    print("\nCluster diameters:")
    for i, mcluster in enumerate(corrdump.clusters[:5]):
        print(f"  Cluster {i}: diameter = {mcluster.diameter:.4f} Å")
    
    test_structure = Structure(
        cell=cell * 2,
        atom_pos=np.array([
            [0.0, 0.0, 0.0],
            [2.0, 2.0, 0.0],
            [2.0, 0.0, 2.0],
            [0.0, 2.0, 2.0],
        ]),
        atom_type=np.array([0, 1, 0, 1])
    )
    
    print(f"\nTest structure: 4 atoms, 50%-50% composition")
    
    correlations = corrdump.calculate_correlations(test_structure)
    
    print(f"\nCorrelation values:")
    for i, (corr, mcluster) in enumerate(zip(correlations[:5], corrdump.clusters[:5])):
        print(f"  Cluster {i} (d={mcluster.diameter:.3f}): {corr:.6f}")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    demo_corrdump()
