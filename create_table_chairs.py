import socket
import json

def create_table_and_chairs():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        print("✅ 连接到 Blender MCP 服务器成功！")
        
        code = """
import bpy
import math

# 清除现有对象
for obj in bpy.data.objects:
    obj.select_set(True)
bpy.ops.object.delete()

# 创建桌子桌面
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.0))
table_top = bpy.context.active_object
table_top.scale = (1.5, 1, 0.1)
table_top.name = "桌面"

# 创建桌腿
leg_height = 1.0
leg_radius = 0.05
leg_positions = [
    (-1.3, -0.8, leg_height/2),
    (1.3, -0.8, leg_height/2),
    (-1.3, 0.8, leg_height/2),
    (1.3, 0.8, leg_height/2)
]

for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=leg_radius, depth=leg_height, location=pos)
    leg = bpy.context.active_object
    leg.name = f"桌腿_{i+1}"

# 创建椅子（4把）
chair_positions = [
    (-2.5, 0, 0),
    (2.5, 0, 0),
    (0, -1.8, 0),
    (0, 1.8, 0)
]

chair_rotations = [0, math.pi, math.pi/2, -math.pi/2]

for chair_idx, (pos, rot) in enumerate(zip(chair_positions, chair_rotations)):
    # 椅子座位
    seat_pos = (pos[0], pos[1], 0.3)
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=seat_pos)
    seat = bpy.context.active_object
    seat.scale = (0.5, 0.5, 0.08)
    seat.rotation_euler = (0, 0, rot)
    seat.name = f"椅子_{chair_idx+1}_座位"
    
    # 椅子靠背
    back_pos = (
        pos[0] - 0.2 * math.sin(rot),
        pos[1] + 0.2 * math.cos(rot),
        0.65
    )
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=back_pos)
    back = bpy.context.active_object
    back.scale = (0.5, 0.08, 0.6)
    back.rotation_euler = (0, 0, rot)
    back.name = f"椅子_{chair_idx+1}_靠背"
    
    # 椅子腿
    chair_leg_positions = [
        (-0.18, -0.18, 0.15),
        (0.18, -0.18, 0.15),
        (-0.18, 0.18, 0.15),
        (0.18, 0.18, 0.15)
    ]
    
    for leg_idx, leg_pos in enumerate(chair_leg_positions):
        # 旋转椅子腿位置
        x = leg_pos[0] * math.cos(rot) - leg_pos[1] * math.sin(rot)
        y = leg_pos[0] * math.sin(rot) + leg_pos[1] * math.cos(rot)
        
        leg_final_pos = (pos[0] + x, pos[1] + y, leg_pos[2])
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.3, location=leg_final_pos)
        chair_leg = bpy.context.active_object
        chair_leg.name = f"椅子_{chair_idx+1}_腿_{leg_idx+1}"

print("创建了桌子和4把椅子！")
"""
        
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        
        sock.sendall(json.dumps(command).encode('utf-8'))
        print(f"📤 发送命令: 创建桌子和椅子")
        
        response = sock.recv(8192)
        print(f"📥 收到响应: {response.decode('utf-8')}")
        
        sock.close()
        print("\n🎉 成功！检查 Blender 中应该有桌子和椅子了！")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_table_and_chairs()
