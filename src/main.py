from audp import transmitter, receiver
from threading import Thread

if __name__ == "__main__":
    Thread(target=receiver.rx_loop, name="devRx").start()
    Thread(target=transmitter.tx_stdin_loop, name="devTx").start()
