#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crystal Structure and Cluster Data Structures
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any
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
    
    @property
    def n_atoms(self) -> int:
        return len(self.atom_pos)
    
    def get_fractional_positions(self) -> np.ndarray:
        """Get atom positions in fractional coordinates."""
        inv_cell = np.linalg.inv(self.cell)
        return np.dot(inv_cell, self.atom_pos.T).T
    
    def wrap_positions(self):
        """Wrap all atom positions into the unit cell."""
        inv_cell = np.linalg.inv(self.cell)
        frac_pos = np.dot(inv_cell, self.atom_pos.T).T
        frac_pos = frac_pos - np.floor(frac_pos)
        self.atom_pos = np.dot(self.cell, frac_pos.T).T


    def get_volume(self) -> float:
        """Get the volume of the unit cell."""
        return np.abs(np.linalg.det(self.cell))


@dataclass
class MultiCluster:
    """Represents a cluster with multiple sites and correlation function index."""
    clus: np.ndarray = field(default_factory=lambda: np.array([]).reshape(0, 3))
    func: np.ndarray = field(default_factory=lambda: np.array([], dtype=int))
    eci: float = 0.0
    
    @property
    def n_sites(self) -> int:
        return len(self.clus)
    
    def get_diameter(self) -> float:
        """Calculate the maximum distance between any two points in cluster."""
        if self.n_sites <= 1:
            return 0.0
        max_dist = 0.0
        for i in range(self.n_sites):
            for j in range(i + 1, self.n_sites):
                dist = np.linalg.norm(self.clus[i] - self.clus[j])
                max_dist = max(max_dist, dist)
        return max_dist


@dataclass
class SpaceGroup:
    """Represents the space group symmetry operations."""
    cell: np.ndarray = field(default_factory=lambda: np.eye(3))
    point_op: np.ndarray = field(default_factory=lambda: np.array([]).reshape(0, 3, 3))
    trans: np.ndarray = field(default_factory=lambda: np.array([]).reshape(0, 3))
    
    @property
    def n_operations(self) -> int:
        return len(self.point_op)


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


def calc_distance(pos1: np.ndarray, pos2: np.ndarray, cell: np.ndarray) -> float:
    """Calculate the minimum image distance between two positions."""
    inv_cell = np.linalg.inv(cell)
    frac1 = np.dot(inv_cell, pos1)
    frac2 = np.dot(inv_cell, pos2)
    diff = frac2 - frac1
    diff = diff - np.round(diff)
    return np.linalg.norm(np.dot(cell, diff))


def generate_supercell(base_cell: np.ndarray, supercell_matrix: np.ndarray) -> np.ndarray:
    """Generate a supercell from a base cell and transformation matrix."""
    return np.dot(base_cell, supercell_matrix)


def find_all_atoms_in_supercell(base_pos: np.ndarray, base_types: np.ndarray,
                                 base_cell: np.ndarray, supercell: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Find all atom positions in a supercell."""
    inv_base = np.linalg.inv(base_cell)
    inv_super = np.linalg.inv(supercell)
    
    smat = np.dot(inv_base, supercell)
    vol_factor = int(round(np.abs(np.linalg.det(smat))))
    
    size = int(round(vol_factor ** (1/3)))
    if size < 1:
        size = 1
    
    new_pos = []
    new_types = []
    
    for i in range(size):
        for j in range(size):
            for k in range(size):
                offset = np.array([i, j, k])
                for pos, atype in zip(base_pos, base_types):
                    frac_pos = np.dot(inv_base, pos) + offset / size
                    new_pos.append(np.dot(supercell, frac_pos))
                    new_types.append(atype)
    
    return np.array(new_pos), np.array(new_types)


def equivalent_by_symmetry(structure1: Structure, structure2: Structure,
                           spacegroup: SpaceGroup, tol: float = 1e-4) -> bool:
    """Check if two structures are equivalent by symmetry."""
    if structure1.n_atoms != structure2.n_atoms:
        return False
    
    for op, trans in zip(spacegroup.point_op, spacegroup.trans):
        transformed_pos = np.array([np.dot(op, pos) + trans for pos in structure1.atom_pos])
        transformed_pos = np.array([wrap_position(pos, structure2.cell) for pos in transformed_pos])
        
        matched = [False] * len(transformed_pos)
        for i, pos1 in enumerate(transformed_pos):
            for j, pos2 in enumerate(structure2.atom_pos):
                if not matched[j] and np.allclose(pos1, pos2, atol=tol):
                    if structure1.atom_type[i] == structure2.atom_type[j]:
                        matched[i] = True
                        break
        
        if all(matched):
            return True
    
    return False
