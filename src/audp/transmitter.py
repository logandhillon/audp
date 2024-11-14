import sounddevice as sd
from audp.modem.v1 import modulate
from audp import SAMPLE_RATE
from audp.packet import Packet


def tx_stdin_loop():
    while True:
        sd.play(modulate(Packet(b'?', input("> ").encode('ascii')).encode()), SAMPLE_RATE)
        sd.wait()


if __name__ == "__main__":
    tx_stdin_loop()
