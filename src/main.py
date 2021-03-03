import pygame

from src.gui.gui_utils import execute_run_loop, init_app_window


# TODO:
#   1. Реализовать возвращение отрицательной скорости из PID
#   2. Реализовать движение кораблика по точкам с помощью PID
#   3. Отображать поворот руля
#   4. Отображать скорость кораблика на самом кораблике
#   5. Отрисовывать более реалистичный кораблик (например, использовать 5 точек для построения)


def main() -> None:
    pygame.init()
    init_app_window()
    execute_run_loop()
    pygame.quit()


if __name__ == '__main__':
    main()
