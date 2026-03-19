#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Blender 快速创建工具
使用方法：直接运行这个脚本，然后在 Blender 中查看结果
"""

import socket
import json
import sys

def send_command(code):
    """发送代码到 Blender 执行"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        
        command = {
            "type": "execute_code",
            "params": {"code": code}
        }
        
        sock.sendall(json.dumps(command).encode('utf-8'))
        response = sock.recv(8192)
        sock.close()
        
        result = json.loads(response.decode('utf-8'))
        if result.get('status') == 'success':
            print(f"✅ 成功：{result.get('result', {}).get('result', '完成')}")
            return True
        else:
            print(f"❌ 失败：{result.get('message', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 连接失败：{e}")
        print("请确保 Blender 正在运行且 BlenderMCP 插件已启动")
        return False

def create_cube():
    """创建立方体"""
    code = """
import bpy
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
print("创建了立方体")
"""
    send_command(code)

def create_sphere():
    """创建球体"""
    code = """
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
print("创建了球体")
"""
    send_command(code)

def create_car():
    """创建汽车"""
    code = """
import bpy
import math

# 车身
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5))
car_body = bpy.context.active_object
car_body.scale = (2, 1, 0.4)
car_body.name = "车身"

# 车顶
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, 1.1))
car_roof = bpy.context.active_object
car_roof.scale = (1.2, 0.8, 0.3)
car_roof.name = "车顶"

# 车轮
wheel_positions = [(-1.5, -0.8, 0.35), (1.5, -0.8, 0.35), (-1.5, 0.8, 0.35), (1.5, 0.8, 0.35)]
for i, pos in enumerate(wheel_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=0.2, location=pos)
    wheel = bpy.context.active_object
    wheel.rotation_euler = (math.pi/2, 0, 0)
    wheel.name = f"车轮_{i+1}"

print("创建了汽车")
"""
    send_command(code)

def main():
    print("=" * 50)
    print("🎨 Blender 快速创建工具")
    print("=" * 50)
    print("请选择要创建的对象：")
    print("1. 立方体")
    print("2. 球体")
    print("3. 汽车")
    print("4. 自定义代码")
    print("0. 退出")
    print("=" * 50)
    
    while True:
        choice = input("请输入选项 (0-4): ").strip()
        
        if choice == '0':
            print("再见！")
            break
        elif choice == '1':
            create_cube()
        elif choice == '2':
            create_sphere()
        elif choice == '3':
            create_car()
        elif choice == '4':
            print("请输入 Python 代码（输入 END 结束）：")
            lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            code = '\n'.join(lines)
            send_command(code)
        else:
            print("无效的选项，请重新输入")

if __name__ == "__main__":
    main()
