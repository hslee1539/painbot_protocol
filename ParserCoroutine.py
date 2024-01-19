from enum import Enum
from typing import Generator
from dataclasses import dataclass

class ParserMessage(Enum):
    FAIL = "[이전 작업 오류] 시작 문자 받는 중..."
    START = "시작 문자 받는 중..."
    MICROWAVE_MODE = "초음파 모드 받는 중..."
    MICROWAVE_VALUE = "초음파 출력값 받는 중..."
    LOWPULSE_MODE   = "저주파 모드 받는 중..."
    LOWPULSE_VALUE  = "저주파 출력값 받는 중..."
    LOWPULSE_PULSE_VALUE = "저주파 펄스 값 받는 중..."
    LOWPULSE_V_VALUE = "저주파 전류값 받는 중..."

class PainMicrowaveMode(Enum):
    CONTINUOUS = b'0'[0]
    PULSE = b'1'[0]

class PainLowPulseMode(Enum):
    CONTINUOUS = b'0'[0]
    INTERVAL = b'1'[0]

class PainLowPulsePulse(Enum):
    PULSE_182Hz_500uS = b'0'[0]
    PULSE_182Hz_250uS = b'1'[0]

@dataclass(frozen=False)
class MutableParserState:
    message: ParserMessage = ParserMessage.START
    microwave_mode: PainMicrowaveMode = PainMicrowaveMode.CONTINUOUS
    microwave: int = 0
    lowpulse_mode: PainLowPulseMode = PainLowPulseMode.CONTINUOUS
    lowpulse: int = 0
    lowpulse_pulse: PainLowPulsePulse = PainLowPulsePulse.PULSE_182Hz_500uS
    lowpulse_v: int = 0

@dataclass(frozen=True)
class ImutablePainState:
    microwave_mode: PainMicrowaveMode = PainMicrowaveMode.CONTINUOUS
    microwave: int = 0
    lowpulse_mode: PainLowPulseMode = PainLowPulseMode.CONTINUOUS
    lowpulse: int = 0
    lowpulse_pulse: PainLowPulsePulse = PainLowPulsePulse.PULSE_182Hz_500uS
    lowpulse_v: int = 0


def flatten(data: Generator[bytes, None, None]):
    for byte_array in data:
        for byte_item in byte_array:
            yield byte_item

def _next_message(message: ParserMessage):
    match message:
        case ParserMessage.FAIL:
            return ParserMessage.MICROWAVE_MODE
        case ParserMessage.START:
            return ParserMessage.MICROWAVE_MODE
        case ParserMessage.MICROWAVE_MODE:
            return ParserMessage.MICROWAVE_VALUE
        case ParserMessage.MICROWAVE_VALUE:
            return ParserMessage.LOWPULSE_MODE
        case ParserMessage.LOWPULSE_MODE:
            return ParserMessage.LOWPULSE_VALUE
        case ParserMessage.LOWPULSE_VALUE:
            return ParserMessage.LOWPULSE_PULSE_VALUE
        case ParserMessage.LOWPULSE_PULSE_VALUE:
            return ParserMessage.LOWPULSE_V_VALUE
        case ParserMessage.LOWPULSE_V_VALUE:
            return ParserMessage.START

def _update_state(state: MutableParserState, next: int):
    match state.message:
        case ParserMessage.MICROWAVE_MODE:
            if next == PainMicrowaveMode.CONTINUOUS.value:
                state.microwave_mode = PainMicrowaveMode.CONTINUOUS
                state.message = _next_message(state.message)
            elif next == PainMicrowaveMode.PULSE.value:
                state.microwave_mode = PainMicrowaveMode.PULSE
                state.message = _next_message(state.message)
            else:
                state.message = ParserMessage.FAIL
        case ParserMessage.MICROWAVE_VALUE:
            if next in range(0, 3 + 1):
                state.microwave = next
                state.message = _next_message(state.message)
            else:
                state.message = ParserMessage.FAIL
        case ParserMessage.LOWPULSE_MODE:
            if next == PainLowPulseMode.CONTINUOUS.value:
                state.lowpulse_mode = PainLowPulseMode.CONTINUOUS
                state.message = _next_message(state.message)
            elif next == PainLowPulseMode.INTERVAL.value:
                state.lowpulse_mode = PainLowPulseMode.INTERVAL
                state.message = _next_message(state.message)
            else:
                state.message = ParserMessage.FAIL
        case ParserMessage.LOWPULSE_VALUE:
            if next in range(0, 50 + 1):
                state.lowpulse = next
                state.message = _next_message(state.message)
            else:
                state.message = ParserMessage.FAIL
        case ParserMessage.LOWPULSE_PULSE_VALUE:
            if next == PainLowPulsePulse.PULSE_182Hz_500uS.value:
                state.lowpulse_pulse = PainLowPulsePulse.PULSE_182Hz_500uS
                state.message = _next_message(state.message)
            elif next == PainLowPulsePulse.PULSE_182Hz_250uS.value:
                state.lowpulse_pulse = PainLowPulsePulse.PULSE_182Hz_250uS
                state.message = _next_message(state.message)
            else:
                state.message = ParserMessage.FAIL
        case ParserMessage.LOWPULSE_V_VALUE:
            if next in range(0, 100 + 1):
                state.lowpulse_v = next
                state.message = _next_message(state.message)
            else:
                state.message = ParserMessage.FAIL
        case _: # FAIL, START
            if next == 2:
                state.message = _next_message(state.message)
            else:
                state.message = ParserMessage.FAIL

def flatmap_parse(data: Generator[int, None, None]):
    state = MutableParserState()
    for next in data:
        is_last = state.message == ParserMessage.LOWPULSE_V_VALUE
        _update_state(state, next)
        yield state.message
        if is_last and state.message == ParserMessage.START:
            yield ImutablePainState(
                state.microwave_mode,
                state.microwave,
                state.lowpulse_mode,
                state.lowpulse,
                state.lowpulse_pulse,
                state.lowpulse_v
            )
