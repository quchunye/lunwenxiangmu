@echo off
chcp 65001 >nul
echo 🎮 启动 Blender MCP Bridge...
echo 项目路径：%~dp0
cd /d "%~dp0"
python run_blender_mcp.py
pause
