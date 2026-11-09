# Fortran 到 Python 自动转换 - 论文研究项目

## 项目概述

本项目旨在利用 AI agent 技术，将 Fortran 代码自动转换为 Python 代码，并结合文献实现以下功能：

- **不可约构型** (Irreducible Configurations)
- **超胞构建** (Supercell Construction)
- **特殊准随机结构搜索** (Special Quasirandom Structure Search)
- **有序结构小集合搜索** (Small Ordered Structure Set Search)

## 项目目录结构

```
项目根目录/
├── src/                        # 源代码目录
│   ├── fortran/               # Fortran 源代码
│   └── python/                # Python 转换代码
├── backups/                    # 备份目录
│   ├── timestamped/          # 时间戳备份
│   └── aliyun/               # 阿里云备份
├── docs/                       # 文档目录
│   ├── papers/               # 论文资料
│   └── experiments/          # 实验记录
├── scripts/                    # 脚本目录
│   └── backup/               # 备份脚本
├── fortran_env.bat            # Fortran 环境配置
├── python_env.bat             # Python 环境配置
└── README.md                  # 项目说明
```

## 快速开始

### 1. 环境配置

#### Fortran 环境
```bash
# 运行 Fortran 环境配置
fortran_env.bat
```

#### Python 环境
```bash
# 运行 Python 环境配置
python_env.bat

# 安装必要的包
pip install numpy sympy
```

### 2. 编译和运行 Fortran 程序

```bash
# 配置环境
fortran_env.bat

# 编译程序
gfortran hello_fortran.f90 -o hello_fortran.exe

# 运行程序
hello_fortran.exe
```

### 3. 备份和版本控制

#### 自动备份（本地 + 阿里云）
```bash
# 运行自动备份脚本
scripts\backup\run_backup.bat
```

#### Git 提交并备份
```bash
# 使用 Python 脚本提交并备份
python scripts\backup\git_backup.py "提交信息"
```

#### 手动 Git 操作
```bash
# 查看状态
git status

# 添加文件
git add .

# 提交更改
git commit -m "提交信息"

# 查看历史
git log
```

## 备份策略

本项目采用**组合备份策略**确保数据安全和可复现性：

### 1. Git 版本控制
- 每次重要更改都提交到 Git
- 支持版本回退和历史追溯
- 提交信息包含时间戳

### 2. 时间戳文件夹备份
- 自动创建带时间戳的备份文件夹
- 保留最近 30 天的备份
- 包含源代码、文档和配置

### 3. 阿里云备份
- 定期同步到阿里云盘
- 压缩备份减少存储空间
- 异地备份确保数据安全

### 4. 自动备份脚本
- `scripts/backup/auto_backup.py` - 主备份脚本
- `scripts/backup/git_backup.py` - Git 提交 + 备份
- `scripts/backup/run_backup.bat` - 快速运行备份

## 可复现性保证

### 1. 环境配置脚本
- `fortran_env.bat` - Fortran 编译器环境
- `python_env.bat` - Python 环境检查

### 2. 自动化脚本
- 所有操作都通过脚本执行
- 避免手动操作带来的不一致性

### 3. 详细文档记录
- 实验记录模板
- 步骤文档
- 代码注释

## 研究内容

### 阶段 1: Fortran 代码分析
- [ ] 收集现有 Fortran 代码
- [ ] 分析代码结构和功能
- [ ] 建立代码功能分类体系

### 阶段 2: AI Agent 转换
- [ ] 训练/微调 AI 模型
- [ ] 实现 Fortran 到 Python 语法转换
- [ ] 验证转换正确性

### 阶段 3: 功能实现
- [ ] 不可约构型生成
- [ ] 超胞构建算法
- [ ] 特殊准随机结构搜索
- [ ] 有序结构小集合搜索

### 阶段 4: 验证和优化
- [ ] 与原始 Fortran 代码对比
- [ ] 性能测试
- [ ] 准确性验证

## 使用文献

文献资料存放在 `docs/papers/` 目录，包括：
- 晶体结构理论
- 对称性分析
- 结构搜索算法
- 材料计算方法

## 实验记录

实验记录模板位于 `docs/experiments/` 目录，每次实验应包含：
- 实验日期和时间
- 实验目的
- 使用的代码版本
- 输入参数
- 输出结果
- 分析和结论

## 常见问题

### Q: 如何恢复备份？
A: 从 `backups/timestamped/` 选择对应日期的备份文件夹，复制回项目根目录。

### Q: Git 提交失败怎么办？
A: 检查是否配置了 Git 用户信息：
```bash
git config --global user.email "your@email.com"
git config --global user.name "Your Name"
```

### Q: 如何配置阿里云备份？
A: 目前使用本地压缩包形式，实际上传需要使用阿里云盘客户端或 API。

## 贡献者

- 研究者：[您的姓名]
- 指导教师：[教师姓名]
- 机构：[您的机构]

## 许可证

本项目为学术研究项目，所有代码和数据仅供研究使用。

## 联系方式

- Email: [您的邮箱]
- 日期：2026 年 3 月

---

*最后更新：2026-03-01*
