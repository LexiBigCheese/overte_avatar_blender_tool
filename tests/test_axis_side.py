from overte_avatar_blender_tool import axis_side


def test_positive_x_is_left():
    assert axis_side(1.0) == "left"


def test_negative_x_is_right():
    assert axis_side(-1.0) == "right"


def test_origin_is_center():
    assert axis_side(0.0) == "center"


def test_within_default_epsilon_is_center():
    assert axis_side(1e-7) == "center"
    assert axis_side(-1e-7) == "center"


def test_just_outside_default_epsilon_picks_a_side():
    assert axis_side(1e-5) == "left"
    assert axis_side(-1e-5) == "right"


def test_configurable_epsilon_widens_centerline():
    # With eps=0.01, anything within ±0.01 should be center
    assert axis_side(0.005, eps=0.01) == "center"
    assert axis_side(-0.005, eps=0.01) == "center"
    assert axis_side(0.02, eps=0.01) == "left"
    assert axis_side(-0.02, eps=0.01) == "right"


def test_zero_epsilon_treats_origin_only_as_center():
    assert axis_side(0.0, eps=0.0) == "center"
    assert axis_side(1e-12, eps=0.0) == "left"
