from data import ImmutablePainState, PlotState
from typing import Generator, Any
from GeneratorUtil import filterIsType, scan


def __sum_state(state: PlotState, index_and_action: tuple[int, int]):
    (index, action) = index_and_action
    if index < 100:
        return PlotState(xs=state.xs + [index], ys=state.ys + [action], y_lim=(0, 100))
    else:
        return PlotState(
            xs=state.xs[1:] + [index], ys=state.ys[1:] + [action], y_lim=(0, 100)
        )


def plot_model(action: Generator[ImmutablePainState | Any, None, None]):
    stream = filterIsType(action, ImmutablePainState)
    stream = map(lambda state: state.lowpulse_v, stream)
    stream = enumerate(stream)
    return scan(__sum_state, stream, PlotState([], [], (0, 100)))
