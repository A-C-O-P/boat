import math

from src.pid import pid
from src.sensors import gps, compass

x_setpoint: float
y_setpoint: float

x_boat_direction_vector: float
y_boat_direction_vector: float

x_boat_center: float
y_boat_center: float


def run_iteration(setpoint: tuple[float, float], delta_time: float) -> tuple[float, float]:
    global x_setpoint, y_setpoint
    global x_boat_direction_vector, y_boat_direction_vector
    global x_boat_center, y_boat_center

    x_setpoint, y_setpoint = setpoint
    x_boat_direction_vector, y_boat_direction_vector = compass.get_direction_vector()
    x_boat_center, y_boat_center = gps.get_boat_center_location()

    deviation_from_course = calc_deviation_from_course()
    distance_to_target = calc_distance_to_target()

    return pid.update_pid(delta_time, deviation_from_course, distance_to_target)


def calc_distance_to_target() -> float:
    return math.sqrt(
        math.pow(x_setpoint - x_boat_center, 2)
        + math.pow(y_setpoint - y_boat_center, 2)
    )


def calc_deviation_from_course() -> float:
    x_setpoint_direction_vector, y_setpoint_direction_vector = get_setpoint_direction_vector()

    return math.degrees(
        calc_angle_between_vectors(
            x_boat_direction_vector, y_boat_direction_vector,
            x_setpoint_direction_vector, y_setpoint_direction_vector
        )
    )


def get_setpoint_direction_vector() -> tuple[float, float]:
    return normalize_vector(x_setpoint - x_boat_center, y_setpoint - y_boat_center)


def normalize_vector(x_coordinate: float, y_coordinate: float) -> tuple[float, float]:
    vector_length = calc_vector_length(x_coordinate, y_coordinate)
    return x_coordinate / vector_length, y_coordinate / vector_length


def calc_vector_length(x_coordinate: float, y_coordinate: float) -> float:
    return math.sqrt(
        math.pow(x_coordinate, 2) + math.pow(y_coordinate, 2)
    )


# https://stackoverflow.com/a/45351293
def calc_angle_between_vectors(x_first_vector: float, y_first_vector: float,
                               x_second_vector: float, y_second_vector: float) -> float:
    first_vector_angle = math.atan2(y_first_vector, x_first_vector)
    second_vector_angle = math.atan2(y_second_vector, x_second_vector)

    angles_diff = second_vector_angle - first_vector_angle

    if angles_diff < -math.pi:
        angles_diff = 2 * math.pi - abs(angles_diff)
    elif angles_diff > math.pi:
        angles_diff = 2 * -math.pi + abs(angles_diff)

    return -angles_diff
