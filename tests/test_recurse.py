from overte_avatar_blender_tool import recurse_test
from tests.fakes import FakeBone


def test_returns_none_for_none():
    assert recurse_test(None) is None


def test_returns_bone_when_name_is_in_rules():
    hips = FakeBone("Hips")
    assert recurse_test(hips) is hips


def test_walks_up_to_first_known_ancestor():
    hips = FakeBone("Hips")
    junk = FakeBone("nonsense_a", parent=hips)
    deeper = FakeBone("nonsense_b", parent=junk)
    assert recurse_test(deeper) is hips


def test_returns_none_when_no_ancestor_is_known():
    a = FakeBone("foo")
    b = FakeBone("bar", parent=a)
    assert recurse_test(b) is None


def test_cycle_terminates():
    # Construct a parent cycle: a -> b -> a. The original code's comment
    # admitted "May endless loop if bone loops exist, whoops!"
    a = FakeBone("foo")
    b = FakeBone("bar", parent=a)
    a.parent = b
    assert recurse_test(b) is None
