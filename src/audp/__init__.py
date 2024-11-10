"""
Analog Unicast Data Protocol (AUDP)
Copyright (c) 2024 Logan Dhillon
"""

BIT_DURATION = 0.02
SAMPLE_RATE = 44100
WAVE_LENGTH = int(SAMPLE_RATE * BIT_DURATION)


class SampleRateMismatch(Exception):
    def __init__(self, sample_rate):
        self.message = f"Sample rate mismatch! Expected {SAMPLE_RATE}, got {sample_rate}"
        super().__init__(self.message)
