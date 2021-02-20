from typing import Final

import pygame
from pygame.color import Color

from src.gui import boat

X_WINDOW_SIZE: Final[int] = 1000
Y_WINDOW_SIZE: Final[int] = 800
BACKGROUND_COLOR: Final[Color] = Color(156, 192, 249)
WINDOW_CAPTION: Final[str] = "Boat"

INITIAL_X_COORDINATE: Final[int] = X_WINDOW_SIZE // 2
INITIAL_Y_COORDINATE: Final[int] = 0

BOAT_COLOR: Final[Color] = Color(34, 139, 34)
BOAT_CIRCLE_RADIUS: Final[int] = 20


def init_app_window() -> None:
    window_size = [X_WINDOW_SIZE, Y_WINDOW_SIZE]
    app_window = pygame.display.set_mode(window_size)
    app_window.fill(BACKGROUND_COLOR)
    pygame.display.set_caption(WINDOW_CAPTION)


def execute_run_loop() -> None:
    boat.init_coordinates(INITIAL_X_COORDINATE, INITIAL_Y_COORDINATE)
    draw_boat()

    run_loop = True
    move_ticker = 0

    while run_loop:
        boat.go_ahead()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP]:
            move_ticker = 60
            boat.increase_speed()
        elif pressed_keys[pygame.K_DOWN]:
            move_ticker = 60
            boat.decrease_speed()
        elif pressed_keys[pygame.K_LEFT]:
            move_ticker = 60
            boat.move_left()
        elif pressed_keys[pygame.K_RIGHT]:
            move_ticker = 60
            boat.move_right()

        if move_ticker > 0:
            move_ticker -= 1

        pygame.display.get_surface().fill(BACKGROUND_COLOR)
        draw_boat()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False


def draw_boat():
    boat_coordinates = boat.get_current_coordinates()
    boat_coordinates = convert_to_pygame_coordinates(boat_coordinates)

    pygame.draw.circle(
        pygame.display.get_surface(),
        BOAT_COLOR,
        pygame.Vector2(boat_coordinates),
        BOAT_CIRCLE_RADIUS
    )


def convert_to_pygame_coordinates(coordinates: tuple[float, float]) -> tuple[float, float]:
    return coordinates[0], Y_WINDOW_SIZE - coordinates[1]
