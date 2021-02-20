import math


def calc_deviation_from_north(x_coordinate: float, y_coordinate: float) -> float:
    if not (x_coordinate or y_coordinate):
        raise Exception("The vector formed by the x and y coordinates must not be zero vector.")

    return ((math.atan2(x_coordinate, y_coordinate) * 180 / math.pi) + 360) % 360
