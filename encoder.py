"""
AUDP Encoder-Decoder, first version
Encodes via PCM, see the AUDP spec for specifics
Copyright (c) 2024 Logan Dhillon
"""

import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import audp
import os

directory = 'out'

if not os.path.exists(directory):
    os.makedirs(directory)


FILE_NAME = "out/audp_packet.wav"


def sine_wave(hz: float, duration: float):
    time_values = np.linspace(0, duration, int(
        audp.SAMPLE_RATE * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * hz * time_values)
    return wave


def encode(bytes: bytes):
    print(f'Encoding {bytes}')
    payload = []

    for byte in bytes:
        for bit in bin(byte)[2:]:
            payload.append(sine_wave(audp.bit_to_hz(int(bit)), audp.BIT_DURATION))

    return np.concatenate(payload)


def extract_analog_signal(wave_data):
    num_waves = len(wave_data) // audp.WAVE_LENGTH
    reshaped = wave_data.reshape(num_waves, audp.WAVE_LENGTH)   # reshape concated array to split it
    return [segment for segment in reshaped]


def extract_frequency(wave_segment, sample_rate):
    N = len(wave_segment)
    yf = fft(wave_segment)
    xf = fftfreq(N, 1 / sample_rate)

    # get peak frequency
    idx = np.argmax(np.abs(yf[:N//2]))
    freq = np.abs(xf[idx])
    return freq


def decode(analog_signal: np.ndarray):
    return [extract_frequency(segment, audp.SAMPLE_RATE) for segment in extract_analog_signal(analog_signal)]


if __name__ == "__main__":
    print(f"\n== ENCODING ({FILE_NAME}) ==")
    encoded = encode(b'Hello, world!')

    combined_wave_int16 = np.int16(encoded * 32767)    # 16-bit PCM format

    wavfile.write(FILE_NAME, audp.SAMPLE_RATE, combined_wave_int16)
    print(f"Exported preloaded sample text to '{FILE_NAME}'")

    print(f"\n== DECODING ({FILE_NAME}) ==")

    sample_rate, data = wavfile.read(FILE_NAME)

    if sample_rate != audp.SAMPLE_RATE:
        raise audp.SampleRateMismatch(sample_rate)

    frequencies = decode(data)
    print("Attempted to decode, got this:", audp.analog_to_bytes(frequencies))
