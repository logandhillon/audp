"""
Resilient AUDP Encoder-Decoder, version 0 beta release
Encodes via AUDP/0.9, see the AUDP spec for specifics
Copyright (c) 2024 Logan Dhillon
"""

import numpy as np
from . import sine_wave, get_frequencies, read_wav_file, write_wav_file
import audp
from typing import List

BIT_HIGH = 6000
BIT_LOW = 4000
BIT_CHUNK_END = 2000
TOLERANCE = 975


def bit_to_hz(bit): return BIT_HIGH if bit == 1 else BIT_LOW


low_min, low_max = BIT_LOW - TOLERANCE, BIT_LOW + TOLERANCE
high_min, high_max = BIT_HIGH - \
    TOLERANCE, BIT_HIGH + TOLERANCE
end_min, end_max = BIT_CHUNK_END - \
    TOLERANCE, BIT_CHUNK_END + TOLERANCE


def digitize_frequency(hz: np.float64) -> int:
    if low_min <= hz <= low_max:
        return 0
    elif high_min <= hz <= high_max:
        return 1
    elif end_min <= hz <= end_max:
        return 2
    else:
        return -1


def digitize_frequencies(frequencies: List[float]) -> List[List[int]]:
    bits = []
    bytes_array = []

    for freq in frequencies:
        bit = digitize_frequency(freq)
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


def encode(bytes: bytes):
    payload = []

    for byte in bytes:
        for bit in bin(byte)[2:]:
            payload.append(
                sine_wave(bit_to_hz(int(bit)), audp.BIT_DURATION))

        payload.append(sine_wave(BIT_CHUNK_END, audp.BIT_DURATION))

    return np.int16(np.concatenate(payload) * 32767)    # 16-bit PCM format


def decode(analog_signal: np.ndarray):
    data = digitize_frequencies(get_frequencies(analog_signal))
    bytes_array = [bytes([int(''.join(map(str, bits)), 2)]) for bits in data]
    return b''.join(bytes_array)


if __name__ == "__main__":
    import os
    directory = 'out'

    if not os.path.exists(directory):
        os.makedirs(directory)

    FILE_NAME = "out/audp_packet.wav"

    print(f"\n== ENCODING ({FILE_NAME}) ==")
    write_wav_file(FILE_NAME, encode(b'Hello, world!'))
    print(f"Exported preloaded sample text to '{FILE_NAME}'")

    print(f"\n== DECODING ({FILE_NAME}) ==")
    print("Attempted to decode, got this:", decode(read_wav_file(FILE_NAME)))
