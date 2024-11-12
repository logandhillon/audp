"""
Efficient AUDP Encoder-Decoder, version 1
Encodes via AUDP/1.0, see the AUDP spec for specifics
Copyright (c) 2024 Logan Dhillon
"""

import numpy as np
import audp
from . import sine_wave, get_frequencies, read_wav_file, write_wav_file
from typing import List

FACTOR = 70


def digitize_signal(frequencies: List[float]) -> bytes:
    bytes_array = []

    for freq in frequencies:
        bytes_array.append(round(freq / FACTOR).to_bytes())

    return b''.join(bytes_array)


def encode(bytes: bytes):
    payload = []

    for byte in bytes:
        payload.append(sine_wave(byte * FACTOR, audp.BIT_DURATION))

    return np.int16(np.concatenate(payload) * 32767)


def decode(analog_signal: np.ndarray):
    return digitize_signal(get_frequencies(analog_signal))


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
