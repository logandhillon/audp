import audp
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.io import wavfile


def sine_wave(hz: float, duration: float):
    time_values = np.linspace(0, duration, int(
        audp.SAMPLE_RATE * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * hz * time_values)
    return wave


def extract_analog_signal(wave_data):
    num_waves = len(wave_data) // audp.WAVE_LENGTH
    # reshape concated array to split it
    reshaped = wave_data.reshape(num_waves, audp.WAVE_LENGTH)
    return [segment for segment in reshaped]


def extract_frequency(wave_segment, sample_rate):
    N = len(wave_segment)
    yf = fft(wave_segment)
    xf = fftfreq(N, 1 / sample_rate)

    # get peak frequency
    idx = np.argmax(np.abs(yf[:N//2]))
    freq = np.abs(xf[idx])
    return freq

def get_frequencies(analog_signal: np.ndarray):
    return [extract_frequency(segment, audp.SAMPLE_RATE) for segment in extract_analog_signal(analog_signal)]


def read_wav_file(filename: str):
    sample_rate, data = wavfile.read(filename)

    if sample_rate != audp.SAMPLE_RATE:
        raise audp.SampleRateMismatch(sample_rate)
    
    return data

def write_wav_file(filename: str, content: np.int16):
    wavfile.write(filename, audp.SAMPLE_RATE, content)