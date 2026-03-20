#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lattice creation and manipulation utilities
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from itertools import product


def create_fcc_lattice(a: float = 4.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Create an FCC lattice with lattice parameter a.
    
    Args:
        a: Lattice parameter in Angstrom
        
    Returns:
        Tuple of (cell, atom_positions, atom_types)
    """
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
    """
    Create a BCC lattice with lattice parameter a.
    
    Args:
        a: Lattice parameter in Angstrom
        
    Returns:
        Tuple of (cell, atom_positions, atom_types)
    """
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


def create_hcp_lattice(a: float = 2.5, c: float = 4.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Create an HCP lattice with lattice parameters a and c.
    
    Args:
        a: Basal plane lattice parameter
        c: Height lattice parameter
        
    Returns:
        Tuple of (cell, atom_positions, atom_types)
    """
    cell = np.array([
        [a, 0.0, 0.0],
        [a/2, a * np.sqrt(3)/2, 0.0],
        [0.0, 0.0, c]
    ])
    
    atom_pos = np.array([
        [0.0, 0.0, 0.0],
        [a/2, a / (2 * np.sqrt(3)), c/2]
    ])
    
    atom_type = np.array([0, 0])
    
    return cell, atom_pos, atom_type


def generate_pair_clusters(cell: np.ndarray, atom_pos: np.ndarray,
                           max_distance: float) -> List[np.ndarray]:
    """
    Generate all pair clusters up to a maximum distance.
    
    Args:
        cell: Unit cell vectors
        atom_pos: Atom positions
        max_distance: Maximum distance for pairs
        
    Returns:
        List of pair clusters
    """
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


def generate_triplet_clusters(cell: np.ndarray, atom_pos: np.ndarray,
                              max_distance: float) -> List[np.ndarray]:
    """
    Generate all triplet clusters up to a maximum distance.
    
    Args:
        cell: Unit cell vectors
        atom_pos: Atom positions
        max_distance: Maximum distance for pairs
        
    Returns:
        List of triplet clusters
    """
    clusters = []
    n_atoms = len(atom_pos)
    inv_cell = np.linalg.inv(cell)
    
    frac_pos = np.dot(inv_cell, atom_pos.T).T
    
    max_images = int(np.ceil(max_distance / np.min(np.linalg.norm(cell, axis=0)))) + 1
    
    pair_list = []
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
                            pair_list.append((i, pos_j_image, dist))
    
    for i, pos_j, dist_ij in pair_list:
        for k, pos_k, dist_ik in pair_list:
            if i != k:
                dist_jk = np.linalg.norm(pos_j - pos_k)
                if dist_jk <= max_distance:
                    cluster = np.array([atom_pos[i], pos_j, pos_k])
                    max_d = max(dist_ij, dist_ik, dist_jk)
                    clusters.append((max_d, cluster))
    
    clusters.sort(key=lambda x: x[0])
    
    unique_clusters = []
    seen = set()
    for max_d, cluster in clusters:
        sorted_cluster = cluster[np.lexsort((cluster[:, 2], cluster[:, 1], cluster[:, 0]))]
        key = tuple(sorted_cluster.flatten().round(4))
        if key not in seen:
            seen.add(key)
            unique_clusters.append(cluster)
    
    return unique_clusters[:20]


def find_supercells(base_cell: np.ndarray, target_volume: int) -> List[np.ndarray]:
    """
    Find all unique supercells up to a given volume.
    
    Args:
        base_cell: Base unit cell
        target_volume: Target volume multiplier
        
    Returns:
        List of supercell matrices
    """
    supercells = []
    
    for a in range(1, target_volume + 1):
        for b in range(1, target_volume + 1):
            for c in range(1, target_volume + 1):
                if a * b * c != target_volume:
                    continue
                
                smat = np.array([
                    [a, 0, 0],
                    [0, b, 0],
                    [0, 0, c]
                ], dtype=float)
                
                supercell = np.dot(base_cell, smat)
                supercells.append(supercell)
    
    return supercells
