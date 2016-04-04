import serial
from .parser import aeconvcmd_parse


class SerialParser:

    def __init__(self, port, timeout=1):
        self.ser = serial.Serial(port=port, timeout=timeout)

    def __del__(self):
        self.close()

    def close(self):
        self.ser.close()

    def read(self):
        escape = False
        bytelist = b""
        while self.ser.isOpen():
            cur = self.ser.read(1)
            if len(cur) > 0:
                if escape:
                    escape = False
                    bytelist += cur
                else:
                    if cur == b"\x40":
                        escape = True
                    elif cur == b"\x0D":
                        bytelist += cur
                        break
                    else:
                        bytelist += cur
        if len(bytelist) > 6 and bytelist[0] == 0x21 and bytelist[-1] == 0x0D:
            return aeconvcmd_parse(bytelist[1:-1])
        else:
            return None