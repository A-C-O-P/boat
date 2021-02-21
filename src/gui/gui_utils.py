from typing import Final

import pygame
from pygame.freetype import Font

from src.gui import boat

X_WINDOW_SIZE: Final[int] = 1000
Y_WINDOW_SIZE: Final[int] = 800
BACKGROUND_COLOR: Final[pygame.Color] = pygame.Color(156, 192, 249)
WINDOW_CAPTION: Final[str] = "Boat"

FONT_SIZE: Final[int] = 20
FONT_COLOR: Final[pygame.Color] = pygame.Color(0, 0, 0)
BOAT_SPEED_DISPLAY_COORDINATES: tuple[int, int] = (10, 700)
font: Font

INITIAL_X_COORDINATE: Final[int] = X_WINDOW_SIZE // 2
INITIAL_Y_COORDINATE: Final[int] = 0

FPS: Final[int] = 300

BOAT_COLOR: Final[pygame.Color] = pygame.Color(34, 139, 34)
BOAT_CIRCLE_RADIUS: Final[int] = 20


def init_app_window() -> None:
    global font

    window_size = [X_WINDOW_SIZE, Y_WINDOW_SIZE]
    app_window = pygame.display.set_mode(window_size)
    app_window.fill(BACKGROUND_COLOR)
    pygame.display.set_caption(WINDOW_CAPTION)

    font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), FONT_SIZE)


def execute_run_loop() -> None:
    boat.init_coordinates(INITIAL_X_COORDINATE, INITIAL_Y_COORDINATE)
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
            boat.move_left()
        elif pressed_keys[pygame.K_RIGHT]:
            boat.move_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        boat.go_ahead()
        redraw_display(display_surface)


def redraw_display(display_surface: pygame.Surface) -> None:
    display_surface.fill(BACKGROUND_COLOR)

    boat_coordinates = boat.get_current_coordinates()
    boat_coordinates = convert_to_pygame_coordinates(boat_coordinates)

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

    pygame.display.flip()


def convert_to_pygame_coordinates(coordinates: tuple[float, float]) -> tuple[float, float]:
    return coordinates[0], Y_WINDOW_SIZE - coordinates[1]
