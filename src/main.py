from threading import Thread
from audp.communicator import LocalCommunicator

lcomm = LocalCommunicator()


def rx():
    while True:
        print(lcomm.recv())


def tx():
    while True:
        lcomm.send(b'?', input("> ").encode('ascii'))


if __name__ == "__main__":
    Thread(target=rx, name="lcomm#rx").start()
    Thread(target=tx, name="lcomm#tx").start()
