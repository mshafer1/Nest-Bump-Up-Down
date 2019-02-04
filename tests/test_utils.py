import nest_utils
from tests import test_mocks


def _set_device_state_dual(device, target, temperature):
    if temperature < target[0] :
        device.hvac_state = nest_utils.DeviceStates.heat.value
    elif temperature > target[1]:
        device.hvac_state = nest_utils.DeviceStates.cool.value
    else:
        device.hvac_state = nest_utils.DeviceStates.off.value


def _set_device_state_single(device, target, temperature, mode):
    if mode == nest_utils.DeviceModes.heat.value and temperature < target :
        device.hvac_state = nest_utils.DeviceStates.heat.value
    elif mode == nest_utils.DeviceModes.cool.value and temperature > target:
        device.hvac_state = nest_utils.DeviceStates.cool.value
    else:
        device.hvac_state = nest_utils.DeviceStates.off.value


def setup_dual_mock_device(target, temperature):
    device = test_mocks.Device()
    device.mode = nest_utils.DeviceModes.heat_cool.value
    device.temperature = temperature
    _set_device_state_dual(device, target, temperature)
    device.target = target
    return device


def setup_single_mock_device(target, temperature, mode):
    device = test_mocks.Device()
    device.mode = mode
    device.temperature = temperature
    _set_device_state_single(device, target, temperature, mode)
    device.target = target
    return device

