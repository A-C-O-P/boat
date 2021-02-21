import math
from typing import Final

SPEED_DELTA: Final[float] = 0.001
RESISTANCE_SPEED: Final[float] = 0.0005
MAX_ABSOLUTE_SPEED: Final[float] = 0.5

x_coordinate: float
y_coordinate: float
boat_speed: float = 0


def init_coordinates(init_x_coordinate: float, init_y_coordinate: float) -> None:
    global x_coordinate, y_coordinate
    x_coordinate = init_x_coordinate
    y_coordinate = init_y_coordinate


def get_current_coordinates() -> tuple[float, float]:
    return x_coordinate, y_coordinate


def get_current_speed() -> float:
    return round(boat_speed, 3)


def go_ahead() -> None:
    global boat_speed, y_coordinate

    if math.isclose(boat_speed, 0) or abs(boat_speed) < RESISTANCE_SPEED:
        boat_speed = 0
        return

    if boat_speed > 0:
        boat_speed -= RESISTANCE_SPEED
    else:
        boat_speed += RESISTANCE_SPEED

    y_coordinate += boat_speed


def increase_speed() -> None:
    global boat_speed

    if math.isclose(boat_speed, MAX_ABSOLUTE_SPEED):
        return

    boat_speed += SPEED_DELTA


def decrease_speed() -> None:
    global boat_speed

    if math.isclose(abs(boat_speed), MAX_ABSOLUTE_SPEED):
        return

    boat_speed -= SPEED_DELTA


def move_left() -> None:
    global x_coordinate
    x_coordinate -= 0.5


def move_right() -> None:
    global x_coordinate
    x_coordinate += 0.5
