from src.gui import boat


def get_boat_center_location() -> tuple[float, float]:
    boat_location = boat.get_center_location()
    return boat_location.x, boat_location.y
