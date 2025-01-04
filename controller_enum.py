from enum import Enum

class Steering(Enum):
    LEFT = "a"
    RIGHT = "d"


class Speed(Enum):
    ACCELERATION = "w"
    BRAKE = "s"
