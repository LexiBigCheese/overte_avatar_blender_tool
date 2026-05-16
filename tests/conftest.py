"""
Test setup. The add-on imports `bpy` and `mathutils` at module load, neither of
which exist outside Blender, so we install minimal stand-ins in sys.modules
before the package is ever imported. Anything the operator/panel classes touch
at *class* time (like bpy.props.EnumProperty as a descriptor, or the metaclass
on bpy.types.Operator) needs a believable stub here; runtime-only bpy access
(bpy.ops.armature.calculate_roll, vertex_groups, etc.) doesn't.
"""
import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _install_fake_bpy():
    bpy = types.ModuleType("bpy")
    bpy.types = types.ModuleType("bpy.types")
    bpy.props = types.ModuleType("bpy.props")
    bpy.ops = types.SimpleNamespace(armature=types.SimpleNamespace(calculate_roll=lambda **kw: None))
    bpy.utils = types.ModuleType("bpy.utils")
    bpy.data = types.SimpleNamespace(armatures=[])

    class _PropertyStub:
        def __init__(self, **kw):
            self.kw = kw

    bpy.props.EnumProperty = _PropertyStub
    bpy.props.BoolProperty = _PropertyStub
    bpy.props.StringProperty = _PropertyStub
    bpy.props.FloatProperty = _PropertyStub
    bpy.props.IntProperty = _PropertyStub

    class Operator:
        pass
    class Panel:
        pass
    class AddonPreferences:
        pass
    class Bone:
        pass
    class Context:
        pass
    class Menu:
        pass
    bpy.types.Operator = Operator
    bpy.types.Panel = Panel
    bpy.types.AddonPreferences = AddonPreferences
    bpy.types.Bone = Bone
    bpy.types.Context = Context
    bpy.types.Menu = Menu
    bpy.types.VIEW3D_MT_edit_armature = types.SimpleNamespace(append=lambda f: None,remove=lambda f: None)
    bpy.context = types.SimpleNamespace(window_manager=types.SimpleNamespace(keyconfigs=types.SimpleNamespace(addon=None)))

    def _register_classes_factory(classes):
        return (lambda: None, lambda: None)
    bpy.utils.register_classes_factory = _register_classes_factory

    sys.modules["bpy"] = bpy
    sys.modules["bpy.types"] = bpy.types
    sys.modules["bpy.props"] = bpy.props
    sys.modules["bpy.utils"] = bpy.utils

    mathutils = types.ModuleType("mathutils")
    class Vector:
        def __init__(self, xyz):
            self.x, self.y, self.z = xyz
        def __add__(self, other):
            return Vector((self.x + other.x, self.y + other.y, self.z + other.z))
        @property
        def length(self):
            return (self.x * self.x + self.y * self.y + self.z * self.z) ** 0.5
    mathutils.Vector = Vector
    sys.modules["mathutils"] = mathutils


_install_fake_bpy()
