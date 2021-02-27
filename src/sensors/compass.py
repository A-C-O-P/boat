import math

from src.gui import boat


def get_deviation_from_north() -> float:
    boat_x_direction_vector, boat_y_direction_vector = get_direction_vector()
    deviation_angle = math.degrees(
        math.atan2(
            boat_x_direction_vector, boat_y_direction_vector
        )
    )

    return (deviation_angle + 360) % 360  # math.atan2() returns angle [-180; +180]


def get_direction_vector() -> tuple[float, float]:
    return boat.get_direction_vector()
