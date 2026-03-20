#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correlation function utilities
"""

import numpy as np
from typing import List, Tuple, Dict, Optional


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


def generate_trigo_corr_functions(n_components: int) -> np.ndarray:
    """Generate trigonometric correlation functions."""
    table = CorrFuncTable(n_components)
    return table.table


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


def calc_correlation(atom_types: List[int], cluster: np.ndarray,
                     corr_func_table: np.ndarray) -> float:
    """
    Calculate the correlation function for a single cluster.
    
    Args:
        atom_types: List of atom types at each cluster site
        cluster: Cluster positions (not used directly, for reference)
        corr_func_table: Correlation function table
        
    Returns:
        Correlation value
    """
    if len(atom_types) == 0:
        return 0.0
    
    corr = 1.0
    for i, atype in enumerate(atom_types):
        func_idx = 0
        if func_idx < corr_func_table.shape[0] and atype < corr_func_table.shape[1]:
            corr *= corr_func_table[func_idx, atype]
    
    return corr


def calc_objective_function(corr: np.ndarray, target_corr: np.ndarray,
                            sqs_tol: float = 1e-3, weight_dist: float = 1.0,
                            weight_nbpt: float = 1.0, weight_decay: float = 0.0,
                            diameters: np.ndarray = None, 
                            nb_points: np.ndarray = None) -> float:
    """
    Calculate the objective function for SQS optimization.
    
    Lower values indicate better match to target correlations.
    """
    dcorr = np.abs(corr - target_corr)
    
    if diameters is None or nb_points is None:
        return np.sum(dcorr)
    
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
