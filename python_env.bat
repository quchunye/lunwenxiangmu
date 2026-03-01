@echo off
REM ========================================
REM Python 环境配置脚本
REM 论文项目：Fortran 到 Python 自动转换
REM ========================================

echo ========================================
echo Python 环境配置
echo ========================================

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python 版本:
python --version
echo.

REM 检查必要的包
echo 检查必要的 Python 包...
python -c "import numpy; print('NumPy:', numpy.__version__)" 2>nul || echo NumPy: 未安装
python -c "import sympy; print('SymPy:', sympy.__version__)" 2>nul || echo SymPy: 未安装
python -c "import json; print('JSON: 内置模块')" 2>nul || echo JSON: 错误
python -c "import re; print('RE: 内置模块')" 2>nul || echo RE: 错误
echo.

echo ========================================
echo 项目目录结构:
echo   src\fortran\  - Fortran 源代码
echo   src\python\   - Python 转换代码
echo   backups\      - 备份文件
echo   docs\         - 文档和论文资料
echo ========================================
echo.
echo 提示：运行以下命令安装必要的包:
echo   pip install numpy sympy
echo.
