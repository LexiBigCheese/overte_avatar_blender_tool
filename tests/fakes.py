"""Small fakes for the bits of Blender state our pure-logic tests need."""
from types import SimpleNamespace


class FakeBone:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.use_connect = True
        self.color = SimpleNamespace(palette=None)
        if parent is not None:
            parent.children.append(self)


class FakeVertexGroup:
    def __init__(self, name):
        self.name = name


class FakeMesh:
    def __init__(self, vg_names=()):
        self.vertex_groups = [FakeVertexGroup(n) for n in vg_names]


class FakeEditBones(dict):
    """Behaves like Blender's edit_bones collection (dict-like + .active).

    In real Blender, iterating edit_bones yields bone objects, not keys, so
    override __iter__ to match.
    """
    def __init__(self, bones):
        super().__init__({b.name: b for b in bones})
        self.active = None

    def __iter__(self):
        return iter(self.values())

    def get(self, key, default=None):
        return super().get(key, default)


class FakeArmatureData:
    def __init__(self, bones):
        self.edit_bones = FakeEditBones(bones)


class FakeArmatureObject:
    type = "ARMATURE"
    def __init__(self, bones, meshes=()):
        self.data = FakeArmatureData(bones)
        self.children = list(meshes)
        self.vertex_groups = []  # armatures don't really have these


class FakeContext:
    def __init__(self, armature, active_bone=None, scene_objects=None):
        self.active_object = armature
        self.active_bone = active_bone
        self.scene = SimpleNamespace(objects=scene_objects or [armature])


def build_tree(spec, parent=None, out=None):
    """spec = ("name", [child_spec, ...]); returns flat list of FakeBones."""
    if out is None:
        out = []
    name, children = spec
    bone = FakeBone(name, parent=parent)
    out.append(bone)
    for child in children:
        build_tree(child, parent=bone, out=out)
    return out
