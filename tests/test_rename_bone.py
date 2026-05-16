from overte_avatar_blender_tool import rename_bone, rules
from tests.fakes import FakeArmatureObject, FakeContext, FakeMesh, build_tree


def test_vertex_groups_on_the_mesh_get_renamed():
    # Regression for the vertex-group bug: rename_bone used to iterate
    # the armature's vertex_groups (which don't exist) instead of the mesh's.
    bones = build_tree(("OldName", []))
    mesh = FakeMesh(vg_names=["OldName", "OtherGroup"])
    arm = FakeArmatureObject(bones, meshes=[mesh])
    ctx = FakeContext(arm, active_bone=bones[0])
    bone = arm.data.edit_bones["OldName"]

    rename_bone(bone, ctx, "Hips")

    assert bone.name == "Hips"
    assert {vg.name for vg in mesh.vertex_groups} == {"Hips", "OtherGroup"}


def test_rename_to_non_rule_skips_roll_and_callback():
    bones = build_tree(("foo", []))
    arm = FakeArmatureObject(bones, meshes=[FakeMesh()])
    ctx = FakeContext(arm, active_bone=bones[0])
    bone = arm.data.edit_bones["foo"]
    # flow_* names are not in rules; no callback or roll should fire and no
    # exception either
    rename_bone(bone, ctx, "flow_tail_1")
    assert bone.name == "flow_tail_1"


def test_rename_sets_color_palette():
    bones = build_tree(("anything", []))
    arm = FakeArmatureObject(bones, meshes=[FakeMesh()])
    ctx = FakeContext(arm, active_bone=bones[0])
    bone = arm.data.edit_bones["anything"]
    rename_bone(bone, ctx, "Hips")
    assert bone.color.palette == "THEME03"


def test_reparent_to_known_ancestor():
    # Selecting an UpLeg-shaped bone whose grandparent is Hips, with a random
    # parent in between, then renaming with reparent=True should hop the bone
    # up to Hips.
    bones = build_tree(("Hips", [("intermediate", [("scrambled", [])])]))
    arm = FakeArmatureObject(bones, meshes=[FakeMesh()])
    bone = arm.data.edit_bones["scrambled"]
    ctx = FakeContext(arm, active_bone=bone)

    rename_bone(bone, ctx, "LeftUpLeg", reparent=True)

    assert bone.name == "LeftUpLeg"
    assert bone.parent.name == "Hips"
    assert bone.use_connect is False


def test_reparent_root_unparents():
    # Renaming a child bone to Hips with reparent=True must actually drop the
    # parent link, since Hips is a root. The old code had a dead `is None`
    # branch that never executed.
    bones = build_tree(("some_root", [("the_one", [])]))
    arm = FakeArmatureObject(bones, meshes=[FakeMesh()])
    bone = arm.data.edit_bones["the_one"]
    ctx = FakeContext(arm, active_bone=bone)

    rename_bone(bone, ctx, "Hips", reparent=True)

    assert bone.parent is None
