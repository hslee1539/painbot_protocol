import serial
import random


def read_serial(serial: serial.Serial):
    while True:
        yield serial.read()
