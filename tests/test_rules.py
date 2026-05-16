from overte_avatar_blender_tool import rules, ROLL_AXIS


def test_hips_is_root_required():
    hips = rules["Hips"]
    assert hips.parent == []
    assert hips.optional is False
    assert hips.roll == "YNeg"


def test_spine_chain_parents():
    assert rules["Spine"].parent == ["Hips"]
    assert rules["Spine1"].parent == ["Spine"]
    assert rules["Spine1"].optional is True
    assert rules["Spine2"].parent == ["Spine", "Spine1"]
    assert rules["Neck"].parent == ["Spine2"]
    assert rules["Head"].parent == ["Neck"]
    assert rules["HeadTop_End"].optional is True


def test_eye_bones_have_callback_and_head_parent():
    for side in ("Left", "Right"):
        eye = rules[side + "Eye"]
        assert eye.parent == ["Head"]
        assert eye.roll == "YNeg"
        assert eye.callback is not None


def test_arm_chain_is_required():
    for side in ("Left", "Right"):
        for bone in (side + "Shoulder", side + "Arm", side + "ForeArm", side + "Hand"):
            assert rules[bone].optional is False, bone
            assert rules[bone].roll == "ZNeg", bone


def test_finger_chains_are_optional():
    for side in ("Left", "Right"):
        for finger in ("Thumb", "Index", "Middle", "Ring", "Pinky"):
            base = side + "Hand" + finger
            assert rules[base + "1"].parent == [side + "Hand"]
            for joint in (base + "1", base + "2", base + "3", base + "4"):
                assert rules[joint].optional is True, joint


def test_leg_chain_is_required():
    # Regression test: UpLeg / Leg / Foot were originally marked optional=True
    for side in ("Left", "Right"):
        for bone in (side + "UpLeg", side + "Leg", side + "Foot"):
            assert rules[bone].optional is False, bone
        assert rules[side + "UpLeg"].parent == ["Hips"]
        assert rules[side + "UpLeg"].roll == "YNeg"
        assert rules[side + "Leg"].parent == [side + "UpLeg"]
        assert rules[side + "Foot"].parent == [side + "Leg"]
        assert rules[side + "Foot"].roll == "YPos"


def test_toes_remain_optional():
    for side in ("Left", "Right"):
        assert rules[side + "ToeBase"].optional is True
        assert rules[side + "Toe_End"].optional is True
        assert rules[side + "ToeBase"].parent == [side + "Foot"]
        assert rules[side + "Toe_End"].parent == [side + "ToeBase"]


def test_roll_axis_table_covers_all_literals():
    assert set(ROLL_AXIS) == {"YNeg", "YPos", "ZNeg", "ZPos"}
    # Every roll value used by any rule must be mappable
    for name, m in rules.items():
        if m.roll is not None:
            assert m.roll in ROLL_AXIS, name
