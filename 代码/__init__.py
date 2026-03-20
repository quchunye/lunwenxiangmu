#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATAT Python - Complete Implementation
Based on ATAT by Axel van de Walle

This package provides:
- mcsqs: Special Quasirandom Structure Generator
- corrdump: Correlation Function Calculator  
- maps: Cluster Expansion
- emc2: Monte Carlo Simulation
"""

from .structure import Structure, MultiCluster, SpaceGroup
from .correlation import (
    generate_trigo_corr_functions,
    CorrFuncTable,
    calc_correlation,
    calc_cluster_diameter,
)
from .mcsqs import MCSQS
from .lattice import (
    create_fcc_lattice,
    create_bcc_lattice,
    generate_pair_clusters,
    generate_triplet_clusters,
    find_supercells,
)
from .corrdump import CorrDump
from .maps import ClusterExpansion
from .emc2 import MonteCarlo

__version__ = "1.0.0"
__author__ = "Based on ATAT by Axel van de Walle"

__all__ = [
    'Structure',
    'MultiCluster',
    'SpaceGroup',
    'MCSQS',
    'CorrDump',
    'ClusterExpansion',
    'MonteCarlo',
    'generate_trigo_corr_functions',
    'CorrFuncTable',
    'calc_correlation',
    'calc_cluster_diameter',
    'create_fcc_lattice',
    'create_bcc_lattice',
    'generate_pair_clusters',
    'generate_triplet_clusters',
    'find_supercells',
]
