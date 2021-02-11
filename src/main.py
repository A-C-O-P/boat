import time
from typing import Final

import matplotlib.pyplot as plt
import numpy
from scipy.interpolate import make_interp_spline

import pid

LOOP_END: Final[int] = 50


def main() -> None:
    set_point = 0.0

    feedback_list: list[int] = []
    time_list: list[float] = []
    set_point_list: list[float] = []

    feedback = 0

    for i in range(1, LOOP_END):
        engine_speed_output, steering_wheel_degree_output = pid.update_pid(set_point - feedback)

        if set_point > 0:
            # TODO: change feedback calculation
            feedback += ((steering_wheel_degree_output) - (1 / i))
        if i > 9:
            set_point = 1.0

        time.sleep(0.02)

        feedback_list.append(feedback)
        time_list.append(i)
        set_point_list.append(set_point)

    draw_graphics(time_list, feedback_list, set_point_list)


def draw_graphics(time_list: list[float], feedback_list: list[int],
                  set_point_list: list[float]) -> None:
    time_array = numpy.array(time_list)
    time_smooth = numpy.linspace(time_array.min(), time_array.max(), 300)

    helper_x3 = make_interp_spline(time_list, feedback_list)
    feedback_smooth = helper_x3(time_smooth)
    plt.plot(time_smooth, feedback_smooth)
    plt.plot(time_list, set_point_list)
    plt.xlim((0, LOOP_END))
    plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5))
    plt.xlabel('time (s)')
    plt.ylabel('Deviation from course')
    plt.title('BOAT PID')

    plt.ylim((1 - 0.5, 1 + 0.5))

    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
