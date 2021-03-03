import math
from typing import Final

UPDATE_INTERVAL_TIME: Final[float] = 0.01

VELOCITY_PROPORTIONAL_GAIN: Final[float] = 0.60
VELOCITY_INTEGRAL_GAIN: Final[float] = 0.00022
VELOCITY_DERIVATIVE_GAIN: Final[float] = 0.36

DEGREE_PROPORTIONAL_GAIN: Final[float] = 1.8
DEGREE_INTEGRAL_GAIN: Final[float] = 0.003
DEGREE_DERIVATIVE_GAIN: Final[float] = 1.20

VELOCITY_WINDUP_GUARD: Final[float] = 95.0
DEGREE_WINDUP_GUARD: Final[float] = 25.0

""" Global variables """
prev_deviation_from_course = 0.0
prev_distance_to_target = 0.0
prev_output_value: tuple[float, float] = 0.0, 0.0

velocity_integral_term: list[float] = [0.0]
degree_integral_term: list[float] = [0.0]

current_velocity_integral_gain: float = VELOCITY_INTEGRAL_GAIN
current_degree_integral_gain: float = DEGREE_INTEGRAL_GAIN


def update_pid(delta_time: float, deviation_from_course: float, distance_to_target: float) -> tuple[float, float]:
    """
    Corrects the boat path

    deviation_from_course: float - deviation in degrees from the course
    distance_to_target: float - distance to boat target
    pid() -> tuple[float, float] (boat velocity, steering wheel degree)
    """
    global prev_deviation_from_course
    global prev_distance_to_target
    global prev_output_value

    global velocity_integral_term
    global degree_integral_term

    global current_velocity_integral_gain
    global current_degree_integral_gain

    print(f"DISTANCE ERROR: {distance_to_target}")
    print(f"DEVIATION ERROR: {deviation_from_course}")

    delta_deviation_from_course = deviation_from_course - prev_deviation_from_course
    delta_distance_to_target = distance_to_target - prev_distance_to_target

    if delta_time < UPDATE_INTERVAL_TIME:
        return prev_output_value

    boat_velocity = calculate_pid_output(
        VELOCITY_PROPORTIONAL_GAIN,
        current_velocity_integral_gain,
        VELOCITY_DERIVATIVE_GAIN,
        velocity_integral_term,
        delta_time,
        distance_to_target,
        delta_distance_to_target
    )

    print(f"BOAT VELOCITY before WINDUP GUARD: {boat_velocity}")

    limited_boat_velocity = apply_windup_guard(boat_velocity, VELOCITY_WINDUP_GUARD)

    if not math.isclose(boat_velocity, limited_boat_velocity) \
            and ((boat_velocity > 0) == (distance_to_target > 0)):
        current_velocity_integral_gain = 0
    else:
        current_velocity_integral_gain = VELOCITY_INTEGRAL_GAIN

    steering_wheel_angle = calculate_pid_output(
        DEGREE_PROPORTIONAL_GAIN,
        DEGREE_INTEGRAL_GAIN,
        DEGREE_DERIVATIVE_GAIN,
        degree_integral_term,
        delta_time,
        deviation_from_course,
        delta_deviation_from_course
    )

    limited_steering_wheel_angle = apply_windup_guard(steering_wheel_angle, DEGREE_WINDUP_GUARD)

    if not math.isclose(steering_wheel_angle, limited_steering_wheel_angle) \
            and ((steering_wheel_angle > 0) == (deviation_from_course > 0)):
        current_degree_integral_gain = 0
    else:
        current_degree_integral_gain = DEGREE_INTEGRAL_GAIN

    prev_deviation_from_course = deviation_from_course
    prev_distance_to_target = distance_to_target
    prev_output_value = limited_boat_velocity, steering_wheel_angle

    return limited_boat_velocity, limited_steering_wheel_angle


def calculate_pid_output(proportional_gain: float, integral_gain: float, derivative_gain: float,
                         integral_term: list[float], delta_time: float,
                         error: float, delta_error: float) -> float:
    proportional_term = proportional_gain * error
    integral_term[0] += error * delta_time

    derivative_term = derivative_gain * (delta_error / delta_time)

    return proportional_term + integral_gain * integral_term[0] + derivative_term


# Integral windup: https://youtu.be/NVLXCwc8HzM?t=200
def apply_windup_guard(calculated_value: float, windup_guard_value: float) -> float:
    if calculated_value > windup_guard_value:
        return windup_guard_value
    elif calculated_value < -windup_guard_value:
        return -windup_guard_value
    else:
        return calculated_value


def reset_pid() -> None:
    global prev_deviation_from_course
    global prev_distance_to_target
    global prev_output_value
    global velocity_integral_term
    global degree_integral_term
    global current_velocity_integral_gain

    prev_deviation_from_course = 0.0
    prev_distance_to_target = 0.0
    prev_output_value = 0.0, 0.0

    velocity_integral_term = [0.0]
    degree_integral_term = [0.0]

    current_velocity_integral_gain = VELOCITY_INTEGRAL_GAIN
