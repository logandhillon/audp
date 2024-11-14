from threading import Thread
from audp.packet import Packet
from audp.communicator import LocalCommunicator


def rx():
    while True:
        print("incoming:", LocalCommunicator.recv())


def tx():
    while True:
        LocalCommunicator.send(Packet(b'?', input("> ").encode('ascii')))


if __name__ == "__main__":
    Thread(target=rx, name="commRx").start()
    Thread(target=tx, name="commTx").start()
