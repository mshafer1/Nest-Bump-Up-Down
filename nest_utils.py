from builtins import min, max, abs, input

from enum import Enum

import nest
import config


import os

_base_dir = os.path.dirname(os.path.relpath(__file__))


def _get_auth():
    if _get_auth._auth:
        return
    file_path = config.access_token_cache_file \
        if os.path.isabs(config.access_token_cache_file) \
        else os.path.join(_base_dir, config.access_token_cache_file)

    with nest.Nest(client_id=config.client_id, client_secret=config.client_secret,
                   access_token_cache_file=file_path) as napi:
        if napi.authorization_required:
            print('Go to ' + napi.authorize_url + ' to authorize, then enter PIN below')
            pin = input("PIN: ")
            napi.request_token(pin)
        _get_auth._auth = True
_get_auth._auth = None


class DeviceModes(Enum):
    heat_cool = 'heat-cool'
    heat = 'heat'
    cool = 'cool'


class DeviceStates(Enum):
    off = 'off'
    heat = 'heating'
    cool = 'cooling'


def _range_shift(range, distance, gap):
    '''Perform the desired shift on the range - adjusting either the top or the bottom or both

    :param range: tuple (bottom, top) of current values to shift
    :param distance: how far to shift (positive causes the bottom to shift up, negative shifts the top down)
    :param gap: minimum gap between top and bottom to maintain
    :return: tuple (bottom, top) after shifting

    >>> _range_shift((68, 70), 2, 4)
    (70, 74)
    >>> _range_shift((68, 70), -2, 4)
    (64, 68)
    '''
    if distance > 0:
        bottom = min((range[0] + distance), config.max) # go up distance, but don't cross 80
        top = max(range[1], bottom + gap)  # keep the top unless needing to shift up to keep {gap} degree distance
    else:
        top = max(range[1] - abs(distance), config.min)
        bottom = min(range[0], top - gap)
    return bottom, top


def _set_bottom(device, target):
    mode = DeviceModes(device.mode)
    current_target = device.target

    if mode is DeviceModes.heat_cool:
        bottom = min(target, config.max)  # go up to target, but don't cross max
        # keep the top unless needing to shift up to keep {gap} degree distance
        top = max(current_target.high, bottom + config.gap)
        new_target = (bottom, top)
    elif mode is DeviceModes.heat or mode is DeviceModes.cool:
        new_target = min((target), config.max) # go up to target, but don't cross max
    else:
        new_target = current_target
    device.target = new_target


def _set_top(device, target):
    mode = DeviceModes(device.mode)
    current_target = device.target

    if mode is DeviceModes.heat_cool:
        top = max(target, config.min)  # go up to target, but don't cross max
        # keep the bottom unless needing to shift up to keep {gap} degree distance
        bottom = min(current_target.low, top - config.gap)
        new_target = (bottom, top)
    elif mode is DeviceModes.heat or mode is DeviceModes.cool:
        new_target = max((target), config.min)  # go to target, but don't cross min
    else:
        new_target = current_target
    device.target = new_target


def _bump_up(device):
    current_temp = device.temperature

    state = DeviceStates(device.hvac_state)
    if state is DeviceStates.heat:
        # raise target temp or No-op?
        pass
    elif state is DeviceStates.off:
        # get current, raise target to current + step
        _set_bottom(device, current_temp + config.step)
    elif state is DeviceStates.cool:
        # raise target temp
        _set_top(device, current_temp + config.step)


def _bump_down(device):
    current_temp = device.temperature

    state = DeviceStates(device.hvac_state)
    if state is DeviceStates.cool:
        # No-op
        pass
    elif state is DeviceStates.off:
        # get current, lower target to current - step
        _set_top(device, current_temp - config.step)
    elif state is DeviceStates.heat:
        # lower target temp
        _set_bottom(device, current_temp - config.step)

def _list():
    _get_auth()
    with nest.Nest(client_id=config.client_id, client_secret=config.client_secret,
                   access_token_cache_file=config.access_token_cache_file) as napi:
        for therm in napi.thermostats:
            print(therm.name)


def bump_up():
    _get_auth()
    with nest.Nest(client_id=config.client_id, client_secret=config.client_secret,
                   access_token_cache_file=config.access_token_cache_file) as napi:
        if config.affect_all:
            for device in napi.thermostats:
                _bump_up(device)
        else:
            device = [therm for therm in napi.thermostats if therm.name == config.device_name][0]
            _bump_up(device)


def bump_down():
    _get_auth()
    with nest.Nest(client_id=config.client_id, client_secret=config.client_secret,
                   access_token_cache_file=config.access_token_cache_file) as napi:
        if config.affect_all:
            for device in napi.thermostats:
                _bump_down(device)
        else:
            device = [therm for therm in napi.thermostats if therm.name == config.device_name][0]
            _bump_down(device)


def set_fan(time=15):
    _get_auth()
    with nest.Nest(client_id=config.client_id, client_secret=config.client_secret,
                   access_token_cache_file=config.access_token_cache_file) as napi:
        if config.affect_all:
            for device in napi.thermostats:
                device.fan_timer = time
                device.fan = True
        else:
            device = [therm for therm in napi.thermostats if therm.name == config.device_name][0]
            device.fan_timer = time
            device.fan = True
