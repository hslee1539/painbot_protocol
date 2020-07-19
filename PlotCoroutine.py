import matplotlib.pyplot as plt
import matplotlib.axes as axes
from collections import deque


class PlotCoroutine:
    def __init__(self, fig : plt.Figure,plot_size = 100):
        self.fig = fig
        self.plot_size = plot_size

    def __enter__(self):
        self._drawer = self._draw()
        next(self._drawer)
        return self._drawer

    def __exit__(self, type, value, traceback):
        pass
    
    def _draw(self):
        subplot = self.fig.add_subplot(1,1,1)
        subplot : axes.Axes
        x = tuple(range(self.plot_size))

        def zeros(maxlen : int):
            for _ in range(maxlen):
                yield 0

        y = deque(zeros(maxlen = self.plot_size), maxlen = self.plot_size)
        
        plt.connect("close_event", self._onClose)
        self.life = True
        while self.life:
            y.append((yield "draw 완료... 저주파 전류값 받는 중..."))
            subplot.clear()
            subplot.set_title("저주파 전류")
            subplot.set_ylim((0,100))
            subplot.plot(x, y)
            plt.draw()
            plt.pause(0.0001)
        return self._drawer
    
    def _onClose(self, event):
        self.life = False


"""
예제 코드입니다.

"""

if __name__ == "__main__":
    from ParserCoroutine import ParserCoroutine
    from SerialWrapper import SerialWrapper
    
    with PlotCoroutine(plt.figure(figsize=[1,1])) as plot:
        with ParserCoroutine() as parser:
            with SerialWrapper("debug") as ser:
                try:
                    while True:
                        retval = parser.send( ser.read() )
                        if type(retval) is dict:
                            plot.send(retval["low frequency electric current"])
                except StopIteration:
                    pass

    



    
