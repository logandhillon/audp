from queue import Queue
from time import sleep
from audp.modem.v1 import modulate, demodulate
import sounddevice as sd
from audp import SAMPLE_RATE, WAVE_LENGTH
from audp.packet import CTRL, Packet


def chirp(packet: Packet):
    sd.play(modulate(packet.encode()), SAMPLE_RATE)
    sd.wait()


class LocalCommunicator:
    def __init__(self) -> None:
        self.last_recv = None   # last received packet
        self.rbuf = []          # received bytes buffer
        self.rqueue = Queue()   # received packet queue

    def send(self, addr: bytes, payload: bytes):
        i = 0
        for byte in payload:
            print(f"sending byte {i}")
            chirp(Packet(addr, byte.to_bytes()))

            print("Waiting for ACK...")
            while not self.last_recv:
                sleep(0.2)
                chirp(Packet(addr, byte.to_bytes()))
            print("last packet:", self.last_recv)
            i += 1

    def recv(self) -> Packet:
        with sd.InputStream(callback=self.rx_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=WAVE_LENGTH):
            while True:
                if self.rqueue.qsize() == 0:
                    continue
                return self.rqueue.get()

    def rx_callback(self, indata, frames, time, status):
        b = demodulate(indata)

        if (b != CTRL.SOH.value and len(self.rbuf) < 1) or not b:
            # no SOH yet?                               no byte?
            return

        self.rbuf.append(ord(b))

        if b == CTRL.ETX.value:
            try:
                packet = Packet.decode(bytes(self.rbuf))
                self.rqueue.put(packet)
                chirp(Packet(b'sys', CTRL.ACK.value))
            except Exception as e:
                print(f"{e}\ncallback info: status={status or 'OK'}, buffer={bytes(self.rbuf)  or '<empty>'}")
            finally:
                self.rbuf.clear()
