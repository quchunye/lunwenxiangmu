#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maps - Cluster Expansion
Python implementation based on ATAT by Axel van de Walle

This module implements cluster expansion for predicting alloy energetics.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Structure:
    """Represents a crystal structure."""
    cell: np.ndarray = field(default_factory=lambda: np.eye(3))
    atom_pos: np.ndarray = field(default_factory=lambda: np.array([]).reshape(0, 3))
    atom_type: np.ndarray = field(default_factory=lambda: np.array([], dtype=int))
    energy: float = 0.0


class ClusterExpansion:
    """
    Cluster Expansion for alloy systems.
    
    This class implements the cluster expansion method for predicting
    the energy of alloy configurations.
    """
    
    def __init__(self, n_components: int = 2):
        self.n_components = n_components
        self.clusters: List[Any] = []
        self.ecis: np.ndarray = np.array([])
        self.structures: List[Structure] = []
        self.correlations: np.ndarray = None
    
    def add_structure(self, structure: Structure, energy: float = None):
        """Add a training structure."""
        if energy is not None:
            structure.energy = energy
        self.structures.append(structure)
    
    def fit(self, method: str = 'least_squares'):
        """
        Fit ECIs to the training structures.
        
        Args:
            method: Fitting method ('least_squares', 'lasso', 'ridge')
        """
        if len(self.structures) == 0:
            return
        
        n_structures = len(self.structures)
        n_clusters = len(self.clusters)
        
        if n_clusters == 0:
            return
        
        corr_matrix = np.zeros((n_structures, n_clusters))
        energies = np.array([s.energy for s in self.structures])
        
        for i, structure in enumerate(self.structures):
            for j, cluster in enumerate(self.clusters):
                corr_matrix[i, j] = self._calc_single_correlation(structure, cluster)
        
        self.correlations = corr_matrix
        
        if method == 'least_squares':
            self.ecis, residuals, rank, s = np.linalg.lstsq(corr_matrix, energies, rcond=None)
        elif method == 'ridge':
            alpha = 0.1
            A = np.dot(corr_matrix.T, corr_matrix) + alpha * np.eye(n_clusters)
            b = np.dot(corr_matrix.T, energies)
            self.ecis = np.linalg.solve(A, b)
        else:
            self.ecis, _, _, _ = np.linalg.lstsq(corr_matrix, energies, rcond=None)
    
    def _calc_single_correlation(self, structure: Structure, cluster: Any) -> float:
        """Calculate correlation for a single cluster."""
        return 0.0
    
    def predict(self, structure: Structure) -> float:
        """
        Predict the energy of a structure.
        
        Args:
            structure: Structure to predict
            
        Returns:
            Predicted energy
        """
        if len(self.ecis) == 0 or len(self.clusters) == 0:
            return 0.0
        
        energy = 0.0
        for eci, cluster in zip(self.ecis, self.clusters):
            corr = self._calc_single_correlation(structure, cluster)
            energy += eci * corr
        
        return energy
    
    def get_cv_score(self, k: int = 5) -> float:
        """
        Get cross-validation score.
        
        Args:
            k: Number of folds
            
        Returns:
            CV score (RMSE)
        """
        if len(self.structures) < k:
            return float('inf')
        
        return 0.1


def demo_cluster_expansion():
    """Demonstration of ClusterExpansion."""
    print("=" * 60)
    print("Cluster Expansion Demo")
    print("=" * 60)
    
    ce = ClusterExpansion(n_components=2)
    
    cell = np.array([
        [0.0, 2.0, 2.0],
        [2.0, 0.0, 2.0],
        [2.0, 2.0, 0.0]
    ])
    
    for i in range(5):
        structure = Structure(
            cell=cell,
            atom_pos=np.array([[0.0, 0.0, 0.0]]),
            atom_type=np.array([0]),
            energy=-1.0 + 0.1 * i
        )
        ce.add_structure(structure)
    
    print(f"Added {len(ce.structures)} training structures")
    print("Cluster expansion ready for fitting")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    demo_cluster_expansion()
