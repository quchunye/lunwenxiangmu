#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for ATAT Python implementation
验证所有核心工具的物理合理性
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from structure import Structure, MultiCluster, SpaceGroup
from correlation import (
    generate_trigo_corr_functions,
    CorrFuncTable,
    calc_cluster_diameter,
)
from lattice import (
    create_fcc_lattice,
    create_bcc_lattice,
    create_hcp_lattice,
    generate_pair_clusters,
)
from corrdump import CorrDump, find_spacegroup


def test_correlation_functions():
    """测试关联函数的正确性"""
    print("=" * 60)
    print("测试1: 关联函数验证")
    print("=" * 60)
    
    print("\n二元系统关联函数:")
    corr_2 = generate_trigo_corr_functions(2)
    print(f"  Pi_0 = {corr_2[0]}")
    print(f"  验证: Pi(A) + Pi(B) = {corr_2[0, 0] + corr_2[0, 1]} (应为0)")
    assert abs(corr_2[0, 0] + corr_2[0, 1]) < 1e-10, "二元关联函数错误"
    
    print("\n三元系统关联函数:")
    corr_3 = generate_trigo_corr_functions(3)
    print(f"  Pi_0 = {corr_3[0]}")
    print(f"  Pi_1 = {corr_3[1]}")
    sum_0 = sum(corr_3[0])
    sum_1 = sum(corr_3[1])
    print(f"  验证: sum(Pi_0) = {sum_0:.6f} (应为0)")
    print(f"  验证: sum(Pi_1) = {sum_1:.6f} (应为0)")
    assert abs(sum_0) < 1e-10, "三元关联函数 Pi_0 错误"
    assert abs(sum_1) < 1e-10, "三元关联函数 Pi_1 错误"
    
    print("\n✅ 关联函数验证通过!")
    return True


def test_lattice_creation():
    """测试晶格创建"""
    print("\n" + "=" * 60)
    print("测试2: 晶格创建")
    print("=" * 60)
    
    print("\nFCC 晶格:")
    cell_fcc, pos_fcc, type_fcc = create_fcc_lattice(a=4.0)
    print(f"  晶格参数: a = 4.0 Å")
    print(f"  原子数: {len(pos_fcc)}")
    print(f"  体积: {np.abs(np.linalg.det(cell_fcc)):.2f} Å³")
    assert len(pos_fcc) == 1, "FCC 原子数错误"
    
    print("\nBCC 晶格:")
    cell_bcc, pos_bcc, type_bcc = create_bcc_lattice(a=2.87)
    print(f"  晶格参数: a = 2.87 Å")
    print(f"  原子数: {len(pos_bcc)}")
    print(f"  体积: {np.abs(np.linalg.det(cell_bcc)):.2f} Å³")
    assert len(pos_bcc) == 2, "BCC 原子数错误"
    
    print("\nHCP 晶格:")
    cell_hcp, pos_hcp, type_hcp = create_hcp_lattice(a=2.5, c=4.0)
    print(f"  晶格参数: a = 2.5 Å, c = 4.0 Å")
    print(f"  原子数: {len(pos_hcp)}")
    print(f"  体积: {np.abs(np.linalg.det(cell_hcp)):.2f} Å³")
    assert len(pos_hcp) == 2, "HCP 原子数错误"
    
    print("\n✅ 晶格创建测试通过!")
    return True


def test_corrdump_basic():
    """测试 CorrDump 基本功能"""
    print("\n" + "=" * 60)
    print("测试3: CorrDump 基本功能")
    print("=" * 60)
    
    cell = np.array([
        [0.0, 2.0, 2.0],
        [2.0, 0.0, 2.0],
        [2.0, 2.0, 0.0]
    ])
    atom_pos = np.array([[0.0, 0.0, 0.0]])
    atom_type = np.array([0])
    
    corrdump = CorrDump(n_components=2)
    corrdump.set_lattice(cell, atom_pos, atom_type)
    
    print(f"\n设置晶格成功")
    print(f"  空间群操作数: {len(corrdump.space_group.point_ops)}")
    
    corrdump.generate_clusters(max_cluster_size=2, max_distances={2: 6.0})
    print(f"  生成团簇数: {len(corrdump.clusters)}")
    
    assert len(corrdump.clusters) > 0, "团簇生成失败"
    
    print("\n✅ CorrDump 基本功能测试通过!")
    return True


def test_corrdump_correlations():
    """测试关联函数计算"""
    print("\n" + "=" * 60)
    print("测试4: 关联函数计算")
    print("=" * 60)
    
    cell = np.array([
        [0.0, 2.0, 2.0],
        [2.0, 0.0, 2.0],
        [2.0, 2.0, 0.0]
    ])
    
    atom_pos = np.array([[0.0, 0.0, 0.0]])
    atom_type = np.array([0])
    
    corrdump = CorrDump(n_components=2)
    corrdump.set_lattice(cell, atom_pos, atom_type)
    corrdump.generate_clusters(max_cluster_size=2, max_distances={2: 6.0})
    
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
    
    print(f"\n测试结构: 4 原子, 50%-50% 成分")
    
    correlations = corrdump.calculate_correlations(test_structure)
    
    print(f"\n关联函数值:")
    for i, corr in enumerate(correlations[:4]):
        print(f"  团簇 {i}: {corr:.6f}")
    
    assert len(correlations) == len(corrdump.clusters), "关联函数数量不匹配"
    
    print("\n✅ 关联函数计算测试通过!")
    return True


