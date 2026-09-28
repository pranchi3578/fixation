"""
The tabletop: render settings, paper materials, the two lights every shot
is allowed (one warm practical, one cool ambient), and a camera.

Units are metres; a Doubtling is about 5 cm tall, so the set is a tabletop
and the lens behaves like a macro on a copy stand.
"""

import math
import os

import bpy

TEX = os.path.join(os.path.dirname(__file__), "..", "build", "tex")


def reset(samples=64, res=(1080, 1080), fps=24):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.device = "CPU"
    s.cycles.samples = samples
    s.cycles.use_denoising = True
    s.cycles.denoiser = "OPENIMAGEDENOISE"
    s.cycles.max_bounces = 6
    s.cycles.transmission_bounces = 4
    s.render.resolution_x, s.render.resolution_y = res
    s.render.resolution_percentage = 100
    s.render.fps = fps
    s.render.film_transparent = False
    s.view_settings.view_transform = "AgX"
    s.view_settings.look = "AgX - Medium High Contrast"
    s.render.image_settings.file_format = "PNG"
    s.render.threads_mode = "AUTO"
    return s


def paper_material(stock, name=None, translucency=0.25, bump=0.15,
                   roughness=0.85):
    """Paper: diffuse with a little light through it, and tooth for bump."""
    name = name or stock
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.blend_method = "HASHED"
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    col = nt.nodes.new("ShaderNodeTexImage")
    col.image = bpy.data.images.load(os.path.join(TEX, f"{stock}_col.png"),
                                     check_existing=True)
    col.interpolation = "Cubic"
    hgt = nt.nodes.new("ShaderNodeTexImage")
    hgt.image = bpy.data.images.load(os.path.join(TEX, f"{stock}_hgt.png"),
                                     check_existing=True)
    hgt.image.colorspace_settings.name = "Non-Color"
    bmp = nt.nodes.new("ShaderNodeBump")
    bmp.inputs["Strength"].default_value = bump
    bmp.inputs["Distance"].default_value = 0.0004
    nt.links.new(hgt.outputs["Color"], bmp.inputs["Height"])

    diff = nt.nodes.new("ShaderNodeBsdfPrincipled")
    diff.inputs["Roughness"].default_value = roughness
    diff.inputs["Specular IOR Level"].default_value = 0.2
    nt.links.new(col.outputs["Color"], diff.inputs["Base Color"])
    nt.links.new(bmp.outputs["Normal"], diff.inputs["Normal"])
    tr = nt.nodes.new("ShaderNodeBsdfTranslucent")
    nt.links.new(col.outputs["Color"], tr.inputs["Color"])
    nt.links.new(bmp.outputs["Normal"], tr.inputs["Normal"])
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs["Fac"].default_value = translucency
    nt.links.new(diff.outputs[0], mix.inputs[1])
    nt.links.new(tr.outputs[0], mix.inputs[2])

    # torn edges: alpha cuts the sheet
    transp = nt.nodes.new("ShaderNodeBsdfTransparent")
    cut = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(col.outputs["Alpha"], cut.inputs["Fac"])
    nt.links.new(transp.outputs[0], cut.inputs[1])
    nt.links.new(mix.outputs[0], cut.inputs[2])
    nt.links.new(cut.outputs[0], out.inputs["Surface"])
    return m


def flat_material(name, rgb, emission=0.0, roughness=0.6):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*rgb, 1)
    p.inputs["Roughness"].default_value = roughness
    if emission:
        p.inputs["Emission Color"].default_value = (*rgb, 1)
        p.inputs["Emission Strength"].default_value = emission
    return m


def tabletop(stock="card_4", size=1.2):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    t = bpy.context.object
    t.name = "tabletop"
    t.data.materials.append(paper_material(stock, translucency=0.0,
                                           bump=0.25))
    return t


def ambient(rgb=(0.35, 0.45, 0.65), strength=0.25):
    """The cool fill: night through a window."""
    w = bpy.data.worlds.new("world")
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*rgb, 1)
    bg.inputs["Strength"].default_value = strength
    return w


def practical(loc=(0.18, -0.12, 0.28), energy=6.0, size=0.05,
              kelvin_rgb=(1.0, 0.72, 0.42), name="lamp"):
    """The warm key: a desk lamp, small and close, so shadows are hard-ish."""
    d = bpy.data.lights.new(name, "AREA")
    d.energy = energy
    d.size = size
    d.color = kelvin_rgb
    o = bpy.data.objects.new(name, d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    aim(o, (0, 0, 0.01))
    return o


def camera(loc=(0, -0.32, 0.2), target=(0, 0, 0.015), lens=60,
           fstop=4.0, focus=None):
    c = bpy.data.cameras.new("cam")
    c.lens = lens
    c.sensor_width = 36
    c.dof.use_dof = True
    c.dof.aperture_fstop = fstop
    o = bpy.data.objects.new("cam", c)
    bpy.context.collection.objects.link(o)
    o.location = loc
    aim(o, target)
    c.dof.focus_distance = focus or math.dist(loc, target)
    bpy.context.scene.camera = o
    return o


def aim(obj, target):
    from mathutils import Vector
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def render_still(path):
    s = bpy.context.scene
    s.render.filepath = os.path.abspath(path)
    bpy.ops.render.render(write_still=True)
