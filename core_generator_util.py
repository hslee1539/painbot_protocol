from typing import Generator, Callable


def take(stream: Generator[any, any, None], m: int):
    if m > 0:
        m -= 1
        for i, next in enumerate(stream):
            yield (next)
            if i >= m:
                break


def last(stream: Generator[any, any, None]):
    for i in stream:
        pass
    yield i


def filterIsType(stream: Generator[any, any, None], cls: any):
    for i in stream:
        if type(i) == cls:
            yield i


def scan(fn: Callable[[any, any], any], stream: Generator[any, any, None], init: any):
    s = init
    for i in stream:
        s = fn(s, i)
        yield (s)
