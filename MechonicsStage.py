import sys
from dataclasses import dataclass

import ftd2xx as ftd
from ftd2xx import defines, FTD2XX

SCALE_FACTOR = 64 / 450  # steps per nm


def nm_to_steps(pos_nm: float) -> int:
    return round(pos_nm * SCALE_FACTOR)


def move_to_relative_position(handle: FTD2XX, axis: int, velocity: int, distance_nm: float):
    steps = nm_to_steps(distance_nm)
    s = f'PM,{axis},{velocity},{steps}\r'
    data = bytes(s, encoding='utf-8')
    handle.purge()
    handle.write(data)


def move_to_absolute_position(handle: FTD2XX, axis: int, velocity: int, position_nm: float):
    position = nm_to_steps(position_nm)
    s = f'PA,{axis},{velocity},{position}\r'
    data = bytes(s, encoding='utf-8')
    handle.purge()
    handle.write(data)


def move_single_step(handle: FTD2XX, axis: int, direction: int):
    if direction in {0,1}:
        s = f'PS,{axis},{direction}\r'
        data = bytes(s, encoding='utf-8')
        handle.purge()
        handle.write(data)
    else:
        print('Given direction is not valid')


def set_speed(handle: FTD2XX, axis: int, velocity: int):
    s = f'PV,{axis},{velocity}\r'
    data = bytes(s, encoding='utf-8')
    handle.purge()
    handle.write(data)


def set_ramp(handle: FTD2XX, axis: int, ramp: int):
    s = f'SR,{axis},{ramp}\r'
    data = bytes(s, encoding='utf-8')
    handle.purge()
    handle.write(data)

handle = ftd.openEx(bytes('A000000', encoding='uft-8'))
move_to_relative_position(1,1000,-10000)
# print(d.getDeviceInfo())

