from serial import Serial
from core_serial import read_serial
from core_parser import flatmap_parse, flatten
from core_model import plot_model
from core_plot import plot
from typing import Generator, Any
from core_data import ImmutablePainState, PlotState

def repository(serial: Serial):
    return read_serial(serial)

def use_case(raw_stream: Generator[bytes, None, None]):
    return flatmap_parse(flatten(raw_stream))

def model(action: Generator[ImmutablePainState | Any, None, None]):
    return plot_model(action)

def render(state: Generator[PlotState, None, None]):
    plot(state)

if __name__ == "__main__":
    with Serial(port="COM3", baudrate=11520) as serial:
        render(model(use_case(repository(serial))))
