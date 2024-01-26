from enum import Enum
from dataclasses import dataclass


class ParserMessage(Enum):
    FAIL = "[이전 작업 오류] 시작 문자 받는 중..."
    START = "시작 문자 받는 중..."
    MICROWAVE_MODE = "초음파 모드 받는 중..."
    MICROWAVE_VALUE = "초음파 출력값 받는 중..."
    LOWPULSE_MODE = "저주파 모드 받는 중..."
    LOWPULSE_VALUE = "저주파 출력값 받는 중..."
    LOWPULSE_PULSE_VALUE = "저주파 펄스 값 받는 중..."
    LOWPULSE_V_VALUE = "저주파 전류값 받는 중..."
    END = "(option) 마지막 문자 받는 중..."


class PainMicrowaveMode(Enum):
    CONTINUOUS = b"0"[0]
    PULSE = b"1"[0]


class PainLowPulseMode(Enum):
    CONTINUOUS = b"0"[0]
    INTERVAL = b"1"[0]


class PainLowPulsePulse(Enum):
    PULSE_182Hz_500uS = b"0"[0]
    PULSE_182Hz_250uS = b"1"[0]


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
class ImmutablePainState:
    microwave_mode: PainMicrowaveMode = PainMicrowaveMode.CONTINUOUS
    microwave: int = 0
    lowpulse_mode: PainLowPulseMode = PainLowPulseMode.CONTINUOUS
    lowpulse: int = 0
    lowpulse_pulse: PainLowPulsePulse = PainLowPulsePulse.PULSE_182Hz_500uS
    lowpulse_v: int = 0


# ui state
@dataclass(frozen=True)
class PlotState:
    xs: list[int]
    ys: list[float]
    y_lim: tuple[int, int]
