# GitHub 配置指南

**配置日期**: 2026-03-01  
**项目位置**: D:\Trae CN\论文\

## 🔧 GitHub 配置步骤

### 方法 1: 使用命令行配置（推荐）

#### 1. 配置 Git 用户信息
```bash
# 设置用户名
git config --global user.name "Your Name"

# 设置邮箱（使用你注册 GitHub 的邮箱）
git config --global user.email "your-email@example.com"
```

#### 2. 在 GitHub 上创建仓库
1. 访问 https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写仓库名称，例如：`fortran-to-python-thesis`
4. 选择 Public 或 Private
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

#### 3. 关联本地仓库
```bash
cd "D:\Trae CN\论文"

# 添加远程仓库（替换 URL 为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 验证
git remote -v

# 推送代码
git push -u origin master
```

#### 4. 后续推送
```bash
# 提交更改
git add .
git commit -m "提交信息"

# 推送到 GitHub
git push
```

---

### 方法 2: 使用 GitHub Desktop

1. 下载 GitHub Desktop: https://desktop.github.com
2. 安装并登录 GitHub 账号
3. 点击 "Add" → "Add Existing Repository"
4. 选择 `D:\Trae CN\论文`
5. 点击 "Publish repository"

---

### 方法 3: 使用 SSH 密钥（更安全）

#### 1. 生成 SSH 密钥
```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```
按回车接受默认位置

#### 2. 添加 SSH 密钥到 GitHub
```bash
# 查看公钥
cat ~/.ssh/id_ed25519.pub
```
复制输出内容

#### 3. 在 GitHub 添加密钥
1. 访问 https://github.com/settings/keys
2. 点击 "New SSH key"
3. 粘贴公钥内容
4. 点击 "Add SSH key"

#### 4. 使用 SSH 关联
```bash
cd "D:\Trae CN\论文"
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin master
```

---

## 📝 自动化脚本

### 创建 setup_github.bat

```batch
@echo off
chcp 65001 >nul
echo ========================================
echo GitHub 配置工具
echo ========================================
echo.

set REPO_URL=https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

echo 请配置以下信息:
echo.

set /p USERNAME="输入 GitHub 用户名："
set /p EMAIL="输入 GitHub 邮箱："
set /p REPO_NAME="输入仓库名称："

echo.
echo 正在配置 Git...
git config --global user.name "%USERNAME%"
git config --global user.email "%EMAIL%"
echo ✓ Git 用户信息已配置
echo.

echo 正在关联远程仓库...
cd /d "D:\Trae CN\论文"
git remote add origin https://github.com/%USERNAME%/%REPO_NAME%.git
if %errorlevel%==0 (
    echo ✓ 远程仓库已关联
) else (
    echo ✗ 可能已经配置过远程仓库
    git remote set-url origin https://github.com/%USERNAME%/%REPO_NAME%.git
    echo ✓ 远程仓库 URL 已更新
)

echo.
echo 正在推送到 GitHub...
git push -u origin master
if %errorlevel%==0 (
    echo ✓ 推送成功！
    echo.
    echo 仓库地址：https://github.com/%USERNAME%/%REPO_NAME%.git
) else (
    echo ✗ 推送失败，请检查网络连接和仓库设置
)

echo.
pause
```

---

## 🔍 常用 GitHub 命令

### 查看远程仓库
```bash
git remote -v
```

### 查看状态
```bash
git status
```

### 查看提交历史
```bash
git log --oneline
```

### 拉取远程更改
```bash
git pull
```

### 推送本地更改
```bash
git push
```

### 克隆仓库
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

---

## ⚠️ 注意事项

1. **不要提交敏感信息**
   - 检查 `.gitignore` 文件
   - 不要提交密码、API 密钥等

2. **定期推送**
   - 每次重要修改后推送到 GitHub
   - 作为异地备份

3. **分支管理**
   - 主分支：master/main
   - 开发分支：dev
   - 实验分支：experiment-*

4. **提交信息规范**
   ```
   feat: 新功能
   fix: 修复 bug
   docs: 文档更新
   style: 代码格式
   refactor: 重构
   test: 测试
   chore: 构建/工具
   ```

---

## 🎯 快速配置检查清单

- [ ] 配置 Git 用户名
- [ ] 配置 Git 邮箱
- [ ] 在 GitHub 创建仓库
- [ ] 关联远程仓库
- [ ] 首次推送
- [ ] 测试拉取和推送
- [ ] 配置 SSH 密钥（可选）

---

## 📞 需要您提供的信息

为了帮您自动配置 GitHub，请提供：

1. **GitHub 用户名**: 
2. **GitHub 邮箱**: 
3. **仓库名称**: (例如：fortran-to-python-thesis)
4. **仓库类型**: Public / Private

提供后，我可以帮您：
- 自动生成配置脚本
- 创建 .gitignore 优化
- 设置 README.md
- 配置 GitHub Actions

---

**配置状态**: ⏳ 待配置  
**最后更新**: 2026-03-01
