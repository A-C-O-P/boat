from typing import Final

CHANGE_SPEED_STEP: Final[float] = 0.0001
CHANGE_DIRECTION_STEP: Final[float] = 0.05
INITIAL_BOAT_SPEED: Final[float] = 0.05

x_coordinate: float
y_coordinate: float
boat_speed: float = INITIAL_BOAT_SPEED


def init_coordinates(init_x_coordinate: float, init_y_coordinate: float) -> None:
    global x_coordinate, y_coordinate
    x_coordinate = init_x_coordinate
    y_coordinate = init_y_coordinate


def get_current_coordinates() -> tuple[float, float]:
    return x_coordinate, y_coordinate


def go_ahead() -> None:
    global y_coordinate
    y_coordinate += boat_speed


def increase_speed() -> None:
    global boat_speed
    boat_speed += CHANGE_SPEED_STEP


def decrease_speed() -> None:
    global boat_speed
    boat_speed -= CHANGE_SPEED_STEP


def move_left() -> None:
    global x_coordinate
    x_coordinate -= CHANGE_DIRECTION_STEP


def move_right() -> None:
    global x_coordinate
    x_coordinate += CHANGE_DIRECTION_STEP
