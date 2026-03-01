@echo off
REM ========================================
REM Fortran 编译器环境配置脚本
REM 论文项目：Fortran 到 Python 自动转换
REM ========================================

set PATH=C:\msys64\mingw64\bin;%PATH%
set MSYS2_PATH=C:\msys64\mingw64

echo ========================================
echo Fortran 编译环境已配置
echo ========================================
gfortran --version 2>nul | findstr /C:"GNU Fortran"
echo.
echo 使用方法:
echo   1. 编译 Fortran 程序：gfortran program.f90 -o program.exe
echo   2. 运行程序：program.exe
echo   3. 编译并优化：gfortran -O2 program.f90 -o program.exe
echo   4. 调试模式：gfortran -g program.f90 -o program.exe
echo.
echo 项目目录结构:
echo   src\fortran\  - Fortran 源代码
echo   src\python\   - Python 转换代码
echo   backups\      - 备份文件
echo   docs\         - 文档和论文资料
echo ========================================
