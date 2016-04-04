import serial
from aeconversion import SerialParser

if __name__ == "__main__":

    serial_parser = SerialParser(4)
    while True:
        print(serial_parser.read())