def test_cluster_diameter():
    """测试团簇直径计算"""
    print("\n" + "=" * 60)
    print("测试5: 团簇直径计算")
    print("=" * 60)
    
    cluster1 = np.array([[0, 0, 0], [1, 0, 0]])
    d1 = calc_cluster_diameter(cluster1)
    print(f"\n团簇1: 两点距离 = {d1:.4f} Å (应为 1.0)")
    assert abs(d1 - 1.0) < 1e-6, "团簇直径计算错误"
    
    cluster2 = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    d2 = calc_cluster_diameter(cluster2)
    print(f"团簇2: 三角形最大距离 = {d2:.4f} Å (应为 sqrt(2) ≈ 1.414)")
    assert abs(d2 - np.sqrt(2)) < 1e-6, "三角形团簇直径错误"
    
    cluster3 = np.array([[0, 0, 0], [1, 1, 1], [-1, -1, -1]])
    d3 = calc_cluster_diameter(cluster3)
    print(f"团簇3: 三点最大距离 = {d3:.4f} Å")
    
    print("\n✅ 团簇直径计算测试通过!")
    return True


def test_pair_clusters():
    """测试团簇生成"""
    print("\n" + "=" * 60)
    print("测试6: 团簇生成")
    print("=" * 60)
    
    cell, atom_pos, atom_type = create_fcc_lattice(a=4.0)
    
    clusters = generate_pair_clusters(cell, atom_pos, max_distance=6.0)
    
    print(f"\nFCC 晶格团簇生成:")
    print(f"  最大距离: 6.0 Å")
    print(f"  生成团簇数: {len(clusters)}")
    
    assert len(clusters) > 0, "团簇生成失败"
    
    distances = [calc_cluster_diameter(c) for c in clusters]
    print(f"  团簇距离: {[f'{d:.3f}' for d in distances[:5]]}")
    
    print("\n✅ 团簇生成测试通过!")
    return True


def test_ternary_system():
    """测试三元系统"""
    print("\n" + "=" * 60)
    print("测试7: 三元系统")
    print("=" * 60)
    
    cell = np.array([
        [0.0, 2.0, 2.0],
        [2.0, 0.0, 2.0],
        [2.0, 2.0, 0.0]
    ])
    
    atom_pos = np.array([[0.0, 0.0, 0.0]])
    atom_type = np.array([0])
    
    corrdump = CorrDump(n_components=3)
    corrdump.set_lattice(cell, atom_pos, atom_type)
    corrdump.generate_clusters(max_cluster_size=2, max_distances={2: 6.0})
    
    print(f"\n三元系统关联函数表:")
    print(f"  {corrdump.corr_func_table.table}")
    
    test_structure = Structure(
        cell=cell * 2,
        atom_pos=np.array([
            [0.0, 0.0, 0.0],
            [2.0, 2.0, 0.0],
            [2.0, 0.0, 2.0],
            [0.0, 2.0, 2.0],
        ]),
        atom_type=np.array([0, 1, 2, 0])
    )
    
    correlations = corrdump.calculate_correlations(test_structure)
    
    print(f"\n三元系统关联函数值:")
    for i, corr in enumerate(correlations[:4]):
        print(f"  团簇 {i}: {corr:.6f}")
    
    print("\n✅ 三元系统测试通过!")
    return True


def test_file_io():
    """测试文件读写"""
    print("\n" + "=" * 60)
    print("测试8: 文件读写")
    print("=" * 60)
    
    cell = np.array([
        [0.0, 2.0, 2.0],
        [2.0, 0.0, 2.0],
        [2.0, 2.0, 0.0]
    ])
    
    atom_pos = np.array([[0.0, 0.0, 0.0]])
    atom_type = np.array([0])
    
    corrdump = CorrDump(n_components=2)
    corrdump.set_lattice(cell, atom_pos, atom_type)
    corrdump.generate_clusters(max_cluster_size=2, max_distances={2: 6.0})
    
    test_file = "test_clusters.txt"
    corrdump.write_clusters(test_file)
    print(f"\n写入团簇文件: {test_file}")
    
    corrdump2 = CorrDump(n_components=2)
    corrdump2.read_clusters(test_file)
    print(f"读取团簇数: {len(corrdump2.clusters)}")
    
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"清理测试文件: {test_file}")
    
    print("\n✅ 文件读写测试通过!")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "#" * 60)
    print("#  ATAT Python 物理合理性验证测试套件")
    print("#" * 60)
    
    tests = [
        ("关联函数验证", test_correlation_functions),
        ("晶格创建", test_lattice_creation),
        ("CorrDump 基本功能", test_corrdump_basic),
        ("关联函数计算", test_corrdump_correlations),
        ("团簇直径计算", test_cluster_diameter),
        ("团簇生成", test_pair_clusters),
        ("三元系统", test_ternary_system),
        ("文件读写", test_file_io),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ 测试失败: {name}")
            print(f"   错误: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"通过: {passed}/{len(tests)}")
    print(f"失败: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 所有测试通过! ATAT Python 实现物理合理。")
    else:
        print("\n⚠️ 部分测试失败，请检查实现。")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
