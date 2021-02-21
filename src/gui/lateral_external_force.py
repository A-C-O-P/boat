from typing import Final

from src.gui import boat

EXTERNAL_FORCE: Final[float] = 0.1


def use_force() -> None:
    boat.set_x_coordinate(boat.get_current_coordinates()[0] + EXTERNAL_FORCE)
