import threading

from typing import Final, Sequence, Union

import pygame
from pygame.rect import Rect
from pygame.freetype import Font
from pygame.math import Vector2

from src.pid import feedback_loop
from src.pid import pid
from src.sensors import compass
from src.gui import boat, setpoint

X_WINDOW_SIZE: Final[int] = 1000
Y_WINDOW_SIZE: Final[int] = 800
BACKGROUND_COLOR: Final[pygame.Color] = pygame.Color(156, 192, 249)
WINDOW_CAPTION: Final[str] = "Boat"

FONT_SIZE: Final[int] = 20
FONT_COLOR: Final[pygame.Color] = pygame.Color(0, 0, 0)
BOAT_VELOCITY_DISPLAY_COORDINATES: tuple[int, int] = (10, 650)
STEERING_WHEEL_ANGLE_DISPLAY_COORDINATES: tuple[int, int] = (10, 700)
COMPASS_DATA_DISPLAY_COORDINATES: tuple[int, int] = (10, 750)
font: Font

INITIAL_TOP_ANGLE_LOCATION: Final[Vector2] = Vector2(X_WINDOW_SIZE // 2, 50)
INITIAL_LEFT_ANGLE_LOCATION: Final[Vector2] = Vector2(X_WINDOW_SIZE // 2 - 20, 0)
INITIAL_RIGHT_ANGLE_LOCATION: Final[Vector2] = Vector2(X_WINDOW_SIZE // 2 + 20, 0)

FPS: Final[int] = 60

BOAT_COLOR: Final[pygame.Color] = pygame.Color(34, 139, 34)
BOAT_CIRCLE_RADIUS: Final[int] = 20

SETPOINT_COLOR: Final[pygame.Color] = pygame.Color(255, 0, 0)
SETPOINT_CIRCLE_RADIUS: Final[int] = 5

LEFT_MOUSE_BUTTON: Final[int] = 1
RIGHT_MOUSE_BUTTON: Final[int] = 3

EXTERNAL_FORCE_VECTOR: Final[Vector2] = Vector2(15, 0)

is_feedback_loop_running: bool = False
setpoint_rect: Union[Rect, None] = None

velocity_from_pid: float = 0
steering_wheel_angle_from_pid: float = 0

handle_pid_lock = threading.Lock()

is_pid_reaction_thread_running: bool = False
pid_reaction_thread: Union[threading.Thread, None] = None


def init_app_window() -> None:
    global font

    window_size = [X_WINDOW_SIZE, Y_WINDOW_SIZE]
    app_window = pygame.display.set_mode(window_size)
    app_window.fill(BACKGROUND_COLOR)
    pygame.display.set_caption(WINDOW_CAPTION)

    font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), FONT_SIZE)


def execute_run_loop() -> None:
    boat.init_boat(INITIAL_TOP_ANGLE_LOCATION, INITIAL_LEFT_ANGLE_LOCATION, INITIAL_RIGHT_ANGLE_LOCATION)
    setpoint.set_coordinates(None, None)

    display_surface = pygame.display.get_surface()
    redraw_display(display_surface)
    clock = pygame.time.Clock()

    while True:
        delta_time = clock.get_time() / 1000

        pressed_keys = pygame.key.get_pressed()
        handle_pressed_keys(pressed_keys, delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
                remove_setpoint()
                setpoint_x_coordinate, setpoint_y_coordinate = convert_coordinates(pygame.mouse.get_pos())
                setpoint.set_coordinates(setpoint_x_coordinate, setpoint_y_coordinate)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_BUTTON:
                remove_setpoint()

        if is_feedback_loop_running:
            handle_pid(delta_time)

        # apply_external_force(delta_time)
        boat.go_ahead(delta_time)

        center_location = boat.get_center_location()
        location_coordinates = (center_location.x, center_location.y)
        if setpoint_rect and setpoint_rect.collidepoint(convert_coordinates(location_coordinates)):
            remove_setpoint()

        redraw_display(display_surface)
        clock.tick_busy_loop(FPS)


def handle_pid(delta_time: float) -> None:
    global velocity_from_pid, steering_wheel_angle_from_pid, is_pid_reaction_thread_running, pid_reaction_thread

    handle_pid_lock.acquire()

    velocity_from_pid, steering_wheel_angle_from_pid = feedback_loop.run_iteration(
        setpoint.get_coordinates(),
        delta_time
    )

    print(f"speed from PID: {velocity_from_pid}")
    print(f"angle from PID: {steering_wheel_angle_from_pid}")
    print(f"current boat velocity: {boat.get_current_velocity()}\n")

    handle_pid_lock.release()

    if not is_pid_reaction_thread_running:
        is_pid_reaction_thread_running = True
        pid_reaction_thread = threading.Thread(target=react_to_pid_changes, args=(delta_time,), daemon=True)
        pid_reaction_thread.start()


def react_to_pid_changes(delta_time: float) -> None:
    delta_time *= 5

    while is_pid_reaction_thread_running:
        handle_pid_lock.acquire()

        if boat.get_current_velocity() > velocity_from_pid:
            boat.decrease_velocity(delta_time)

        if boat.get_current_velocity() < velocity_from_pid:
            boat.increase_velocity(delta_time)

        if boat.get_current_steering_wheel_angle() > steering_wheel_angle_from_pid:
            boat.turn_steering_wheel_left(delta_time)

        if boat.get_current_steering_wheel_angle() < steering_wheel_angle_from_pid:
            boat.turn_steering_wheel_right(delta_time)

        handle_pid_lock.release()


def handle_pressed_keys(pressed_keys: Sequence[bool], delta_time: float) -> None:
    if pressed_keys[pygame.K_UP]:
        boat.increase_velocity(delta_time)
    elif pressed_keys[pygame.K_DOWN]:
        boat.decrease_velocity(delta_time)
    else:
        boat.apply_resistance_deceleration(delta_time)

    if pressed_keys[pygame.K_LEFT]:
        boat.turn_steering_wheel_left(delta_time)
    elif pressed_keys[pygame.K_RIGHT]:
        boat.turn_steering_wheel_right(delta_time)
    else:
        boat.apply_resistance_steering_wheel_rotate()

    if pressed_keys[pygame.K_r]:
        set_feedback_loop_status()


def apply_external_force(delta_time: float) -> None:
    external_force_location_delta = EXTERNAL_FORCE_VECTOR * delta_time
    top_angle_location, left_angle_location, right_angle_location, center_location = boat.get_current_coordinates()
    boat.set_coordinates(
        top_angle_location + external_force_location_delta,
        left_angle_location + external_force_location_delta,
        right_angle_location + external_force_location_delta,
        center_location + external_force_location_delta
    )


def remove_setpoint() -> None:
    global setpoint_rect

    setpoint.set_coordinates(None, None)
    set_feedback_loop_status()
    setpoint_rect = None


def set_feedback_loop_status() -> None:
    global is_feedback_loop_running, is_pid_reaction_thread_running

    if setpoint.is_setpoint_exist():
        is_feedback_loop_running = True
    else:
        is_feedback_loop_running = False
        is_pid_reaction_thread_running = False
        pid.reset_pid()


def redraw_display(display_surface: pygame.Surface) -> None:
    display_surface.fill(BACKGROUND_COLOR)

    top_angle_location, left_angle_location, right_angle_location, _ = boat.get_current_coordinates()

    boat_center_location = boat.get_center_location()
    boat_angle = convert_angle(boat.get_angle())

    top_angle_location = rotate_angle_coordinate(top_angle_location, boat_center_location, boat_angle)
    left_angle_location = rotate_angle_coordinate(left_angle_location, boat_center_location, boat_angle)
    right_angle_location = rotate_angle_coordinate(right_angle_location, boat_center_location, boat_angle)

    top_angle_location = convert_coordinates((top_angle_location.x, top_angle_location.y))
    left_angle_location = convert_coordinates((left_angle_location.x, left_angle_location.y))
    right_angle_location = convert_coordinates((right_angle_location.x, right_angle_location.y))

    pygame.draw.polygon(
        display_surface,
        BOAT_COLOR,
        [top_angle_location, left_angle_location, right_angle_location]
    )

    font.render_to(
        display_surface,
        BOAT_VELOCITY_DISPLAY_COORDINATES,
        f"Boat velocity: {boat.get_current_velocity()} px/sec",
        FONT_COLOR
    )

    font.render_to(
        display_surface,
        STEERING_WHEEL_ANGLE_DISPLAY_COORDINATES,
        f"Steering wheel angle: {boat.get_current_steering_wheel_angle()}°",
        FONT_COLOR
    )

    font.render_to(
        display_surface,
        COMPASS_DATA_DISPLAY_COORDINATES,
        f"Compass data: {get_compass_data()}°",
        FONT_COLOR
    )

    draw_setpoint(display_surface)

    pygame.display.flip()


def convert_angle(angle: float) -> float:
    return -angle


def rotate_angle_coordinate(angle_location: Vector2, boat_center_location: Vector2, boat_angle: float) -> Vector2:
    reduced_angle_location = angle_location - boat_center_location
    reduced_angle_location.rotate_ip_rad(boat_angle)

    return reduced_angle_location + boat_center_location


def get_compass_data() -> float:
    return round(compass.get_deviation_from_north())


def draw_setpoint(display_surface: pygame.Surface) -> None:
    global setpoint_rect

    setpoint_coordinates = setpoint.get_coordinates()

    if not (setpoint_coordinates[0] is None and setpoint_coordinates[1] is None):
        setpoint_coordinates = convert_coordinates(setpoint_coordinates)

        setpoint_rect = pygame.draw.circle(
            display_surface,
            SETPOINT_COLOR,
            setpoint_coordinates,
            SETPOINT_CIRCLE_RADIUS
        )


def convert_coordinates(coordinates: tuple[float, float]) -> tuple[float, float]:
    return coordinates[0], Y_WINDOW_SIZE - coordinates[1]
