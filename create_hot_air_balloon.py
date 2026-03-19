import socket
import json

def create_red_hot_air_balloon():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        print("✅ 连接到 Blender MCP 服务器成功！")
        
        code = """
import bpy

# 创建热气球的气球部分（球体）
bpy.ops.mesh.primitive_uv_sphere_add(radius=2, location=(0, 0, 3))
balloon = bpy.context.active_object
balloon.name = "气球"

# 创建热气球的篮子（立方体）
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.5))
basket = bpy.context.active_object
basket.scale = (0.8, 0.8, 0.4)
basket.name = "篮子"

# 创建绳子（用小圆柱体）
import math
for i in range(4):
    angle = i * (math.pi / 2)
    x = math.cos(angle) * 1.5
    y = math.sin(angle) * 1.5
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=3.5, location=(x, y, 1))
    rope = bpy.context.active_object
    rope.rotation_euler = (math.pi/2, 0, angle)
    rope.name = f"绳子_{i+1}"

print("创建了红色热气球！")
"""
        
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        
        sock.sendall(json.dumps(command).encode('utf-8'))
        print(f"📤 发送命令: 创建红色热气球")
        
        response = sock.recv(8192)
        print(f"📥 收到响应: {response.decode('utf-8')}")
        
        sock.close()
        print("\n🎉 成功！检查 Blender 中应该有一个热气球了！")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_red_hot_air_balloon()
