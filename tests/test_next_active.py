from overte_avatar_blender_tool import next_active_after_rename, rules
from tests.fakes import FakeArmatureObject, build_tree


def _eb(bones):
    return FakeArmatureObject(bones).data.edit_bones


def test_jumps_to_sole_fresh_child():
    bones = build_tree(("Hips", [("nameless", [])]))
    eb = _eb(bones)
    hips = eb["Hips"]
    nxt = next_active_after_rename(hips, eb)
    assert nxt is eb["nameless"]


def test_skips_already_named_children_when_choosing():
    # Hand has 5 finger roots. After renaming 4 of them, only one remains
    # nameless. Logic should jump there, not get confused by siblings.
    bones = build_tree((
        "LeftHand",
        [
            ("LeftHandThumb1", []),
            ("LeftHandIndex1", []),
            ("LeftHandMiddle1", []),
            ("LeftHandRing1", []),
            ("scrambled_pinky", []),
        ],
    ))
    eb = _eb(bones)
    nxt = next_active_after_rename(eb["LeftHand"], eb)
    assert nxt is eb["scrambled_pinky"]


def test_multiple_fresh_children_no_jump():
    bones = build_tree(("LeftHand", [("a", []), ("b", [])]))
    eb = _eb(bones)
    nxt = next_active_after_rename(eb["LeftHand"], eb)
    assert nxt is None


def test_dead_end_returns_to_named_target():
    # Build a Hips with a LeftHand that has no fresh children. LeftHand's
    # rule should have dead_end_return = "Spine2", set during rule_chain build.
    bones = build_tree((
        "Hips",
        [
            ("Spine2", [
                ("LeftHand", []),
            ]),
        ],
    ))
    eb = _eb(bones)
    nxt = next_active_after_rename(eb["LeftHand"], eb)
    assert nxt is eb["Spine2"]


def test_dead_end_but_target_missing_returns_none():
    bones = build_tree(("LeftHand", []))
    eb = _eb(bones)
    # No Spine2 in this armature; dead_end_return refers to a missing bone
    assert next_active_after_rename(eb["LeftHand"], eb) is None


def test_foot_dead_end_returns_to_hips():
    # Regression for the explicit returning_to("Hips") added to the Foot rule
    assert rules["LeftFoot"].dead_end_return == "Hips"
    assert rules["RightFoot"].dead_end_return == "Hips"
