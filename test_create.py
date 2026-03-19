import socket
import json

def test_create():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        print("✅ 连接到 Blender MCP 服务器成功！")
        
        code = """
import bpy
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
print("创建了立方体")
"""
        
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        
        sock.sendall(json.dumps(command).encode('utf-8'))
        print(f"📤 发送命令")
        
        response = sock.recv(8192)
        print(f"📥 收到响应：{response.decode('utf-8')}")
        
        sock.close()
        return True
    except Exception as e:
        print(f"❌ 失败：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_create()
