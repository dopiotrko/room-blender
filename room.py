import bpy
from math import radians as rad

def chanel(chanel_id='RGBA'):
    chanels = {'RGBA', 'RGB', 'ALPHA'}
    if chanel_id not in chanels:
        raise ValueError('Chanel id must be one of ' + chanels)
    for object in bpy.data.scenes['Scene'].objects: 
        if object.type == 'MESH':
            if chanel_id == 'RGBA':
                object.hide_render = False
            elif chanel_id == 'RGB':
                object.hide_render = object.active_material.use_transparency
            elif chanel_id == 'ALPHA':
                object.hide_render = not object.active_material.use_transparency

def make_transparent(material, colour, transparency):                
    material.use_nodes = True
    material_nodes = material.node_tree.nodes
    diff_n = material_nodes.get('Diffuse BSDF')
    out_n = material_nodes.get('Material Output')
    mix_n = material_nodes.new('ShaderNodeMixShader')
    transparent_n = material_nodes.new("ShaderNodeBsdfTransparent")
    diff_n.inputs[0].default_value = colour
    mix_n.inputs[0].default_value = transparency
    material.node_tree.links.new(out_n.inputs[0], mix_n.outputs[0])
    material.node_tree.links.new(mix_n.inputs[1], diff_n.outputs[0])
    material.node_tree.links.new(mix_n.inputs[2], transparent_n.outputs[0])
        
for object in bpy.data.scenes['Scene'].objects: 
    if object.name == 'Camera':
        camera = object
    elif object.name == 'Lamp':
        lamp = object
    else:
        bpy.data.objects.remove(object) 
        
for material in bpy.data.materials:       
    bpy.data.materials.remove(material) 
    
lamp.location = (-3, 0, 2.2)

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.cycles.film_transparent = True

bpy.ops.mesh.primitive_cube_add()
blat = bpy.context.object
blat.scale[2] = .03
blat.location = (0, 0, 1)

wood_material = bpy.data.materials.new(name='wood')
blat.data.materials.append( wood_material )
blat.active_material.diffuse_color = (0.12, 0.06, 0)
legs =[]

for i in range(4):
    bpy.ops.mesh.primitive_cube_add()
    legs.append( bpy.context.object )
    legs[i].scale = (.03, .03, .5)
    legs[i].data.materials.append( wood_material )
    
legs[0].location = (-.95, -.95, .5)    
legs[1].location = (.95, .95, .5)
legs[2].location = (-.95, .95, .5)
legs[3].location = (.95, -.95, .5)

bpy.ops.mesh.primitive_monkey_add(radius=.2, location=(0.3, -0.3, 1.23))
monkey = bpy.context.object
m_material = bpy.data.materials.new(name='monkey_skin')
monkey.data.materials.append( m_material )
monkey.active_material.diffuse_color = (0.4, 0.2, 0)
monkey.rotation_euler[2] = -0.785398

bpy.ops.mesh.primitive_cylinder_add(radius=.15, depth=.4, location=(-0.3, 0.3, 1.23))
vase = bpy.context.object
glass = bpy.data.materials.new(name='glass')
vase.data.materials.append( glass )
vase.active_material.use_transparency = True
make_transparent(glass, (1, 1, 0, 1), .8)

bpy.ops.mesh.primitive_plane_add(radius=1, location=(-2, 0, 0) )
floor = bpy.context.object
floor.scale = (4, 2.5, 0)
floor_material = bpy.data.materials.new(name='floor')
floor.data.materials.append( floor_material )
floor.active_material.diffuse_color = (0.2, 0.2, 0.2)

bpy.ops.mesh.primitive_plane_add(radius=1, location=(-2, 2.5, 1.25) )
wall_N = bpy.context.object
wall_N.scale = (4, 1.25, 0)
wall_N.rotation_euler = (rad(90), 0, 0)
wall_SN_material = bpy.data.materials.new(name='wall_SN')
wall_N.data.materials.append( wall_SN_material )
wall_N.active_material.diffuse_color = (0.021089, 0.183035, 0.2)
wall_N.active_material.raytrace_mirror.reflect_factor = 0.1

bpy.ops.mesh.primitive_plane_add(radius=1, location=(-2, -2.5, 1.25) )
wall_N = bpy.context.object
wall_N.scale = (4, 1.25, 0)
wall_N.rotation_euler = (rad(90), 0, 0)
wall_N.data.materials.append( wall_SN_material )

bpy.ops.mesh.primitive_plane_add(radius=1, location=(-6, 0, 1.25) )
wall_W = bpy.context.object
wall_W.scale = (1.25, 2.5, 0)
wall_W.rotation_euler = (0, rad(90), 0)
wall_WE_material = bpy.data.materials.new(name='wall_WE')
wall_W.data.materials.append( wall_WE_material )
wall_W.active_material.diffuse_color = (0.0746483, 0.2, 0.0418606)

bpy.ops.mesh.primitive_plane_add(radius=1, location=(2, 0, 1.25) )
wall_E = bpy.context.object
wall_E.scale = (1.25, 2.5, 0)
wall_E.rotation_euler = (0, rad(90), 0)
wall_E.data.materials.append( wall_WE_material )

bpy.ops.mesh.primitive_plane_add(radius=1, location=(-2, 0, 2.5) )
ceiling = bpy.context.object
ceiling.scale = (4, 2.5, 0)
ceiling_material = bpy.data.materials.new(name='ceiling')
ceiling.data.materials.append( ceiling_material )
ceiling.active_material.diffuse_color = (1, 1, 1)

camera.location = (-5.98, -2, 2.15)
camera.rotation_euler = ( rad(78.), 0, rad(-68.))


chanel('RGBA')
bpy.data.scenes['Scene'].render.filepath = 'd:/blender/room/room_RGB.png'
bpy.ops.render.render( write_still=True ) 
                   
chanel('RGB')
bpy.data.scenes['Scene'].render.filepath = 'd:/blender/room/room1_RGB.png'
bpy.ops.render.render( write_still=True ) 

chanel('ALPHA')
bpy.data.scenes['Scene'].render.filepath = 'd:/blender/room/room1_Alpha.png'
bpy.ops.render.render( write_still=True ) 

chanel('ALPHA')
camera.location = (-2.27, -1.14, 2.15)
camera.rotation_euler = ( rad(60.), 0, rad(-68.))

bpy.data.scenes['Scene'].render.filepath = 'd:/blender/room/room2_Alpha.png'
bpy.ops.render.render( write_still=True ) 

chanel('RGB')
bpy.data.scenes['Scene'].render.filepath = 'd:/blender/room/room2_RGB.png'
bpy.ops.render.render( write_still=True ) 
