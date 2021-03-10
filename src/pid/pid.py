import math
from typing import Final

UPDATE_INTERVAL_TIME: Final[float] = 0.01

VELOCITY_PROPORTIONAL_GAIN: Final[float] = 0.60
VELOCITY_INTEGRAL_GAIN: Final[float] = 0.00022
VELOCITY_DERIVATIVE_GAIN: Final[float] = 0.36

DEGREE_PROPORTIONAL_GAIN: Final[float] = 1.8
DEGREE_INTEGRAL_GAIN: Final[float] = 0.003
DEGREE_DERIVATIVE_GAIN: Final[float] = 1.20

MAX_VELOCITY_VALUE: Final[float] = 95.0
MAX_ANGLE_VALUE: Final[float] = 25.0

WINDUP_GUARD: Final[float] = 1

""" Global variables """
prev_deviation_from_course = 0.0
prev_distance_to_target = 0.0
prev_output_value: tuple[float, float] = 0.0, 0.0

velocity_integral_term: list[float] = [0.0]
degree_integral_term: list[float] = [0.0]

current_velocity_integral_gain: list[float] = [VELOCITY_INTEGRAL_GAIN]
current_degree_integral_gain: list[float] = [DEGREE_INTEGRAL_GAIN]


def update_pid(delta_time: float, deviation_from_course: float, distance_to_target: float) -> tuple[float, float]:
    """
    Corrects the boat path

    deviation_from_course: float - deviation in degrees from the course
    distance_to_target: float - distance to boat target
    pid() -> tuple[float, float] (boat velocity, steering wheel degree)
    """
    global prev_distance_to_target
    global prev_deviation_from_course
    global prev_output_value

    print(f"DISTANCE ERROR: {distance_to_target}")
    print(f"DEVIATION ERROR: {deviation_from_course}")

    delta_distance_to_target = distance_to_target - prev_distance_to_target
    delta_deviation_from_course = deviation_from_course - prev_deviation_from_course

    if delta_time < UPDATE_INTERVAL_TIME:
        return prev_output_value

    output_boat_velocity = calculate_pid_output(
        VELOCITY_PROPORTIONAL_GAIN,
        current_velocity_integral_gain,
        VELOCITY_DERIVATIVE_GAIN,
        velocity_integral_term,
        delta_time,
        distance_to_target,
        delta_distance_to_target,
        MAX_VELOCITY_VALUE,
        VELOCITY_INTEGRAL_GAIN
    )

    output_steering_wheel_angle = calculate_pid_output(
        DEGREE_PROPORTIONAL_GAIN,
        current_degree_integral_gain,
        DEGREE_DERIVATIVE_GAIN,
        degree_integral_term,
        delta_time,
        deviation_from_course,
        delta_deviation_from_course,
        MAX_ANGLE_VALUE,
        DEGREE_INTEGRAL_GAIN
    )

    print(
        f"PID output:"
        f"\n\tVelocity: {output_boat_velocity}"
        f"\n\tAngle: {output_steering_wheel_angle}"
    )
    output_value = output_boat_velocity, output_steering_wheel_angle

    prev_distance_to_target = distance_to_target
    prev_deviation_from_course = deviation_from_course
    prev_output_value = output_value

    return output_value


def calculate_pid_output(proportional_gain: float, integral_gain: list[float], derivative_gain: float,
                         integral_term: list[float], delta_time: float, error: float, delta_error: float,
                         max_value: float, integral_gain_constant: float) -> float:
    pid_output = calculate_normalized_pid_output(
        proportional_gain,
        integral_gain[0],
        derivative_gain,
        integral_term,
        delta_time,
        error,
        delta_error,
        max_value
    )

    limited_pid_output = apply_windup_guard(pid_output)

    if not math.isclose(pid_output, limited_pid_output) and pid_output > 0 and error > 0:
        integral_gain[0] = 0
    else:
        integral_gain[0] = integral_gain_constant

    return limited_pid_output


def calculate_normalized_pid_output(proportional_gain: float, integral_gain: float, derivative_gain: float,
                                    integral_term: list[float], delta_time: float,
                                    error: float, delta_error: float, max_value: float) -> float:
    proportional_term = proportional_gain * error
    integral_term[0] += error * delta_time
    derivative_term = derivative_gain * (delta_error / delta_time)

    pid_output = proportional_term + integral_gain * integral_term[0] + derivative_term

    return normalize_pid_output(pid_output, max_value)


def normalize_pid_output(pid_output: float, max_value: float) -> float:
    return pid_output / max_value


# Integral windup: https://youtu.be/NVLXCwc8HzM?t=200
def apply_windup_guard(pid_output: float) -> float:
    if pid_output > WINDUP_GUARD:
        return WINDUP_GUARD
    elif pid_output < -WINDUP_GUARD:
        return -WINDUP_GUARD
    else:
        return pid_output


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

    current_velocity_integral_gain = [VELOCITY_INTEGRAL_GAIN]
