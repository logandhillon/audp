"""
Analog Unicast Data Protocol (AUDP)
Copyright (c) 2024 Logan Dhillon
"""

BIT_DURATION = 0.02

# FOR PCM-BASED MODEMS
BIT_HIGH = 6000
BIT_LOW = 4000
BIT_CHUNK_END = 2000
TOLERANCE = 975

# FOR DAC-BASED MODEMS
DAC_FACTOR = 70

SAMPLE_RATE = 44100
WAVE_LENGTH = int(SAMPLE_RATE * BIT_DURATION)

bit_to_hz = lambda bit: BIT_HIGH if bit == 1 else BIT_LOW


class SampleRateMismatch(Exception):
    def __init__(self, sample_rate):
        self.message = f"Sample rate mismatch! Expected {SAMPLE_RATE}, got {sample_rate}"
        super().__init__(self.message)
