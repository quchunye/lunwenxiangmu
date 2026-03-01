@echo off
chcp 65001 >nul
echo ========================================
echo 论文项目基础框架检查工具
echo ========================================
echo.
echo 检查位置：D:\Trae CN\论文\
echo.

set BASE_DIR=D:\Trae CN\论文
set ERROR_COUNT=0

echo [1] 检查目录结构...
echo ========================================

if exist "%BASE_DIR%\src\fortran" (
    echo ✓ src\fortran\ 目录存在
) else (
    echo ✗ src\fortran\ 目录缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\src\python" (
    echo ✓ src\python\ 目录存在
) else (
    echo ✗ src\python\ 目录缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\backups\timestamped" (
    echo ✓ backups\timestamped\ 目录存在
) else (
    echo ✗ backups\timestamped\ 目录缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\backups\aliyun" (
    echo ✓ backups\aliyun\ 目录存在
) else (
    echo ✗ backups\aliyun\ 目录缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\docs\papers" (
    echo ✓ docs\papers\ 目录存在
) else (
    echo ✗ docs\papers\ 目录缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\docs\experiments" (
    echo ✓ docs\experiments\ 目录存在
) else (
    echo ✗ docs\experiments\ 目录缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\scripts\backup" (
    echo ✓ scripts\backup\ 目录存在
) else (
    echo ✗ scripts\backup\ 目录缺失
    set /a ERROR_COUNT+=1
)

echo.
echo [2] 检查关键文件...
echo ========================================

if exist "%BASE_DIR%\src\fortran\hello_fortran.f90" (
    echo ✓ src\fortran\hello_fortran.f90
) else (
    echo ✗ src\fortran\hello_fortran.f90 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\src\python\fortran_to_python_converter.py" (
    echo ✓ src\python\fortran_to_python_converter.py
) else (
    echo ✗ src\python\fortran_to_python_converter.py 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\src\python\hello_fortran_converted.py" (
    echo ✓ src\python\hello_fortran_converted.py
) else (
    echo ✗ src\python\hello_fortran_converted.py 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\scripts\backup\auto_backup.py" (
    echo ✓ scripts\backup\auto_backup.py
) else (
    echo ✗ scripts\backup\auto_backup.py 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\scripts\backup\git_backup.py" (
    echo ✓ scripts\backup\git_backup.py
) else (
    echo ✗ scripts\backup\git_backup.py 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\scripts\backup\run_backup.bat" (
    echo ✓ scripts\backup\run_backup.bat
) else (
    echo ✗ scripts\backup\run_backup.bat 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\fortran_env.bat" (
    echo ✓ fortran_env.bat
) else (
    echo ✗ fortran_env.bat 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\python_env.bat" (
    echo ✓ python_env.bat
) else (
    echo ✗ python_env.bat 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\README.md" (
    echo ✓ README.md
) else (
    echo ✗ README.md 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\项目使用快速指南.md" (
    echo ✓ 项目使用快速指南.md
) else (
    echo ✗ 项目使用快速指南.md 缺失
    set /a ERROR_COUNT+=1
)

echo.
echo [3] 检查文档...
echo ========================================

if exist "%BASE_DIR%\docs\论文步骤记录.md" (
    echo ✓ docs\论文步骤记录.md
) else (
    echo ✗ docs\论文步骤记录.md 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\docs\项目搭建完成总结.md" (
    echo ✓ docs\项目搭建完成总结.md
) else (
    echo ✗ docs\项目搭建完成总结.md 缺失
    set /a ERROR_COUNT+=1
)

if exist "%BASE_DIR%\docs\experiments\实验记录模板.md" (
    echo ✓ docs\experiments\实验记录模板.md
) else (
    echo ✗ docs\experiments\实验记录模板.md 缺失
    set /a ERROR_COUNT+=1
)

echo.
echo [4] 检查 Git 配置...
echo ========================================

cd /d "%BASE_DIR%"
if exist ".git" (
    echo ✓ Git 仓库已初始化
) else (
    echo ✗ Git 仓库未初始化
    set /a ERROR_COUNT+=1
)

git remote -v >nul 2>&1
if %errorlevel%==0 (
    echo ✓ Git 远程仓库已配置
    echo   远程仓库:
    git remote -v
) else (
    echo ⚠ Git 远程仓库未配置 (可选)
)

echo.
echo [5] 测试功能...
echo ========================================

echo 测试 Fortran 编译...
cd /d "%BASE_DIR%\src\fortran"
gfortran hello_fortran.f90 -o test_compile.exe >nul 2>&1
if %errorlevel%==0 (
    echo ✓ Fortran 编译器工作正常
    del test_compile.exe
) else (
    echo ⚠ Fortran 编译器不可用或未安装
)

echo 测试 Python 环境...
python --version >nul 2>&1
if %errorlevel%==0 (
    echo ✓ Python 环境可用
    python --version
) else (
    echo ✗ Python 环境不可用
    set /a ERROR_COUNT+=1
)

echo.
echo ========================================
echo 检查结果汇总
echo ========================================
if %ERROR_COUNT%==0 (
    echo ✓ 所有检查项通过！基础框架完整
) else (
    echo ✗ 发现 %ERROR_COUNT% 个问题或缺失
)

echo.
echo ========================================
echo 下一步建议
echo ========================================
echo 1. 配置 GitHub: 运行 setup_github.bat
echo 2. 查看使用指南：项目使用快速指南.md
echo 3. 开始编写代码：src\fortran\
echo 4. 记录实验：docs\experiments\实验记录模板.md

echo.
pause
