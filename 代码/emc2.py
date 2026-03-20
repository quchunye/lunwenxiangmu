#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emc2 - Monte Carlo Simulation
Python implementation based on ATAT by Axel van de Walle

This module implements Monte Carlo simulations for studying alloy thermodynamics.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass, field
import random


@dataclass
class Structure:
    """Represents a crystal structure."""
    cell: np.ndarray = field(default_factory=lambda: np.eye(3))
    atom_pos: np.ndarray = field(default_factory=lambda: np.array([]).reshape(0, 3))
    atom_type: np.ndarray = field(default_factory=lambda: np.array([], dtype=int))


class MonteCarlo:
    """
    Monte Carlo Simulation for alloy systems.
    
    This class implements Monte Carlo simulations for studying
    thermodynamic properties of alloys.
    """
    
    def __init__(self, seed: int = None):
        self.rng = random.Random(seed)
        self.np_rng = np.random.default_rng(seed)
        
        self.structure: Optional[Structure] = None
        self.temperature: float = 300.0
        self.n_steps: int = 10000
        self.equilibrium_steps: int = 1000
        
        self.energy_history: List[float] = []
        self.acceptance_rate: float = 0.0
        
        self._energy_func = None
    
    def set_structure(self, cell: np.ndarray, atom_pos: np.ndarray, 
                      atom_type: np.ndarray):
        """Set the simulation structure."""
        self.structure = Structure(
            cell=np.array(cell, dtype=float),
            atom_pos=np.array(atom_pos, dtype=float),
            atom_type=np.array(atom_type, dtype=int)
        )
    
    def set_energy_function(self, func):
        """Set the energy function for the simulation."""
        self._energy_func = func
    
    def set_temperature(self, temperature: float):
        """Set the simulation temperature in Kelvin."""
        self.temperature = temperature
    
    def calculate_energy(self) -> float:
        """Calculate the current energy of the structure."""
        if self._energy_func is not None:
            return self._energy_func(self.structure)
        return 0.0
    
    def run(self, verbose: bool = True) -> Dict[str, Any]:
        """
        Run the Monte Carlo simulation.
        
        Args:
            verbose: Whether to print progress
            
        Returns:
            Dictionary with simulation results
        """
        if self.structure is None:
            return {'error': 'No structure set'}
        
        self.energy_history = []
        accepted = 0
        total = 0
        
        current_energy = self.calculate_energy()
        
        kB = 8.617333262e-5
        beta = 1.0 / (kB * self.temperature)
        
        for step in range(self.n_steps):
            n_atoms = len(self.structure.atom_type)
            if n_atoms < 2:
                break
            
            i = self.rng.randint(0, n_atoms - 1)
            j = self.rng.randint(0, n_atoms - 1)
            
            while j == i:
                j = self.rng.randint(0, n_atoms - 1)
            
            self.structure.atom_type[i], self.structure.atom_type[j] = \
                self.structure.atom_type[j], self.structure.atom_type[i]
            
            new_energy = self.calculate_energy()
            delta_E = new_energy - current_energy
            
            total += 1
            
            if delta_E < 0 or self.rng.random() < np.exp(-beta * delta_E):
                current_energy = new_energy
                accepted += 1
            else:
                self.structure.atom_type[i], self.structure.atom_type[j] = \
                    self.structure.atom_type[j], self.structure.atom_type[i]
            
            if step >= self.equilibrium_steps:
                self.energy_history.append(current_energy)
            
            if verbose and (step + 1) % 2000 == 0:
                print(f"  Step {step + 1}/{self.n_steps}, E = {current_energy:.4f} eV")
        
        self.acceptance_rate = accepted / total if total > 0 else 0.0
        
        results = {
            'final_energy': current_energy,
            'average_energy': np.mean(self.energy_history) if self.energy_history else current_energy,
            'energy_std': np.std(self.energy_history) if self.energy_history else 0.0,
            'acceptance_rate': self.acceptance_rate,
            'n_steps': self.n_steps
        }
        
        return results
    
    def get_heat_capacity(self) -> float:
        """Calculate heat capacity from energy fluctuations."""
        if len(self.energy_history) < 10:
            return 0.0
        
        kB = 8.617333262e-5
        var_E = np.var(self.energy_history)
        n_atoms = len(self.structure.atom_type) if self.structure else 1
        
        return var_E / (kB * self.temperature ** 2) / n_atoms


def demo_monte_carlo():
    """Demonstration of Monte Carlo simulation."""
    print("=" * 60)
    print("Monte Carlo Simulation Demo")
    print("=" * 60)
    
    mc = MonteCarlo(seed=42)
    
    cell = np.array([
        [0.0, 2.0, 2.0],
        [2.0, 0.0, 2.0],
        [2.0, 2.0, 0.0]
    ])
    
    atom_pos = np.array([
        [0.0, 0.0, 0.0],
        [2.0, 2.0, 0.0],
        [2.0, 0.0, 2.0],
        [0.0, 2.0, 2.0],
    ])
    
    atom_type = np.array([0, 1, 0, 1])
    
    mc.set_structure(cell, atom_pos, atom_type)
    mc.set_temperature(1000.0)
    mc.n_steps = 5000
    mc.equilibrium_steps = 500
    
    def simple_energy(structure):
        energy = 0.0
        for atype in structure.atom_type:
            if atype == 0:
                energy -= 0.1
            else:
                energy += 0.1
        return energy
    
    mc.set_energy_function(simple_energy)
    
    print(f"\nRunning Monte Carlo at T = {mc.temperature} K")
    print(f"Number of atoms: {len(atom_type)}")
    print(f"Number of steps: {mc.n_steps}")
    
    results = mc.run(verbose=True)
    
    print("\n" + "=" * 60)
    print("Results")
    print("=" * 60)
    print(f"Final energy: {results['final_energy']:.4f} eV")
    print(f"Average energy: {results['average_energy']:.4f} eV")
    print(f"Energy std: {results['energy_std']:.4f} eV")
    print(f"Acceptance rate: {results['acceptance_rate']:.2%}")
    print(f"Heat capacity: {mc.get_heat_capacity():.4f} kB/atom")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    demo_monte_carlo()
