#!/usr/bin/env python3
import sys
import os
import asyncio
import logging

# 设置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('d:\\Trae CN\\论文\\blender_mcp.log', encoding='utf-8'),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

logger.info("🎮 Blender MCP Bridge 启动中...")
logger.info(f"项目路径：{project_root}")

try:
    from blender_mcp_bridge import app
    from mcp.server.stdio import stdio_server
    
    logger.info("✅ 模块加载成功")
    logger.info("🚀 启动 MCP 服务器...")
    
    asyncio.run(stdio_server(app))
except Exception as e:
    logger.error(f"❌ 错误：{e}", exc_info=True)
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
