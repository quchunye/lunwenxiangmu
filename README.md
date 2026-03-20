# 毕业论文提交材料

**作者**: 曲春晔  
**日期**: 2026年3月20日

---

## 文件夹结构

```
论文提交材料/
│
├── 毕业论文_曲春晔.md          # 完整论文 (主文件)
├── 开题报告曲春晔.docx         # 开题报告
├── 论文图表_专业版.md          # 图表文档
├── 项目完整复现指南.md         # 复现步骤说明
├── 完整对话记录.md             # 项目全过程记录
├── generate_pro_figures.py     # 图表生成脚本
├── verify_theory.py            # 理论验证脚本
│
├── figures/                    # 论文图表 (6个)
│   ├── fig1_supercell_pro.png
│   ├── fig2_configurations_pro.png
│   ├── fig3_correlation_pro.png
│   ├── fig4_ssos_pro.png
│   ├── fig5_comparison_pro.png
│   └── system_architecture.drawio
│
└── 代码/                       # 完整代码 (22个文件)
    ├── Python代码 (12个)
    │   ├── __init__.py
    │   ├── corrdump.py         # 关联函数计算
    │   ├── correlation.py      # 关联函数模块
    │   ├── cu_au_example.py    # Cu-Au算例
    │   ├── emc2.py             # 蒙特卡洛
    │   ├── lattice.py          # 晶格模块
    │   ├── maps.py             # 相图计算
    │   ├── mcp_server.py       # MCP接口
    │   ├── mcsqs.py            # SQS生成器
    │   ├── nnomp.py            # SSOS搜索
    │   ├── structure.py        # 结构模块
    │   └── test_atat.py        # 测试文件
    │
    └── fortran/                # Fortran代码 (10个)
        ├── supercell.f90       # 超胞构建
        ├── disorder.f90        # 无序构型
        ├── configurations.f90  # 构型生成
        ├── symmetry.f90        # 对称性分析
        ├── structure.f90       # 结构处理
        ├── groups.f90          # 群操作
        ├── functions.f90       # 工具函数
        ├── outfiles.f90        # 文件输出
        ├── progress.f90        # 进度显示
        └── stdout.f90          # 标准输出
```

---

## 快速查看

### 1. 论文主文件
- **毕业论文_曲春晔.md** - 完整论文 (~15000字)

### 2. 图表
- 打开 `figures/` 文件夹查看6个专业图表

### 3. 代码
- **Python代码**: `代码/` 目录下12个文件
- **Fortran代码**: `代码/fortran/` 目录下10个文件

### 4. 复现步骤
- 查看 `项目完整复现指南.md`

### 5. 答辩准备
- 查看 `完整对话记录.md` 中的答辩常见问题

---

## 项目统计

| 指标 | 数值 |
|------|------|
| 论文字数 | ~15000字 |
| 参考文献 | 15篇 |
| 图表数量 | 6个 |
| Python代码 | 12个文件 |
| Fortran代码 | 10个文件 |
| 测试用例 | 8个通过 |

---

## GitHub备份

https://github.com/quchunye/mcsqs-python

---

**创建日期**: 2026年3月20日
