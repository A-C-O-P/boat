from typing import Final

import pygame
from pygame.freetype import Font

from src.gui import boat, setpoint, lateral_external_force

X_WINDOW_SIZE: Final[int] = 1000
Y_WINDOW_SIZE: Final[int] = 800
BACKGROUND_COLOR: Final[pygame.Color] = pygame.Color(156, 192, 249)
WINDOW_CAPTION: Final[str] = "Boat"

FONT_SIZE: Final[int] = 20
FONT_COLOR: Final[pygame.Color] = pygame.Color(0, 0, 0)
BOAT_SPEED_DISPLAY_COORDINATES: tuple[int, int] = (10, 700)
STEERING_WHEEL_ANGLE_DISPLAY_COORDINATES: tuple[int, int] = (10, 750)
font: Font

INITIAL_X_COORDINATE: Final[int] = X_WINDOW_SIZE // 2
INITIAL_Y_COORDINATE: Final[int] = 0

FPS: Final[int] = 300

BOAT_COLOR: Final[pygame.Color] = pygame.Color(34, 139, 34)
BOAT_CIRCLE_RADIUS: Final[int] = 20

SETPOINT_COLOR: Final[pygame.Color] = pygame.Color(255, 0, 0)
SETPOINT_CIRCLE_RADIUS: Final[int] = 5

LEFT_MOUSE_BUTTON: Final[int] = 1
RIGHT_MOUSE_BUTTON: Final[int] = 3


def init_app_window() -> None:
    global font

    window_size = [X_WINDOW_SIZE, Y_WINDOW_SIZE]
    app_window = pygame.display.set_mode(window_size)
    app_window.fill(BACKGROUND_COLOR)
    pygame.display.set_caption(WINDOW_CAPTION)

    font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), FONT_SIZE)


def execute_run_loop() -> None:
    boat.init_coordinates(INITIAL_X_COORDINATE, INITIAL_Y_COORDINATE)
    setpoint.set_coordinates(None, None)

    display_surface = pygame.display.get_surface()
    redraw_display(display_surface)
    clock = pygame.time.Clock()

    while True:
        clock.tick_busy_loop(FPS)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP]:
            boat.increase_speed()
        elif pressed_keys[pygame.K_DOWN]:
            boat.decrease_speed()
        elif pressed_keys[pygame.K_LEFT]:
            boat.turn_steering_wheel_left()
        elif pressed_keys[pygame.K_RIGHT]:
            boat.turn_steering_wheel_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
                setpoint_x_coordinate, setpoint_y_coordinate = convert_coordinates(pygame.mouse.get_pos())
                setpoint.set_coordinates(setpoint_x_coordinate, setpoint_y_coordinate)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_BUTTON:
                setpoint.set_coordinates(None, None)

        # lateral_external_force.use_force()
        boat.go_ahead()
        redraw_display(display_surface)


def redraw_display(display_surface: pygame.Surface) -> None:
    display_surface.fill(BACKGROUND_COLOR)

    boat_coordinates = boat.get_current_coordinates()
    boat_coordinates = convert_coordinates(boat_coordinates)

    pygame.draw.circle(
        display_surface,
        BOAT_COLOR,
        boat_coordinates,
        BOAT_CIRCLE_RADIUS
    )

    font.render_to(
        display_surface,
        BOAT_SPEED_DISPLAY_COORDINATES,
        f"Boat speed: {boat.get_current_speed()}",
        FONT_COLOR
    )

    font.render_to(
        display_surface,
        STEERING_WHEEL_ANGLE_DISPLAY_COORDINATES,
        f"Steering wheel angle: {boat.get_current_steering_wheel_angle()}",
        FONT_COLOR
    )

    draw_setpoint(display_surface)

    pygame.display.flip()


def draw_setpoint(display_surface: pygame.Surface) -> None:
    setpoint_coordinates = setpoint.get_coordinates()

    if not (setpoint_coordinates[0] is None and setpoint_coordinates[1] is None):
        setpoint_coordinates = convert_coordinates(setpoint_coordinates)

        pygame.draw.circle(
            display_surface,
            SETPOINT_COLOR,
            setpoint_coordinates,
            SETPOINT_CIRCLE_RADIUS
        )


def convert_coordinates(coordinates: tuple[float, float]) -> tuple[float, float]:
    return coordinates[0], Y_WINDOW_SIZE - coordinates[1]
