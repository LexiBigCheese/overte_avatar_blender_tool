from overte_avatar_blender_tool import Matcher


def test_default_state():
    m = Matcher()
    assert m.parent == []
    assert m.optional is False
    assert m.roll is None
    assert m.callback is None
    assert m.dead_end_return is None


def test_parents_stored_as_list():
    m = Matcher("A", "B")
    assert m.parent == ["A", "B"]
    # par() must work; previously this raised because parent was a tuple
    m.par("C")
    assert m.parent == ["A", "B", "C"]


def test_fluent_chain():
    m = Matcher("Hips").opt().yneg()
    assert m.parent == ["Hips"]
    assert m.optional is True
    assert m.roll == "YNeg"


def test_roll_setters_cover_all_four_axes():
    assert Matcher().yneg().roll == "YNeg"
    assert Matcher().ypos().roll == "YPos"
    assert Matcher().zneg().roll == "ZNeg"
    assert Matcher().zpos().roll == "ZPos"


def test_cback_and_returning_to():
    def cb(b, c, n):
        pass
    m = Matcher().cback(cb).returning_to("Hips")
    assert m.callback is cb
    assert m.dead_end_return == "Hips"
