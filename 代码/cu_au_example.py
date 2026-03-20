#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cu-Au 二元合金完整算例
用于毕业论文第四章实证分析
"""

import numpy as np
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from structure import Structure
from correlation import generate_trigo_corr_functions, CorrFuncTable, calc_cluster_diameter
from lattice import create_fcc_lattice, generate_pair_clusters
from corrdump import CorrDump


def run_cu_au_example():
    """运行Cu-Au二元合金完整算例"""
    
    print("=" * 70)
    print("Cu-Au 二元合金 SSOS 搜索完整算例")
    print("=" * 70)
    
    results = {}
    
    # ========== Step 1: 晶格设置 ==========
    print("\n" + "=" * 70)
    print("Step 1: 设置FCC晶格")
    print("=" * 70)
    
    a = 3.615  # Cu的晶格参数 (Angstrom)
    cell = np.array([
        [0.0, a/2, a/2],
        [a/2, 0.0, a/2],
        [a/2, a/2, 0.0]
    ])
    
    print(f"\nFCC晶格参数: a = {a} Å")
    print(f"晶格矢量:")
    for i, v in enumerate(cell):
        print(f"  a{i+1} = [{v[0]:.4f}, {v[1]:.4f}, {v[2]:.4f}] Å")
    
    atom_pos = np.array([[0.0, 0.0, 0.0]])
    atom_type = np.array([0])
    
    volume = np.abs(np.linalg.det(cell))
    print(f"\n原胞体积: {volume:.4f} Å³")
    
    results['lattice'] = {
        'parameter': a,
        'volume': volume,
        'cell': cell
    }
    
    # ========== Step 2: 超胞生成 ==========
    print("\n" + "=" * 70)
    print("Step 2: 超胞生成")
    print("=" * 70)
    
    supercell_sizes = [4, 8, 16]
    supercells = []
    
    for n_atoms in supercell_sizes:
        size = int(round(n_atoms ** (1/3)))
        if size < 1:
            size = 1
        
        sc_cell = cell * size
        sc_volume = np.abs(np.linalg.det(sc_cell))
        
        sc_pos = []
        sc_types = []
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    offset = np.array([i, j, k]) / size
                    for pos in atom_pos:
                        frac_pos = pos / (cell[0] + cell[1] + cell[2]) + offset
                        sc_pos.append(np.dot(sc_cell, frac_pos / size))
                        sc_types.append(0)
        
        sc_pos = np.array(sc_pos)
        sc_types = np.array(sc_types)
        
        supercells.append({
            'n_atoms': len(sc_pos),
            'cell': sc_cell,
            'volume': sc_volume,
            'size': size
        })
        
        print(f"\n超胞 {size}×{size}×{size}:")
        print(f"  原子数: {len(sc_pos)}")
        print(f"  体积: {sc_volume:.4f} Å³")
    
    results['supercells'] = supercells
    
    # ========== Step 3: 不可约构型生成 ==========
    print("\n" + "=" * 70)
    print("Step 3: 不可约构型生成")
    print("=" * 70)
    
    n_atoms = 4
    print(f"\n选择 {n_atoms} 原子超胞进行构型生成")
    
    all_configs = []
    for i in range(2 ** n_atoms):
        config = [(i >> j) & 1 for j in range(n_atoms)]
        all_configs.append(config)
    
    unique_configs = []
    for config in all_configs:
        n_cu = sum(config)
        n_au = n_atoms - n_cu
        is_unique = True
        for uc in unique_configs:
            if uc['n_cu'] == n_cu and uc['n_au'] == n_au:
                is_unique = False
                break
        if is_unique:
            unique_configs.append({
                'config': config,
                'n_cu': n_cu,
                'n_au': n_au,
                'composition': n_cu / n_atoms
            })
    
    print(f"\n总构型数: {len(all_configs)}")
    print(f"不可约构型数: {len(unique_configs)}")
    print(f"\n不可约构型列表:")
    print(f"{'编号':<6} {'Cu原子数':<10} {'Au原子数':<10} {'Cu成分':<10}")
    print("-" * 40)
    for i, uc in enumerate(unique_configs):
        print(f"{i+1:<6} {uc['n_cu']:<10} {uc['n_au']:<10} {uc['composition']:.2f}")
    
    results['configurations'] = unique_configs
    
    # ========== Step 4: 关联函数计算 ==========
    print("\n" + "=" * 70)
    print("Step 4: 关联函数计算")
    print("=" * 70)
    
    corrdump = CorrDump(n_components=2)
    corrdump.set_lattice(cell, atom_pos, atom_type)
    
    max_distance = a * 1.5
    clusters = generate_pair_clusters(cell, atom_pos, max_distance)
    
    for cluster in clusters[:4]:
        corrdump.add_cluster(cluster)
    
    print(f"\n团簇生成:")
    print(f"  最大距离: {max_distance:.4f} Å")
    print(f"  生成团簇数: {len(corrdump.clusters)}")
    
    print(f"\n团簇信息:")
    for i, mcluster in enumerate(corrdump.clusters):
        print(f"  团簇 {i+1}: 直径 = {mcluster.diameter:.4f} Å")
    
    sc_cell_4 = cell * 2
    sc_pos_4 = []
    for i in range(2):
        for j in range(2):
            offset = np.array([i, j]) * 0.5
            frac_pos = np.array([0.0, 0.0, 0.0]) + np.array([offset[0], offset[1], 0.0])
            pos = np.dot(sc_cell_4, frac_pos)
            sc_pos_4.append(pos)
    sc_pos_4 = np.array(sc_pos_4[:4])
    print(f"\n4原子超胞坐标数: {len(sc_pos_4)}")
    
    corr_matrix = []
    print(f"\n关联函数矩阵:")
    print(f"{'构型':<8}", end="")
    for i in range(len(corrdump.clusters)):
        print(f"Π_{i:<6}", end="")
    print()
    print("-" * 60)
    
    for i, uc in enumerate(unique_configs):
        atom_types = np.array(uc['config'])
        test_structure = Structure(
            cell=sc_cell_4,
            atom_pos=sc_pos_4,
            atom_type=atom_types
        )
        
        correlations = corrdump.calculate_correlations(test_structure)
        corr_matrix.append(correlations)
        
        print(f"{i+1:<8}", end="")
        for corr in correlations:
            print(f"{corr:<8.4f}", end="")
        print()
    
    corr_matrix = np.array(corr_matrix)
    results['correlation_matrix'] = corr_matrix
    
    # ========== Step 5: SSOS搜索 ==========
    print("\n" + "=" * 70)
    print("Step 5: SSOS搜索")
    print("=" * 70)
    
    from scipy.optimize import nnls
    
    def randomized_omp(A, b, k, max_iter=1000):
        best_residual = float('inf')
        best_x = None
        best_support = None
        
        for _ in range(max_iter):
            support = [np.random.randint(A.shape[1])]
            residual = b.copy()
            
            for _ in range(k - 1):
                correlations = A.T @ residual
                for s in support:
                    correlations[s] = 0
                
                if np.max(correlations) <= 0:
                    break
                
                max_indices = np.where(correlations == np.max(correlations))[0]
                new_index = np.random.choice(max_indices)
                support.append(new_index)
                
                A_support = A[:, support]
                x_support, _ = nnls(A_support, b)
                residual = b - A_support @ x_support
            
            A_support = A[:, support]
            x_support, _ = nnls(A_support, b)
            residual_norm = np.linalg.norm(b - A_support @ x_support)
            
            if residual_norm < best_residual:
                best_residual = residual_norm
                best_x = np.zeros(A.shape[1])
                best_x[support] = x_support
                best_support = support
        
        return best_x, best_support, best_residual
    
    A = corr_matrix.T
    n_configs = A.shape[1]
    A = np.vstack((A, np.ones(n_configs)))
    m = A.shape[0]
    b = np.zeros(m)
    b[-1] = 1
    
    print(f"\n目标: 搜索SSOS结构集合")
    print(f"候选构型数: {n_configs}")
    print(f"目标关联函数: [0, 0, 0, 0, 1] (随机合金)")
    
    ssos_results = []
    for k in [2, 3, 4, 5]:
        print(f"\n搜索 {k} 个结构的SSOS...")
        start_time = time.time()
        
        w, support, residual = randomized_omp(A, b, k, max_iter=500)
        
        elapsed = time.time() - start_time
        
        weights = w[w > 1e-10]
        
        result = {
            'k': k,
            'support': support,
            'weights': weights,
            'residual': residual,
            'time': elapsed
        }
        ssos_results.append(result)
        
        print(f"  选中构型: {[s+1 for s in support]}")
        print(f"  权重: {[f'{w:.4f}' for w in weights]}")
        print(f"  残差: {residual:.6f}")
        print(f"  用时: {elapsed:.4f} 秒")
    
    results['ssos'] = ssos_results
    
    # ========== 结果汇总 ==========
    print("\n" + "=" * 70)
    print("结果汇总")
    print("=" * 70)
    
    print("\n1. 超胞生成:")
    print(f"   测试了 {len(supercells)} 种超胞规模")
    
    print("\n2. 构型生成:")
    print(f"   总构型数: {len(all_configs)}")
    print(f"   不可约构型数: {len(unique_configs)}")
    print(f"   压缩比: {len(all_configs)/len(unique_configs):.2f}")
    
    print("\n3. 关联函数:")
    print(f"   团簇数: {len(corrdump.clusters)}")
    print(f"   关联函数矩阵: {corr_matrix.shape}")
    
    print("\n4. SSOS搜索结果对比:")
    print(f"{'结构数':<8} {'残差':<12} {'用时(秒)':<10}")
    print("-" * 35)
    for r in ssos_results:
        print(f"{r['k']:<8} {r['residual']:<12.6f} {r['time']:<10.4f}")
    
    best_result = min(ssos_results, key=lambda x: x['residual'])
    print(f"\n最优结果: {best_result['k']} 个结构")
    print(f"  构型编号: {[s+1 for s in best_result['support']]}")
    print(f"  权重: {[f'{w:.4f}' for w in best_result['weights']]}")
    
    return results


if __name__ == "__main__":
    results = run_cu_au_example()
    
    print("\n" + "=" * 70)
    print("算例完成！数据已保存，可用于论文第四章。")
    print("=" * 70)
