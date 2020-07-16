class Parser:
    MESSAGE_FAIL = "[이전 작업 오류] 시작 문자 받는 중..."
    MESSAGE_START = "시작 문자 받는 중..."
    MESSAGE_MICROWAVE_MODE = "초음파 모드 받는 중..."
    MESSAGE_MICROWAVE_VALUE = "초음파 출력값 받는 중..."
    MESSAGE_LOWPULSE_MODE   = "저주파 모드 받는 중..."
    MESSAGE_LOWPULSE_VALUE  = "저주파 출력값 받는 중..."
    MESSAGE_LOWPULSE_PULSE_VALUE = "저주파 펄스 값 받는 중..."
    MESSAGE_LOWPULSE_V_VALUE = "저주파 전류값 받는 중..."

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
        self._parser = self._parse()
        next(self._parser)
        pass

    def _parse(self):
        """
        # Parser._parse

        ## 요약

        파싱을 위한 코루틴을 만듭니다.

        ## 입력

        `int`를 받습니다.

        ## 출력

        `str` 또는 `dict` 을 받습니다.

        ##예제

        ```python
        _parser = Parser()._parse()
        retval = _parser.send(2)
        retval = _parser.send(b'0'[0])
        ```

        """

        output = Parser.MESSAGE_START
        success_output = {
            "micro wave mode" : "continuous",
            "micro wave value": 0,
            "low pulse mode"  : "continuous",
            "low pulse value" : 0,
            "low pulse pulse value" : "182Hz, 500uS",
            "low pulse v value" : 0
        }
        while True:
            if Parser.CODE_STX == (yield output):
                output = Parser.MESSAGE_MICROWAVE_MODE
                microwave_mode = (yield output)
                if microwave_mode == Parser.CODE_MODE_CONTINUOUS or microwave_mode == Parser.CODE_MODE_PULSE:
                    output = Parser.MESSAGE_MICROWAVE_VALUE
                    microwave_value = (yield output)
                    if Parser.RANGE_MICROWAVE_MIN <= microwave_value <= Parser.RANGE_MICROWAVE_MAX:
                        output = Parser.MESSAGE_LOWPULSE_MODE
                        lowpulse_mode = (yield output)
                        if lowpulse_mode == Parser.CODE_MODE_CONTINUOUS or lowpulse_mode == Parser.CODE_MODE_INTERVAL:
                            output = Parser.MESSAGE_LOWPULSE_VALUE
                            lowpulse_value = (yield output)
                            if Parser.RANGE_LOWPRASE_MIN <= lowpulse_value <= Parser.RANGE_LOWPULSE_MAX:
                                output = Parser.MESSAGE_LOWPULSE_PULSE_VALUE
                                lowpulse_pulse_value = (yield output)
                                if lowpulse_pulse_value == Parser.CODE_MODE_500uS or lowpulse_pulse_value == Parser.CODE_MODE_250uS:
                                    output = Parser.MESSAGE_LOWPULSE_V_VALUE
                                    lowpulse_v_value = (yield output)
                                    if Parser.RANGE_LOWPULSE_V_MIN <= lowpulse_v_value <= Parser.RANGE_LOWPULSE_V_MAX:
                                        if microwave_mode == Parser.CODE_MODE_CONTINUOUS:
                                            success_output["micro wave mode"] = "continuous"
                                        else:
                                            success_output["micro wave mode"] = "pulse"

                                        success_output["micro wave value"] = microwave_value

                                        if lowpulse_mode == Parser.CODE_MODE_CONTINUOUS:
                                            success_output["low pulse mode"] = "continuous"
                                        else:
                                            success_output["low pulse mode"] = "interval"
                                        
                                        success_output["low pulse value"] = lowpulse_value

                                        if lowpulse_pulse_value == Parser.CODE_MODE_500uS:
                                            success_output["low pulse pulse value"] = "182Hz,500uS"
                                        else:
                                            success_output["low pulse pulse value"] = "182Hz,250uS"
                                        
                                        success_output["low pulse v value"] = lowpulse_v_value
                                        output = success_output.copy()
                                    else:
                                        output = Parser.MESSAGE_FAIL
                                else:
                                    output = Parser.MESSAGE_FAIL
                            else:
                                output = Parser.MESSAGE_FAIL
                        else:
                            output = Parser.MESSAGE_FAIL
                    else:
                        output = Parser.MESSAGE_FAIL
                else:
                    output = Parser.MESSAGE_FAIL
            else:
                output = Parser.MESSAGE_FAIL
    
    def parse(self, value : int):
        return self._parser.send(value)



if __name__ == "__main__":
    import SerialWrapper
    import time

    with SerialWrapper.SerialWrapper("debug") as serial:
        parser = Parser()
        while True:
            print(parser.parse(serial.read()))
            time.sleep(1)




