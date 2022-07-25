from dataclasses import dataclass
from enum import Enum

from ftd2xx import FTD2XX
from ftd2xx import _ftd2xx as _ft

nm = float  # nanometer

SCALE_FACTOR = 64 / 450  # steps per nm


class Axis(Enum):
    X = 1
    Y = 2
    Z = 3


@dataclass
class PositionCounters:
    x: int
    y: int
    z: int

    def update_relative(self, axis: Axis, steps: int) -> None:
        if axis == Axis.X:
            self.x += steps
        elif axis == Axis.Y:
            self.y += steps
        elif axis == Axis.Z:
            self.z += steps
        else:
            raise ValueError

    def update_absolute(self, axis: Axis, position: int) -> None:
        if axis == Axis.X:
            self.x = position
        elif axis == Axis.Y:
            self.y = position
        elif axis == Axis.Z:
            self.z = position
        else:
            raise ValueError


class MechonicsStage(FTD2XX):

    def __init__(self, handle: _ft.FT_HANDLE):
        super().__init__(handle)
        self.position_counters = PositionCounters(0, 0, 0)

    def nm_to_steps(self, pos_nm: float) -> int:
        return round(pos_nm * SCALE_FACTOR)  # SCALE_FACTOR is given by CF-30 controller

    def move_to_relative_position(self, axis: Axis, velocity: int, distance: nm):
        steps = self.nm_to_steps(distance)  # moving by a distance that is given in nm, needs converting
        s = f'PM,{axis.value},{velocity},{steps}\r'
        data = bytes(s, encoding='utf-8')
        self.purge()
        self.write(data)
        self.position_counters.update_relative(axis, steps)

    def move_to_absolute_position(self, axis: Axis, velocity: int, position_nm: nm):
        position = self.nm_to_steps(position_nm)  # moving to a position that is given in nm, needs converting
        s = f'PA,{axis.value},{velocity},{position}\r'
        data = bytes(s, encoding='utf-8')
        self.purge()
        self.write(data)
        self.position_counters.update_absolute(axis, position)

    def move_single_step(self, axis: Axis, direction: int):
        if direction in {0, 1}:
            s = f'PS,{axis.value},{direction}\r'
            data = bytes(s, encoding='utf-8')
            self.purge()
            self.write(data)
        else:
            print('Given direction is not valid')

    def set_speed(self, axis: Axis, velocity: int):
        s = f'PV,{axis.value},{velocity}\r'
        data = bytes(s, encoding='utf-8')
        self.purge()
        self.write(data)

    def set_ramp(self, axis: Axis, ramp: int):
        s = f'SR,{axis.value},{ramp}\r'
        data = bytes(s, encoding='utf-8')
        self.purge()
        self.write(data)

    def set_counter(self, axis: Axis, counter: int):
        s = f'SC,{axis.value},{counter},\r'
        data = bytes(s, encoding='utf-8')
        self.purge()
        self.write(data)

    def ioctl(self):
        pass

