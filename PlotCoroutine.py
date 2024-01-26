import matplotlib.pyplot as plt
import matplotlib.axes as axes
from collections import deque
from typing import Generator
from dataclasses import dataclass


# ui state
@dataclass(frozen=True)
class PlotState:
    xs: list[int]
    ys: list[float]
    y_lim: tuple[int, int]


def plot(state: Generator[PlotState, None, None]):
    fig = plt.figure(figsize=[1, 1])
    subplot = fig.add_subplot(1, 1, 1)
    
    try:
        plt.connect("close_event", exit)
        for next in state:
            subplot.clear()
            subplot.set_xlim((0, 50))
            subplot.set_ylim(next.y_lim)
            if len(next.xs) > 0:
                subplot.plot(next.xs, next.ys)
                plt.draw()
            plt.pause(0.001)
    except Exception as e:
        print(e)
        pass
    finally:
        plt.close(fig)


"""
예제 코드입니다.

"""

if __name__ == "__main__":

    def dummy_model():
        import random

        for i in range(10000):
            if i < 50:
                xs = [it for it in range(i)]
            else:
                xs = [it for it in range(50)]
            ys = [it % 50 + random.random() * 50 for it in xs]
            yield PlotState(xs=xs, ys=ys, y_lim=(0, 100))
    
    plot(dummy_model())
