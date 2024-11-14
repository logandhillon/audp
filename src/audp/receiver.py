import sounddevice as sd
from audp import SAMPLE_RATE
from audp.modem.v1 import demodulate
from audp.packet import CTRL, Packet

buffer = []


def rx_callback(indata, frames, time, status):
    b = demodulate(indata)

    if (b != CTRL.SOH.value and len(buffer) < 1) or not b:
        # no SOH yet?                               no byte?
        return

    buffer.append(ord(b))

    if b == CTRL.ETX.value:
        try:
            packet = Packet.decode(bytes(buffer))
            print(f'from {packet.addr.decode("ascii")}: {packet.payload.decode("ascii")}')
        except Exception as e:
            print(f"{e}\ncallback info: status={status or 'OK'}, buffer={bytes(buffer)  or '<empty>'}")
        finally:
            buffer.clear()


def rx_loop():
    with sd.InputStream(callback=rx_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=882):
        while True:
            pass
