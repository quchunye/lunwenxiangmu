#!/usr/bin/env python
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blender_mcp_bridge import app
from mcp.server.stdio import stdio_server
import asyncio

if __name__ == "__main__":
    print("🎮 Blender MCP Bridge 启动中...", file=sys.stderr)
    try:
        asyncio.run(stdio_server(app))
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
