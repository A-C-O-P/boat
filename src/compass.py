import math


def calc_deviation_from_north(x_coordinate: float, y_coordinate: float) -> float:
    return (math.degrees(math.atan2(x_coordinate, y_coordinate)) + 360) % 360
