from enum import Enum

class ParserMessage(Enum):
    FAIL = "[이전 작업 오류] 시작 문자 받는 중..."
    START = "시작 문자 받는 중..."
    MICROWAVE_MODE = "초음파 모드 받는 중..."
    MICROWAVE_VALUE = "초음파 출력값 받는 중..."
    LOWPULSE_MODE   = "저주파 모드 받는 중..."
    LOWPULSE_VALUE  = "저주파 출력값 받는 중..."
    LOWPULSE_PULSE_VALUE = "저주파 펄스 값 받는 중..."
    LOWPULSE_V_VALUE = "저주파 전류값 받는 중..."

class ParserCoroutine:
    CODE_STX    =   b'\02'[0]
    CODE_MODE_CONTINUOUS = b'0'[0]
    CODE_MODE_PULSE = b'1'[0]
    CODE_MODE_INTERVAL = b'1'[0]
    CODE_MODE_500uS = b'0'[0]
    CODE_MODE_250uS = b'1'[0]

    RANGE_MICROWAVE_MIN = 0
    RANGE_MICROWAVE_MAX = 3
    RANGE_LOWPRASE_MIN  = 0
    RANGE_LOWPULSE_MAX  = 50
    RANGE_LOWPULSE_V_MIN = 0
    RANGE_LOWPULSE_V_MAX = 100

    def __init__(self):
        pass

    def __enter__(self):
        self._parser = self._parse()
        next(self._parser)
        return self._parser

    def __exit__(self, type, value, traceback):
        pass


    def _parse(self):
        """
        ParserCoroutine._parse
        --------------------

        ## 요약

        파싱을 위한 코루틴을 만듭니다.

        ## 입력

        `int`를 받습니다.

        ## 출력

        `str` 또는 `dict` 을 받습니다.

        ##예제

        ```python
        _parser = ParserCoroutine()._parse()
        retval = _parser.send(2)
        retval = _parser.send(b'0'[0])
        ```

        """

        output = ParserMessage.START
        success_output = {
            "micro wave mode" : "continuous",
            "micro wave value": 0,
            "low frequency pulse mode"  : "continuous",
            "low frequency pulse value" : 0,
            "low frequency pulse pulse value" : "182Hz, 500uS",
            "low frequency electric current" : 0
        }
        while True:
            if ParserCoroutine.CODE_STX == (yield output):
                output = ParserMessage.MICROWAVE_MODE
                microwave_mode = (yield output)
                if microwave_mode == ParserCoroutine.CODE_MODE_CONTINUOUS or microwave_mode == ParserCoroutine.CODE_MODE_PULSE:
                    output = ParserMessage.MICROWAVE_VALUE
                    microwave_value = (yield output)
                    if ParserCoroutine.RANGE_MICROWAVE_MIN <= microwave_value <= ParserCoroutine.RANGE_MICROWAVE_MAX:
                        output = ParserMessage.LOWPULSE_MODE
                        lowpulse_mode = (yield output)
                        if lowpulse_mode == ParserCoroutine.CODE_MODE_CONTINUOUS or lowpulse_mode == ParserCoroutine.CODE_MODE_INTERVAL:
                            output = ParserMessage.LOWPULSE_VALUE
                            lowpulse_value = (yield output)
                            if ParserCoroutine.RANGE_LOWPRASE_MIN <= lowpulse_value <= ParserCoroutine.RANGE_LOWPULSE_MAX:
                                output = ParserMessage.LOWPULSE_PULSE_VALUE
                                lowpulse_pulse_value = (yield output)
                                if lowpulse_pulse_value == ParserCoroutine.CODE_MODE_500uS or lowpulse_pulse_value == ParserCoroutine.CODE_MODE_250uS:
                                    output = ParserMessage.LOWPULSE_V_VALUE
                                    lowpulse_v_value = (yield output)
                                    if ParserCoroutine.RANGE_LOWPULSE_V_MIN <= lowpulse_v_value <= ParserCoroutine.RANGE_LOWPULSE_V_MAX:
                                        if microwave_mode == ParserCoroutine.CODE_MODE_CONTINUOUS:
                                            success_output["micro wave mode"] = "continuous"
                                        else:
                                            success_output["micro wave mode"] = "pulse"

                                        success_output["micro wave value"] = microwave_value

                                        if lowpulse_mode == ParserCoroutine.CODE_MODE_CONTINUOUS:
                                            success_output["low frequency pulse mode"] = "continuous"
                                        else:
                                            success_output["low frequency pulse mode"] = "interval"
                                        
                                        success_output["low frequency pulse value"] = lowpulse_value

                                        if lowpulse_pulse_value == ParserCoroutine.CODE_MODE_500uS:
                                            success_output["low frequency pulse pulse value"] = "182Hz,500uS"
                                        else:
                                            success_output["low frequency pulse pulse value"] = "182Hz,250uS"
                                        
                                        success_output["low frequency electric current"] = lowpulse_v_value
                                        output = success_output.copy()
                                    else:
                                        output = ParserMessage.FAIL
                                else:
                                    output = ParserMessage.FAIL
                            else:
                                output = ParserMessage.FAIL
                        else:
                            output = ParserMessage.FAIL
                    else:
                        output = ParserMessage.FAIL
                else:
                    output = ParserMessage.FAIL
            else:
                output = ParserMessage.FAIL
    
    def parse(self, value : int):
        return self._parser.send(value)


"""
예제 코드입니다.
"""
if __name__ == "__main__":
    
    import SerialWrapper
    import time

    with SerialWrapper.SerialWrapper("debug") as serial:
        parser = ParserCoroutine()
        with ParserCoroutine() as parser:
            while True:
                print(parser.send(serial.read()))
                time.sleep(1)
        #while True:
        #    print(parser.parse(serial.read()))
        #    time.sleep(1)




