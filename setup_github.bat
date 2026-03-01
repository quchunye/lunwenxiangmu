@echo off
chcp 65001 >nul
echo ========================================
echo GitHub 自动配置工具
echo ========================================
echo.
echo 本工具将帮助您:
echo 1. 配置 Git 用户信息
echo 2. 关联 GitHub 远程仓库
echo 3. 推送代码到 GitHub
echo.
echo ========================================

REM 配置 Git 用户信息
echo.
set /p GITHUB_USERNAME="请输入您的 GitHub 用户名："
set /p GITHUB_EMAIL="请输入您的 GitHub 邮箱："
set /p REPO_NAME="请输入仓库名称 (例如：fortran-to-python-thesis):"

echo.
echo ========================================
echo 正在配置 Git 用户信息...
echo ========================================
git config --global user.name "%GITHUB_USERNAME%"
git config --global user.email "%GITHUB_EMAIL%"

if %errorlevel%==0 (
    echo ✓ Git 用户信息配置成功
    echo   用户名：%GITHUB_USERNAME%
    echo   邮箱：%GITHUB_EMAIL%
) else (
    echo ✗ Git 配置失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 正在检查远程仓库...
echo ========================================
cd /d "D:\Trae CN\论文"

git remote -v >nul 2>&1
if %errorlevel%==0 (
    echo 当前已配置远程仓库:
    git remote -v
    echo.
    set /p CHANGE_REMOTE="是否更改远程仓库？(Y/N): "
    if /i "%CHANGE_REMOTE%"=="Y" (
        git remote remove origin
    ) else (
        echo 保持现有配置
        goto :PUSH
    )
)

echo.
echo ========================================
echo 正在关联远程仓库...
echo ========================================
set REPO_URL=https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

echo 远程仓库 URL: %REPO_URL%
git remote add origin %REPO_URL%

if %errorlevel%==0 (
    echo ✓ 远程仓库关联成功
) else (
    echo 远程仓库可能已存在，正在更新 URL...
    git remote set-url origin %REPO_URL%
    if %errorlevel%==0 (
        echo ✓ 远程仓库 URL 已更新
    ) else (
        echo ✗ 更新远程仓库失败
        pause
        exit /b 1
    )
)

:PUSH
echo.
echo ========================================
echo 推送到 GitHub...
echo ========================================
echo 提示：如果是首次推送，可能需要输入 GitHub 账号密码或 Token
echo.

git push -u origin master

if %errorlevel%==0 (
    echo.
    echo ========================================
    echo ✓ 推送成功！
    echo ========================================
    echo.
    echo 您的代码已上传到 GitHub:
    echo https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
    echo.
    echo 下次只需运行 "git push" 即可推送更改
) else (
    echo.
    echo ========================================
    echo ✗ 推送失败
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. 仓库不存在 - 请先在 GitHub 创建仓库
    echo 2. 认证失败 - 请使用 Personal Access Token
    echo 3. 网络问题 - 请检查网络连接
    echo.
    echo 创建 Personal Access Token:
    echo https://github.com/settings/tokens
)

echo.
pause
