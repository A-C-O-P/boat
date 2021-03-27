import math


# https://stackoverflow.com/a/45351293
def calc_angle_between_vectors(x_first_vector: float, y_first_vector: float,
                               x_second_vector: float, y_second_vector: float) -> float:
    first_vector_angle = math.atan2(y_first_vector, x_first_vector)
    second_vector_angle = math.atan2(y_second_vector, x_second_vector)

    angles_diff = second_vector_angle - first_vector_angle

    if angles_diff < -math.pi:
        angles_diff = 2 * math.pi - abs(angles_diff)
    elif angles_diff > math.pi:
        angles_diff = 2 * -math.pi + abs(angles_diff)

    return -angles_diff


def normalize_vector(x_coordinate: float, y_coordinate: float) -> tuple[float, float]:
    vector_length = calc_vector_length(x_coordinate, y_coordinate)
    return x_coordinate / vector_length, y_coordinate / vector_length


def calc_vector_length(x_coordinate: float, y_coordinate: float) -> float:
    return math.sqrt(
        math.pow(x_coordinate, 2) + math.pow(y_coordinate, 2)
    )


def calc_distance_between_vectors(x_first_vector: float, x_second_vector: float,
                                  y_first_vector: float, y_second_vector: float) -> float:
    return math.sqrt(
        math.pow(x_first_vector - x_second_vector, 2)
        + math.pow(y_first_vector - y_second_vector, 2)
    )


def calc_dot_product_of_vectors(x_first_vector: float, x_second_vector: float,
                                y_first_vector: float, y_second_vector: float) -> float:
    return (x_first_vector * x_second_vector) + (y_first_vector * y_second_vector)
