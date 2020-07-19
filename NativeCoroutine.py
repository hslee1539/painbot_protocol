import asyncio
import typing

## 테스트 코드입니다.

class NativeCoroutine:
    def __init__(self, coroutine : typing.Generator):
        self.func = coroutine
        pass

    async def __call__(self, data = typing.Any) -> typing.Any:
        retval = None
        if data is typing.Any:
            retval = next(self.func)
        else:
            retval = self.func.send(data)
        return retval


"""
예제입니다
"""
if __name__ == "__main__":
    from ParserCoroutine import ParserCoroutine
    from SerialWrapper import SerialWrapper
    from PlotCoroutine import PlotCoroutine
    import matplotlib.pyplot as plt

    with PlotCoroutine(plt.figure(figsize=[1,1])) as plot:
        with ParserCoroutine() as parser:
            with SerialWrapper("debug") as ser:
                native_plot = NativeCoroutine(plot)
                native_parser = NativeCoroutine(parser)
                async def main():
                    while True:
                        retval = await native_parser(ser.read())
                        if type(retval) is dict:
                            await native_plot(retval["low frequency electric current"])
                    
                
                
                asyncio.run(main())


