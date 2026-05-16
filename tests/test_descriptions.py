from overte_avatar_blender_tool import Matcher, rules, DESCRIPTIONS, enum_callback
from tests.fakes import FakeArmatureObject, FakeContext, build_tree


def test_desc_method_is_fluent_and_sets_description():
    m = Matcher().desc("the chest bone")
    assert m.description == "the chest bone"


def test_default_description_is_empty():
    assert Matcher().description == ""


def test_descriptions_table_propagated_to_rules():
    assert rules["Hips"].description == DESCRIPTIONS["Hips"]
    assert rules["Spine2"].description == "Chest (upper spine)"
    assert rules["LeftHand"].description.startswith("Left hand")


def test_finger_descriptions_distinguish_joints():
    base = "LeftHandThumb"
    assert "base" in rules[base + "1"].description.lower()
    assert "tip" in rules[base + "3"].description.lower()


def test_enum_callback_uses_description():
    # Set up an armature with a root bone of unknown name so the candidate
    # set is just root rules (Hips), then verify the description shows up
    # in the enum tuple.
    bones = build_tree(("something", []))
    arm = FakeArmatureObject(bones)
    active = arm.data.edit_bones["something"]
    ctx = FakeContext(arm, active_bone=active)
    entries = enum_callback(None, ctx)
    assert entries == [("Hips", "Hips", rules["Hips"].description)]


def test_enum_callback_falls_back_when_description_is_empty():
    # Set a description to empty temporarily and verify the fallback fires.
    rules["Hips"].description = ""
    try:
        bones = build_tree(("foo", []))
        arm = FakeArmatureObject(bones)
        active = arm.data.edit_bones["foo"]
        ctx = FakeContext(arm, active_bone=active)
        entries = enum_callback(None, ctx)
        assert entries[0][2] == "Rename to Hips"
    finally:
        rules["Hips"].description = DESCRIPTIONS["Hips"]
