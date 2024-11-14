from enum import Enum


class CTRL(Enum):
    SOH = b'\x01'
    STX = b'\x02'
    ETX = b'\x03'
    ACK = b'\x06'


class PacketDecodeError(Exception):
    def __init__(self, reason: str, packet: bytes):
        super().__init__(f"Failed to decode AUDP packet: {reason}\npacket={packet}")


class Packet:
    def __init__(self, addr: bytes, payload: bytes) -> None:
        self.addr = addr
        self.payload = payload

    def encode(self) -> bytes:
        return CTRL.SOH.value + self.addr + CTRL.STX.value + self.payload + CTRL.ETX.value

    @staticmethod
    def decode(packet: bytes):
        if packet[0] == ord(CTRL.SOH.value) and packet[-1] is ord(CTRL.ETX.value):
            parts = packet[1:-1].split(CTRL.STX.value)
            if len(parts) < 2:
                raise PacketDecodeError("payload missing", packet)
            return Packet(parts[0], parts[1])
        raise PacketDecodeError(f"SOH or ETX byte missing. got bytes {packet[0]}..{packet[-1]}", packet)

    def __str__(self) -> str:
        return f"Packet<addr={self.addr}, payload={self.payload}>"
