@echo off
chcp 65001 >nul
echo CAJ to PDF Converter
echo ====================
echo.

python -m pip install --upgrade pip -q 2>nul
python -m pip install PyPDF2 imagesize -q 2>nul

python caj_converter.py

pause
