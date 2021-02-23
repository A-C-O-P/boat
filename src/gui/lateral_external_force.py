from typing import Final

from src.gui import boat

EXTERNAL_FORCE: Final[float] = 0.5


def use_force() -> None:
    top_angle_location, left_angle_location, right_angle_location = boat.get_current_coordinates()

    top_angle_location.x += EXTERNAL_FORCE
    left_angle_location.x += EXTERNAL_FORCE
    right_angle_location.x += EXTERNAL_FORCE

    boat.set_coordinates(top_angle_location, left_angle_location, right_angle_location)
