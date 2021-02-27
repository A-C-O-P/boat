import time
from typing import Final

UPDATE_INTERVAL_TIME: Final[float] = 0.01

SPEED_PROPORTIONAL_GAIN: Final[float] = 1.2
SPEED_INTEGRAL_GAIN: Final[float] = 1.0
SPEED_DERIVATIVE_GAIN: Final[float] = 0.001

DEGREE_PROPORTIONAL_GAIN: Final[float] = 1.2
DEGREE_INTEGRAL_GAIN: Final[float] = 1.0
DEGREE_DERIVATIVE_GAIN: Final[float] = 0.001

""" Global variables """
prev_time = time.time()
prev_deviation_from_course = 0.0
prev_distance_to_target = 0.0
prev_output_value: tuple[float, float] = 0.0, 0.0

speed_integral_term: list[float] = [0.0]
degree_integral_term: list[float] = [0.0]


def update_pid(deviation_from_course: float, distance_to_target: float) -> tuple[float, float]:
    """
    Corrects the boat path

    deviation_from_course: float - deviation in degrees from the course
    distance_to_target: float - distance to boat target
    pid() -> tuple[float, float] (engine speed, steering wheel degree)
    """
    global prev_time
    global prev_deviation_from_course
    global prev_distance_to_target
    global prev_output_value

    global speed_integral_term
    global degree_integral_term

    current_time = time.time()

    delta_time = current_time - prev_time
    delta_deviation_from_course = deviation_from_course - prev_deviation_from_course
    delta_distance_to_target = distance_to_target - prev_distance_to_target

    if delta_time < UPDATE_INTERVAL_TIME:
        return prev_output_value

    engine_speed = calculate_pid_output(
        SPEED_PROPORTIONAL_GAIN,
        SPEED_INTEGRAL_GAIN,
        SPEED_DERIVATIVE_GAIN,
        speed_integral_term,
        delta_time,
        distance_to_target,
        delta_distance_to_target
    )

    steering_wheel_degree = calculate_pid_output(
        DEGREE_PROPORTIONAL_GAIN,
        DEGREE_INTEGRAL_GAIN,
        DEGREE_DERIVATIVE_GAIN,
        degree_integral_term,
        delta_time,
        deviation_from_course,
        delta_deviation_from_course
    )

    prev_time = current_time
    prev_deviation_from_course = deviation_from_course
    prev_distance_to_target = distance_to_target
    prev_output_value = engine_speed, steering_wheel_degree

    return engine_speed, steering_wheel_degree


def calculate_pid_output(proportional_gain: float, integral_gain: float, derivative_gain: float,
                         integral_term: list[float], delta_time: float,
                         error: float, delta_error: float) -> float:
    proportional_term = proportional_gain * error
    integral_term[0] += error * delta_time
    derivative_term = derivative_gain * (delta_error / delta_time)

    return proportional_term + integral_gain * integral_term[0] + derivative_term
