from typing import Union

x_coordinate: Union[float, None]
y_coordinate: Union[float, None]


def set_coordinates(x: Union[float, None], y: Union[float, None]) -> None:
    global x_coordinate, y_coordinate
    x_coordinate = x
    y_coordinate = y


def get_coordinates() -> tuple[Union[float, None], Union[float, None]]:
    return x_coordinate, y_coordinate


def is_setpoint_exist() -> bool:
    if x_coordinate and y_coordinate:
        return True

    return False
