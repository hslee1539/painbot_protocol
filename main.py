from serial import Serial
from SerialWrapper import read_serial
from ParserCoroutine import flatmap_parse, flatten
from PlotModel import plot_model
from PlotCoroutine import plot
from typing import Generator, Any
from data import ImmutablePainState, PlotState

def repository(serial: Serial):
    return read_serial(serial)

def use_case(raw_stream: Generator[bytes, None, None]):
    return flatmap_parse(flatten(raw_stream))

def model(action: Generator[ImmutablePainState | Any, None, None]):
    return plot_model(action)

def render(state: Generator[PlotState, None, None]):
    plot(state)

if __name__ == "__main__":
    with Serial(port="COM3", baudrate=9600) as serial:
        render(model(use_case(repository(serial))))
