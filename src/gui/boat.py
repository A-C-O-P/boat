import math
from typing import Final

from pygame.math import Vector2

BREAK_DECELERATION: Final[float] = 20

ACCELERATION_RESISTANCE: Final[float] = 10
STEERING_WHEEL_ANGLE_RESISTANCE: Final[float] = math.radians(0.5)

BOAT_ACCELERATION_DELTA: Final[float] = 5
STEERING_WHEEL_ANGLE_DELTA: Final[float] = math.radians(10)

MAX_VELOCITY: Final[float] = 200
MAX_ACCELERATION: Final[float] = 50
MAX_STEERING_WHEEL_ANGLE: Final[float] = math.radians(30)

boat_top_angle_location: Vector2
boat_left_angle_location: Vector2
boat_right_angle_location: Vector2
boat_center_location: Vector2
boat_length: float
boat_angle: float = 0

boat_velocity: Vector2 = Vector2(0, 0)
boat_acceleration: float = 0

steering_wheel_angle: float = 0


def init_boat(init_boat_top_angle_location: Vector2, init_boat_left_angle_location: Vector2,
              init_boat_right_angle_location: Vector2) -> None:
    global boat_top_angle_location, boat_left_angle_location, boat_right_angle_location, boat_length

    boat_top_angle_location = init_boat_top_angle_location
    boat_left_angle_location = init_boat_left_angle_location
    boat_right_angle_location = init_boat_right_angle_location

    boat_length = boat_top_angle_location.y - boat_left_angle_location.y


def increase_velocity(delta_time: float) -> None:
    global boat_acceleration

    if is_positive_velocity():
        boat_acceleration += BOAT_ACCELERATION_DELTA * delta_time
    else:
        boat_acceleration = BREAK_DECELERATION


def decrease_velocity(delta_time: float) -> None:
    global boat_acceleration

    if is_positive_velocity():
        boat_acceleration = -BREAK_DECELERATION
    else:
        boat_acceleration -= BOAT_ACCELERATION_DELTA * delta_time


def is_positive_velocity() -> bool:
    return math.isclose(boat_velocity.y, 0) or boat_velocity.y > 0


def apply_resistance_deceleration(delta_time: float) -> None:
    global boat_acceleration

    if abs(boat_velocity.y) > delta_time * ACCELERATION_RESISTANCE:
        boat_acceleration = -math.copysign(ACCELERATION_RESISTANCE, boat_velocity.y)
    elif not math.isclose(delta_time, 0):
        boat_acceleration = -boat_velocity.y / delta_time


def turn_steering_wheel_left(delta_time: float) -> None:
    global steering_wheel_angle
    steering_wheel_angle -= STEERING_WHEEL_ANGLE_DELTA * delta_time


def turn_steering_wheel_right(delta_time: float) -> None:
    global steering_wheel_angle
    steering_wheel_angle += STEERING_WHEEL_ANGLE_DELTA * delta_time


def apply_resistance_steering_wheel_rotate() -> None:
    global steering_wheel_angle

    if (math.isclose(abs(steering_wheel_angle), 0)
            or abs(steering_wheel_angle) < STEERING_WHEEL_ANGLE_RESISTANCE):
        steering_wheel_angle = 0
    elif steering_wheel_angle > 0:
        steering_wheel_angle -= STEERING_WHEEL_ANGLE_RESISTANCE
    else:
        steering_wheel_angle += STEERING_WHEEL_ANGLE_RESISTANCE


def go_ahead(delta_time: float) -> None:
    apply_acceleration(delta_time)
    rotate_boat(delta_time)


def apply_acceleration(delta_time: float) -> None:
    global boat_acceleration, boat_velocity

    boat_acceleration = get_max_value_when_overflow(
        boat_acceleration, MAX_ACCELERATION
    )

    boat_velocity += Vector2(0, boat_acceleration * delta_time)
    boat_velocity.y = get_max_value_when_overflow(
        boat_velocity.y, MAX_VELOCITY
    )


def rotate_boat(delta_time: float) -> None:
    global steering_wheel_angle, boat_top_angle_location, boat_left_angle_location
    global boat_right_angle_location, boat_angle

    steering_wheel_angle = get_max_value_when_overflow(
        steering_wheel_angle, MAX_STEERING_WHEEL_ANGLE
    )

    if math.isclose(steering_wheel_angle, 0):
        angular_velocity = 0
    else:
        turning_radius = boat_length / math.sin(steering_wheel_angle)
        angular_velocity = boat_velocity.y / turning_radius

    velocity_vector = boat_velocity.rotate_rad(-boat_angle) * delta_time

    boat_top_angle_location += velocity_vector
    boat_left_angle_location += velocity_vector
    boat_right_angle_location += velocity_vector

    boat_angle += angular_velocity * delta_time


def get_max_value_when_overflow(current_value: float, max_value: float) -> float:
    return max(
        -max_value,
        min(current_value, max_value)
    )


def get_current_coordinates() -> tuple[Vector2, Vector2, Vector2]:
    return boat_top_angle_location, boat_left_angle_location, boat_right_angle_location


def get_current_velocity() -> float:
    return round(boat_velocity.y, 3)


def get_current_steering_wheel_angle() -> float:
    return round(math.degrees(steering_wheel_angle), 2)


def set_coordinates(top_angle_location: Vector2, left_angle_location: Vector2, right_angle_location: Vector2) -> None:
    global boat_top_angle_location, boat_left_angle_location, boat_right_angle_location

    boat_top_angle_location = top_angle_location
    boat_left_angle_location = left_angle_location
    boat_right_angle_location = right_angle_location
