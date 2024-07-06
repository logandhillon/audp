"""
Analog Unicast Data Protocol (AUDP)
Copyright (c) 2024 Logan Dhillon
"""

from numpy import float64
from typing import List, Literal

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

def hz_to_bit(hz: float64) -> Literal[0, 1, 2, -1]:
    if (BIT_LOW - TOLERANCE) <= hz <= (BIT_LOW + TOLERANCE):
        return 0
    elif (BIT_HIGH - TOLERANCE) <= hz <= (BIT_HIGH + TOLERANCE):
        return 1
    elif (BIT_CHUNK_END - TOLERANCE) <= hz <= (BIT_CHUNK_END + TOLERANCE):
        return 2
    else:
        return -1
    

def pcm_to_bits(frequencies: List[float]) -> List[List[int]]:
    bits = []
    bytes_array = []

    for freq in frequencies:
        bit = hz_to_bit(freq)
        if bit == 2:
            if bits:
                bytes_array.append(bits)
                bits = []
        elif bit == -1:
            continue
        else:
            bits.append(bit)
    
    if bits:
        bytes_array.append(bits)
    
    return bytes_array


def pcm_to_bytes(frequencies: List[float]) -> bytes:
    data = pcm_to_bits(frequencies)
    bytes_array = [bytes([int(''.join(map(str, bits)), 2)]) for bits in data]
    return b''.join(bytes_array)


def dac_to_bytes(frequencies: List[float]) -> bytes:
    bytes_array = []

    for freq in frequencies:
        bytes_array.append(round(freq / DAC_FACTOR).to_bytes())
    
    return b''.join(bytes_array)


class SampleRateMismatch(Exception):
    def __init__(self, sample_rate):
        self.message = f"Sample rate mismatch! Expected {SAMPLE_RATE}, got {sample_rate}"
        super().__init__(self.message)
