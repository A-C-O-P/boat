from typing import Final

STEP_SIZE: Final[int] = 10

x_coordinate: int
y_coordinate: int


def init_coordinates(init_x_coordinate: int, init_y_coordinate: int) -> None:
    global x_coordinate, y_coordinate

    x_coordinate = init_x_coordinate
    y_coordinate = init_y_coordinate


def get_current_coordinates() -> tuple[int, int]:
    return x_coordinate, y_coordinate


def turn_right() -> None:
    global x_coordinate
    x_coordinate += STEP_SIZE
