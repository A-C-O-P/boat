from typing import Final

import pygame
from pygame.color import Color

from src.gui import boat

X_WINDOW_SIZE: Final[int] = 1000
Y_WINDOW_SIZE: Final[int] = 800
BACKGROUND_COLOR: Final[Color] = Color(156, 192, 249)
WINDOW_CAPTION: Final[str] = "Boat"

INITIAL_X_COORDINATE: Final[int] = X_WINDOW_SIZE // 2
INITIAL_Y_COORDINATE: Final[int] = Y_WINDOW_SIZE

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

    while run_loop:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False


def draw_boat():
    pygame.display.get_surface().fill(BACKGROUND_COLOR)

    boat_coordinates = boat.get_current_coordinates()
    pygame.draw.circle(
        pygame.display.get_surface(),
        BOAT_COLOR,
        pygame.Vector2(boat_coordinates),
        BOAT_CIRCLE_RADIUS
    )

    pygame.display.flip()
