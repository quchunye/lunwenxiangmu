import socket
import json

def create_car():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        print("✅ 连接到 Blender MCP 服务器成功！")
        
        code = """
import bpy
import math

# 创建车身
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5))
car_body = bpy.context.active_object
car_body.scale = (2, 1, 0.4)
car_body.name = "车身"

# 创建车顶
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, 1.1))
car_roof = bpy.context.active_object
car_roof.scale = (1.2, 0.8, 0.3)
car_roof.name = "车顶"

# 创建车轮
wheel_radius = 0.35
wheel_depth = 0.2
wheel_positions = [
    (-1.5, -0.8, 0.35),
    (1.5, -0.8, 0.35),
    (-1.5, 0.8, 0.35),
    (1.5, 0.8, 0.35)
]

for i, pos in enumerate(wheel_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=wheel_radius, depth=wheel_depth, location=pos)
    wheel = bpy.context.active_object
    wheel.rotation_euler = (math.pi/2, 0, 0)
    wheel.name = f"车轮_{i+1}"

print("创建了一辆简单的汽车！")
"""
        
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        
        sock.sendall(json.dumps(command).encode('utf-8'))
        print(f"📤 发送命令: 创建汽车")
        
        response = sock.recv(8192)
        print(f"📥 收到响应: {response.decode('utf-8')}")
        
        sock.close()
        print("\n🎉 成功！检查 Blender 中应该有一辆汽车了！")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_car()
