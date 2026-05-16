from overte_avatar_blender_tool import is_flow_chain_root, validate_flow_chains
from tests.fakes import FakeArmatureObject, build_tree


def _eb(bones):
    return FakeArmatureObject(bones).data.edit_bones


def test_chain_root_detection():
    assert is_flow_chain_root("flow_tail_1") is True
    assert is_flow_chain_root("flow_tail_2") is False
    assert is_flow_chain_root("Hips") is False
    assert is_flow_chain_root("flow_") is False  # missing trailing _1


def test_well_formed_chain_has_no_errors():
    bones = build_tree((
        "flow_tail_1",
        [("flow_tail_2", [("flow_tail_3", [])])],
    ))
    assert validate_flow_chains(_eb(bones)) == []


def test_chain_with_wrong_parent_is_flagged():
    # flow_tail_2 parented to flow_tail_1 is correct; create flow_tail_3 with
    # the wrong parent.
    bones = build_tree(("flow_tail_1", [("flow_tail_2", [])]))
    # Manually add a flow_tail_3 parented to flow_tail_1 instead of _2
    from tests.fakes import FakeBone
    wrong = FakeBone("flow_tail_3", parent=bones[0])  # parented to _1
    bones.append(wrong)
    arm = FakeArmatureObject(bones)
    errors = validate_flow_chains(arm.data.edit_bones)
    assert any("flow_tail_3" in e and "flow_tail_2" in e for e in errors)


def test_chain_with_orphan_link_is_flagged():
    # flow_tail_2 exists but is unparented entirely
    from tests.fakes import FakeBone
    a = FakeBone("flow_tail_1")
    b = FakeBone("flow_tail_2")  # no parent at all
    arm = FakeArmatureObject([a, b])
    errors = validate_flow_chains(arm.data.edit_bones)
    assert len(errors) == 1
    assert "flow_tail_2" in errors[0]


def test_multiple_chains_validated_independently():
    bones = build_tree((
        "flow_tail_1",
        [("flow_tail_2", [])],
    ))
    bones.extend(build_tree((
        "flow_ears_1",
        [("flow_ears_2", [("flow_ears_3", [])])],
    )))
    arm = FakeArmatureObject(bones)
    assert validate_flow_chains(arm.data.edit_bones) == []


def test_non_flow_bones_are_ignored():
    bones = build_tree(("Hips", [("Spine", [("Spine2", [])])]))
    assert validate_flow_chains(_eb(bones)) == []
