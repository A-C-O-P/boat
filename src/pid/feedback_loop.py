import math

from src.pid import pid
from src.sensors import compass, gps
from src.utils import vector_utils

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


def calc_deviation_from_course() -> float:
    x_setpoint_direction_vector, y_setpoint_direction_vector = get_setpoint_direction_vector()

    return math.degrees(
        vector_utils.calc_angle_between_vectors(
            x_boat_direction_vector, y_boat_direction_vector,
            x_setpoint_direction_vector, y_setpoint_direction_vector
        )
    )


def get_setpoint_direction_vector() -> tuple[float, float]:
    return vector_utils.normalize_vector(x_setpoint - x_boat_center, y_setpoint - y_boat_center)


def calc_distance_to_target() -> float:
    distance = vector_utils.calc_distance_between_vectors(
        x_setpoint, x_boat_center,
        y_setpoint, y_boat_center
    )

    if is_setpoint_behind_boat():
        distance = -distance

    return distance


def is_setpoint_behind_boat() -> bool:
    x_between_setpoint_and_boat = x_setpoint - x_boat_center
    y_between_setpoint_and_boat = y_setpoint - y_boat_center

    dot_product = vector_utils.calc_dot_product_of_vectors(
        x_boat_direction_vector, x_between_setpoint_and_boat,
        y_boat_direction_vector, y_between_setpoint_and_boat
    )

    return dot_product < 0
