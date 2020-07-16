import serial
import random

class SerialWrapper:
    def __init__(self, portname : str):
        self.portname = portname
    
    def __enter__(self):
        self._read_debug = self.__read_debug()
        #next(self._read_debug)
        if self.portname == 'debug':
            self.read = self._read
            return self
        else:
            self._ser = serial.Serial(port = self.portname)
            self.read = self._ser.read
            self.read_all = self._ser.read_all
            self.read_until = self._ser.read_until
            self._ser.flush()
        return self

    def __exit__(self, type, value, traceback):
        if self.portname != 'debug':
            self._ser.flush()
            self._ser.close()

    def __read_debug(self):
        def generate():
            retval = [0] * 7
            retval[0] = 2
            retval[1] = b'0'[0] + random.randint(0,1)
            retval[2] = random.randint(0,3)
            retval[3] = b'0'[0] + random.randint(0,1)
            retval[4] = random.randint(0,50)
            retval[5] = b'0'[0] + random.randint(0,1)
            retval[6] = random.randint(0,100)
            
            return bytes(retval)
        while True:
            for output in generate():
                yield output

    def _read(self):
        return next(self._read_debug)
