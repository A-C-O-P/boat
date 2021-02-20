import pygame

from src.gui.gui_utils import execute_run_loop, init_app_window


def main() -> None:
    pygame.init()
    init_app_window()
    execute_run_loop()
    pygame.quit()


if __name__ == '__main__':
    main()
