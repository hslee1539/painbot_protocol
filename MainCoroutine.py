import ParserCoroutine
import SerialWrapper
import PlotCoroutine
import matplotlib.pyplot as plt

class MainCoroutine:
    """
    메인 코루틴 클래스입니다.

    ## 참고
    메인 UI에서 사용합니다.

    만약 데이터 UI 쓰래드를 분리하고 싶으면

    ```
    data = 
    def thread():
        global 
        with ParserCoroutine() as parser:
            with SerialWrapper() as serial:
                try:
                    while True:
                        serial
                    
    with
    ```

    """
    def __init__(self, portName : str, fig : plt.Figure, plot_size = 100):
        """
        메인 코루틴 클래스를 생성합니다.

        """
        self.portName = portName
        self.plot_size = plot_size
        self.fig = fig

    def __enter__(self):
        self.parser = ParserCoroutine.ParserCoroutine()
        self.plot = PlotCoroutine.PlotCoroutine(self.fig, self.plot_size)
        self.mainRoutine = self._mainRoutine()
        return self.mainRoutine

    def __exit__(self, type, value, traceback):
        pass

    def _mainRoutine(self):
        with self.plot as plotRoutine:
            with self.parser as parserRoutine:
                with SerialWrapper.SerialWrapper(self.portName) as ser:
                    while self.plot.life:
                        byteData = ser.read()
                        retval = parserRoutine.send(byteData)
                        if type(retval) is dict:
                            retval = plotRoutine.send(retval["low frequency electric current"])
                        yield retval
        return None

"""
예제입니다.

"""
if __name__ == "__main__":
    try:
        with MainCoroutine(portName="debug", fig=plt.figure(figsize=[1,1]), plot_size= 100) as main:
            for retval in main:
                print(retval) # 프로세싱 과정을 출력함

    except StopIteration:
        # 더이상 반복할 작업이 없음 (종료됨.)
        pass

    except RuntimeError:
        pass