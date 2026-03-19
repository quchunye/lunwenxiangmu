import socket
import json

def create_blue_house():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        print("✅ 连接到 Blender MCP 服务器成功！")
        
        code = """
import bpy

# 清除现有对象
for obj in bpy.data.objects:
    obj.select_set(True)
bpy.ops.object.delete()

# 创建房子主体（墙壁）
bpy.ops.mesh.primitive_cube_add(size=4, location=(0, 0, 2))
house_body = bpy.context.active_object
house_body.scale = (1, 1, 0.8)
house_body.name = "房子主体"

# 创建屋顶（三角形屋顶）
bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=2.5, depth=3, location=(0, 0, 4.2))
roof = bpy.context.active_object
roof.rotation_euler = (0, 0, 0.523599)
roof.scale = (1.2, 1.2, 0.8)
roof.name = "屋顶"

print("创建了房子！")
"""
        
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        
        sock.sendall(json.dumps(command).encode('utf-8'))
        print(f"📤 发送命令: 创建蓝色的房子")
        
        response = sock.recv(8192)
        print(f"📥 收到响应: {response.decode('utf-8')}")
        
        sock.close()
        print("\n🎉 成功！检查 Blender 中应该有一个房子了！")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_blue_house()
