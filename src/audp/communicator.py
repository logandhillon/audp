from queue import Queue
from audp.modem.v1 import modulate, demodulate
import sounddevice as sd
from audp import SAMPLE_RATE
from audp.packet import CTRL, Packet

buffer = []
queue = Queue()


def rx_callback(indata, frames, time, status):
    b = demodulate(indata)

    if (b != CTRL.SOH.value and len(buffer) < 1) or not b:
        # no SOH yet?                               no byte?
        return

    buffer.append(ord(b))

    if b == CTRL.ETX.value:
        try:
            packet = Packet.decode(bytes(buffer))
            queue.put(packet)
        except Exception as e:
            print(f"{e}\ncallback info: status={status or 'OK'}, buffer={bytes(buffer)  or '<empty>'}")
        finally:
            buffer.clear()


class LocalCommunicator:
    @staticmethod
    def send(packet: Packet):
        sd.play(modulate(packet.encode()), SAMPLE_RATE)
        sd.wait()

    @staticmethod
    def recv() -> Packet:
        with sd.InputStream(callback=rx_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=882):
            # check for a packet in the queue, if empty keep waiting
            while True:
                if queue.qsize() == 0:
                    continue
                packet = queue.get(timeout=1)
                return packet
