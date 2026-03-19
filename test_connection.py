#!/usr/bin/env python3
import socket
import json
import sys

def test_connection():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        print("✅ 成功连接到 Blender MCP 服务器！")
        
        command = {
            "type": "get_scene_info"
        }
        
        sock.sendall(json.dumps(command).encode('utf-8'))
        print(f"📤 发送命令: {command}")
        
        response = sock.recv(8192)
        result = json.loads(response.decode('utf-8'))
        print(f"📥 收到响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        sock.close()
        return True
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_connection()
