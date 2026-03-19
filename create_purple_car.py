import socket
import json

def create_purple_car():
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

# 创建紫色材质
material = bpy.data.materials.new(name="紫色材质")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# 清除默认节点
for node in nodes:
    nodes.remove(node)

# 创建新节点
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.inputs['Base Color'].default_value = (0.6, 0.2, 0.8, 1)  # 紫色
bsdf.inputs['Roughness'].default_value = 0.3
output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# 应用材质到车身
if car_body.data.materials:
    car_body.data.materials[0] = material
else:
    car_body.data.materials.append(material)

# 创建车顶
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, 1.1))
car_roof = bpy.context.active_object
car_roof.scale = (1.2, 0.8, 0.3)
car_roof.name = "车顶"

# 应用材质到车顶
if car_roof.data.materials:
    car_roof.data.materials[0] = material
else:
    car_roof.data.materials.append(material)

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
    
    # 创建黑色轮胎材质
    tire_material = bpy.data.materials.new(name=f"轮胎材质_{i+1}")
    tire_material.use_nodes = True
    tire_nodes = tire_material.node_tree.nodes
    tire_links = tire_material.node_tree.links
    
    for node in tire_nodes:
        tire_nodes.remove(node)
    
    tire_bsdf = tire_nodes.new(type='ShaderNodeBsdfPrincipled')
    tire_bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)  # 黑色
    tire_output = tire_nodes.new(type='ShaderNodeOutputMaterial')
    tire_links.new(tire_bsdf.outputs['BSDF'], tire_output.inputs['Surface'])
    
    if wheel.data.materials:
        wheel.data.materials[0] = tire_material
    else:
        wheel.data.materials.append(tire_material)

print("创建了一辆紫色的汽车！")
"""
        
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        
        sock.sendall(json.dumps(command).encode('utf-8'))
        print(f"📤 发送命令: 创建紫色汽车")
        
        response = sock.recv(8192)
        print(f"📥 收到响应: {response.decode('utf-8')}")
        
        sock.close()
        print("\n🎉 成功！检查 Blender 中应该有一辆紫色的汽车了！")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_purple_car()
