from core_data import (
    ParserMessage,
    MutableParserState,
    ImmutablePainState,
    PainMicrowaveMode,
    PainLowPulseMode,
    PainLowPulsePulse,
)
from typing import Generator


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
            return ParserMessage.END
        case ParserMessage.END:
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
        case ParserMessage.END:
            if next == 3:
                state.message = _next_message(state.message)
            elif next == 2:
                state.message = _next_message(ParserMessage.START)
            else:
                state.message = ParserMessage.FAIL
        case _:  # FAIL, START
            if next == 2:
                state.message = _next_message(state.message)
            else:
                state.message = ParserMessage.FAIL


def flatmap_parse(data: Generator[int, None, None]):
    state = MutableParserState()
    is_last = False
    for next in data:
        is_last = state.message == ParserMessage.END
        _update_state(state, next)
        yield state.message
        if is_last and state.message == ParserMessage.START:
            yield ImmutablePainState(
                state.microwave_mode,
                state.microwave,
                state.lowpulse_mode,
                state.lowpulse,
                state.lowpulse_pulse,
                state.lowpulse_v,
            )
    # empty 
    if not is_last and state.message == ParserMessage.END:
        yield ImmutablePainState(
            state.microwave_mode,
            state.microwave,
            state.lowpulse_mode,
            state.lowpulse,
            state.lowpulse_pulse,
            state.lowpulse_v,
        )
