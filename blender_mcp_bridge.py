#!/usr/bin/env python3
import socket
import json
import sys
import os
from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio

app = Server("blender-mcp-bridge")

def send_to_blender(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9876))
    sock.sendall(json.dumps(command).encode('utf-8'))
    response = sock.recv(8192)
    sock.close()
    return json.loads(response.decode('utf-8'))

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_scene_info",
            description="获取当前 Blender 场景信息",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="execute_code",
            description="在 Blender 中执行 Python 代码",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "要执行的 Python 代码"
                    }
                },
                "required": ["code"]
            },
        ),
        Tool(
            name="create_cube",
            description="创建一个立方体",
            inputSchema={
                "type": "object",
                "properties": {
                    "size": {
                        "type": "number",
                        "description": "立方体大小",
                        "default": 2
                    },
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "位置 [x, y, z]",
                        "default": [0, 0, 0]
                    }
                },
            },
        ),
        Tool(
            name="create_sphere",
            description="创建一个球体",
            inputSchema={
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "number",
                        "description": "球体半径",
                        "default": 1
                    },
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "位置 [x, y, z]",
                        "default": [0, 0, 0]
                    }
                },
            },
        ),
        Tool(
            name="create_cylinder",
            description="创建一个圆柱体",
            inputSchema={
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "number",
                        "description": "半径",
                        "default": 1
                    },
                    "depth": {
                        "type": "number",
                        "description": "高度",
                        "default": 2
                    },
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "位置 [x, y, z]",
                        "default": [0, 0, 0]
                    }
                },
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "get_scene_info":
            result = send_to_blender({"type": "get_scene_info"})
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "execute_code":
            code = arguments.get("code", "")
            result = send_to_blender({"type": "execute_code", "params": {"code": code}})
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "create_cube":
            size = arguments.get("size", 2)
            loc = arguments.get("location", [0, 0, 0])
            code = f"""
import bpy
bpy.ops.mesh.primitive_cube_add(size={size}, location=({loc[0]}, {loc[1]}, {loc[2]}))
obj = bpy.context.active_object
print(f"创建了立方体: {{obj.name}}")
"""
            result = send_to_blender({"type": "execute_code", "params": {"code": code}})
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "create_sphere":
            radius = arguments.get("radius", 1)
            loc = arguments.get("location", [0, 0, 0])
            code = f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(radius={radius}, location=({loc[0]}, {loc[1]}, {loc[2]}))
obj = bpy.context.active_object
print(f"创建了球体: {{obj.name}}")
"""
            result = send_to_blender({"type": "execute_code", "params": {"code": code}})
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "create_cylinder":
            radius = arguments.get("radius", 1)
            depth = arguments.get("depth", 2)
            loc = arguments.get("location", [0, 0, 0])
            code = f"""
import bpy
bpy.ops.mesh.primitive_cylinder_add(radius={radius}, depth={depth}, location=({loc[0]}, {loc[1]}, {loc[2]}))
obj = bpy.context.active_object
print(f"创建了圆柱体: {{obj.name}}")
"""
            result = send_to_blender({"type": "execute_code", "params": {"code": code}})
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"错误: {str(e)}")]

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    print("🎮 Blender MCP Bridge 启动中...", file=sys.stderr)
    try:
        asyncio.run(stdio_server(app))
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
