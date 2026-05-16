from overte_avatar_blender_tool import collect_possible_renames
from tests.fakes import FakeArmatureObject, FakeContext, build_tree


def _ctx(bones, active_name):
    armature = FakeArmatureObject(bones)
    active = armature.data.edit_bones[active_name]
    return FakeContext(armature, active_bone=active)


def test_root_bone_offers_root_rules():
    bones = build_tree(("root_thing", []))
    ctx = _ctx(bones, "root_thing")
    # Only Hips has no parent, so it's the only "root" candidate
    assert collect_possible_renames(ctx) == ["Hips"]


def test_known_bone_only_offers_itself():
    bones = build_tree(("Hips", [("Spine", [])]))
    ctx = _ctx(bones, "Hips")
    assert collect_possible_renames(ctx) == ["Hips"]


def test_child_of_hips_offers_spine_and_uplegs():
    bones = build_tree(("Hips", [("nameless", [])]))
    ctx = _ctx(bones, "nameless")
    candidates = set(collect_possible_renames(ctx))
    # Spine is the obvious one, but UpLeg is also parented to Hips
    assert "Spine" in candidates
    assert "LeftUpLeg" in candidates
    assert "RightUpLeg" in candidates
    # Things parented elsewhere should not show up
    assert "Neck" not in candidates


def test_already_used_target_is_excluded():
    bones = build_tree(("Hips", [("Spine", []), ("nameless", [])]))
    ctx = _ctx(bones, "nameless")
    candidates = collect_possible_renames(ctx)
    # Spine already exists in the armature; it should not be offered again
    assert "Spine" not in candidates


def test_hand_offers_fingers_and_arm_continuation():
    # The hand should be a parent target for finger roots
    bones = build_tree(("LeftHand", [("scrambled", [])]))
    ctx = _ctx(bones, "scrambled")
    candidates = set(collect_possible_renames(ctx))
    assert "LeftHandThumb1" in candidates
    assert "LeftHandPinky1" in candidates
