# In the boat movement logic the zero coordinate is in the lower left corner,
#   but the pygame zero coordinate is in the upper left corner
def convert_coordinates(coordinates: tuple[float, float], y_window_size: int) -> tuple[float, float]:
    return coordinates[0], y_window_size - coordinates[1]


# Because of the different position of the zero coordinate, we need to transform the angle
def convert_angle(angle: float) -> float:
    return -angle
