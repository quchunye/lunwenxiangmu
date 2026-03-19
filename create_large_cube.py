import socket
import json

def create_large_cube():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        print("✅ 连接到 Blender MCP 服务器成功！")
        
        code = """
import bpy

# 创建一个很大的立方体
bpy.ops.mesh.primitive_cube_add(size=5, location=(0, 0, 0))

# 获取新创建的对象
cube = bpy.context.active_object
print(f"创建了立方体: {cube.name}, 大小: 5")
"""
        
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        
        sock.sendall(json.dumps(command).encode('utf-8'))
        print(f"📤 发送命令: 创建大立方体")
        
        response = sock.recv(8192)
        print(f"📥 收到响应: {response.decode('utf-8')}")
        
        sock.close()
        print("\n🎉 成功！检查 Blender 中应该有一个大立方体了！")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_large_cube()
