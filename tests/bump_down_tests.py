import pytest

import config

config.step = 2
config.gap = 4

config.max = 80
config.min = 60

import nest_utils
from tests import test_utils

from nest import nest


@pytest.mark.parametrize("target,temperature,expected", [
    # if nothing on, turn ac on
    (nest.LowHighTuple(68, 72), 70, (nest.LowHighTuple(70 - config.step - config.gap,
                                                       70 - config.step))),
    (nest.LowHighTuple(68, 69 + config.step + config.gap + 1), 69 + config.step + config.gap,
      nest.LowHighTuple(68, 69 + config.gap)),
    # if ac running, no-op
    (nest.LowHighTuple(66, 70), 72,
      nest.LowHighTuple(66, 70)),
    # if heat on, turn off
    (nest.LowHighTuple(66, 70), 64,
      nest.LowHighTuple(64 -  config.step, 70)),
])
def test_BumpDown_with_dual(target, temperature, expected):
    device = test_utils.setup_dual_mock_device(target, temperature)

    nest_utils._bump_down(device)

    assert device.target == expected

@pytest.mark.parametrize("target,temperature,expected", [
    # if nothing on, no-op
    (68, 70, 68),
    # if heat on, turn off
    (70, 68, 68 - config.step),
])
def test_BumpDown_with_single_mode_heat(target, temperature, expected):
    device = test_utils.setup_single_mock_device(target, temperature, nest_utils.DeviceModes.heat)

    nest_utils._bump_down(device)

    assert device.target == expected


@pytest.mark.parametrize("target,temperature,expected", [
    # if nothing on, turn ac on
    (70, 68, 68 - config.step),
    # if ac on, no-op
    (70, 72, 70),
])
def test_BumpDown_with_single_mode_ac(target, temperature, expected):
    device = test_utils.setup_single_mock_device(target, temperature, nest_utils.DeviceModes.cool)

    nest_utils._bump_down(device)

    assert device.target == expected


if __name__ == '__main__':
    import unitTestHelper
    unitTestHelper.main(__file__)


