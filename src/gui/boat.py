import math
from typing import Final

SPEED_RESISTANCE: Final[float] = 0.0005
STEERING_WHEEL_ANGLE_RESISTANCE: Final[float] = math.radians(0.01)

SPEED_DELTA: Final[float] = 0.001
STEERING_WHEEL_ANGLE_DELTA: Final[float] = math.radians(0.05)

MAX_ABSOLUTE_SPEED: Final[float] = 0.5
MAX_ABSOLUTE_STEERING_WHEEL_ANGLE: Final[float] = math.radians(30)

x_coordinate: float
y_coordinate: float

boat_speed: float = 0
steering_wheel_angle: float = 0


def init_coordinates(init_x_coordinate: float, init_y_coordinate: float) -> None:
    global x_coordinate, y_coordinate
    x_coordinate = init_x_coordinate
    y_coordinate = init_y_coordinate


def set_x_coordinate(x: float) -> None:
    global x_coordinate
    x_coordinate = x


def get_current_coordinates() -> tuple[float, float]:
    return x_coordinate, y_coordinate


def get_current_speed() -> float:
    return round(boat_speed, 3)


def get_current_steering_wheel_angle() -> float:
    return round(math.degrees(steering_wheel_angle), 2)


# TODO: В данный момент вектор нормали кораблика направлен строго вертикально, а нужно по направлению движения
#  (т.е. катеты треугольника движения не будут только X или только Y)
def go_ahead() -> None:
    global boat_speed, steering_wheel_angle, x_coordinate, y_coordinate

    boat_speed = apply_resistance(boat_speed, SPEED_RESISTANCE)

    if is_zero_reached(boat_speed, SPEED_DELTA, SPEED_RESISTANCE):
        boat_speed = 0
    elif is_max_value_reached(boat_speed, MAX_ABSOLUTE_SPEED):
        if boat_speed > 0:
            boat_speed = MAX_ABSOLUTE_SPEED
        else:
            boat_speed = -MAX_ABSOLUTE_SPEED

    if not math.isclose(boat_speed, 0):
        steering_wheel_angle = apply_resistance(steering_wheel_angle, STEERING_WHEEL_ANGLE_RESISTANCE)

    if is_zero_reached(steering_wheel_angle, STEERING_WHEEL_ANGLE_DELTA, STEERING_WHEEL_ANGLE_RESISTANCE):
        steering_wheel_angle = 0
    elif is_max_value_reached(steering_wheel_angle, MAX_ABSOLUTE_STEERING_WHEEL_ANGLE):
        if steering_wheel_angle > 0:
            steering_wheel_angle = MAX_ABSOLUTE_STEERING_WHEEL_ANGLE
        else:
            steering_wheel_angle = -MAX_ABSOLUTE_STEERING_WHEEL_ANGLE

    if boat_speed > 0:
        x_coordinate += boat_speed * math.sin(steering_wheel_angle)
    else:
        x_coordinate -= boat_speed * math.sin(steering_wheel_angle)

    y_coordinate += boat_speed * math.cos(steering_wheel_angle)


def apply_resistance(current_value: float, resistance_value: float) -> float:
    if math.isclose(abs(current_value), 0):
        return current_value

    if current_value > 0:
        return current_value - resistance_value
    else:
        return current_value + resistance_value


def is_zero_reached(current_value: float, delta_value: float, resistance_value: float) -> bool:
    if math.isclose(abs(current_value), 0):
        return True

    return abs(current_value) < delta_value - resistance_value


def is_max_value_reached(current_value: float, max_value: float) -> bool:
    return abs(current_value) > max_value or math.isclose(abs(current_value), max_value)


def increase_speed() -> None:
    global boat_speed
    boat_speed += SPEED_DELTA


def decrease_speed() -> None:
    global boat_speed
    boat_speed -= SPEED_DELTA


def turn_steering_wheel_left() -> None:
    global steering_wheel_angle
    steering_wheel_angle -= STEERING_WHEEL_ANGLE_DELTA


def turn_steering_wheel_right() -> None:
    global steering_wheel_angle
    steering_wheel_angle += STEERING_WHEEL_ANGLE_DELTA
