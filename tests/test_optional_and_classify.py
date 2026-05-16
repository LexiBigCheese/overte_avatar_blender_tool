from overte_avatar_blender_tool import (
    effective_optional,
    is_toe_bone,
    classify_bones,
    rules,
)
from tests.fakes import FakeArmatureObject, build_tree


def test_is_toe_bone():
    assert is_toe_bone("LeftToeBase") is True
    assert is_toe_bone("RightToe_End") is True
    assert is_toe_bone("LeftFoot") is False
    assert is_toe_bone("Hips") is False


def test_effective_optional_default_passthrough():
    r = rules["LeftToeBase"]
    assert r.optional is True
    assert effective_optional(r, "LeftToeBase", toes_required=False) is True


def test_effective_optional_promotes_toes_when_required():
    r = rules["LeftToeBase"]
    assert effective_optional(r, "LeftToeBase", toes_required=True) is False


def test_effective_optional_leaves_non_toes_alone():
    # Spine1 is optional and is NOT a toe — the pref shouldn't touch it
    r = rules["Spine1"]
    assert r.optional is True
    assert effective_optional(r, "Spine1", toes_required=True) is True


def _eb(bones):
    return FakeArmatureObject(bones).data.edit_bones


def test_classify_bones_empty_armature_puts_hips_in_required_next():
    bones = build_tree(("nothing", []))
    eb = _eb(bones)
    errors, req_next, req_other, opt_next, opt_other = classify_bones(eb)
    assert "Hips" in req_next
    # nothing else has a parent that exists yet, so other root-able items
    # should land in *_otherwise
    assert "Spine" in req_other
    assert "LeftHand" in req_other
    assert errors == []


def test_classify_bones_progresses_after_hips_renamed():
    bones = build_tree(("Hips", []))
    eb = _eb(bones)
    errors, req_next, req_other, opt_next, opt_other = classify_bones(eb)
    assert "Spine" in req_next
    assert "LeftUpLeg" in req_next
    assert "Hips" not in req_next  # already present
    assert "Hips" not in req_other


def test_classify_flags_misparented_bone():
    # Make a Spine that's parented to nothing — should be flagged as needing
    # a Hips parent.
    from tests.fakes import FakeBone, FakeArmatureObject
    spine = FakeBone("Spine")
    arm = FakeArmatureObject([spine])
    errors, *_ = classify_bones(arm.data.edit_bones)
    assert any("Spine" in e and "parented" in e for e in errors)


def test_classify_with_toes_required_moves_toes_to_required_bucket():
    bones = build_tree((
        "Hips",
        [
            ("LeftUpLeg", [("LeftLeg", [("LeftFoot", [])])]),
        ],
    ))
    eb = _eb(bones)
    _, req_next_default, _, opt_next_default, _ = classify_bones(eb, toes_required=False)
    _, req_next_strict, _, opt_next_strict, _ = classify_bones(eb, toes_required=True)
    assert "LeftToeBase" in opt_next_default
    assert "LeftToeBase" not in req_next_default
    assert "LeftToeBase" in req_next_strict
    assert "LeftToeBase" not in opt_next_strict
