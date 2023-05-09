from collections import deque
import serial
import time
import numpy
import math

class SerialSender:
    def __init__(self, device = 'COM6'):
        self.Serial = serial.Serial(device, 115200, timeout=.1)
        time.sleep(2)
        self.BufferSize = 64  # in bytes
        self.BufferQueue = deque()
        self.BufferFilled = 0  # in bytes

        self.command_size = 1  # in bytes
        self.coordinate_size = 2  # in bytes

        self.baseX = int((2 ** (8 * self.coordinate_size - 1)))
        self.baseY = int((2 ** (8 * self.coordinate_size - 1)))
        self.base = numpy.array([self.baseX, self.baseY])

        self.steps_per_mm_XY = numpy.array([40.0, 40.0])

        theta = numpy.deg2rad(-45)
        self.rotation_matrix = numpy.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        self.board_square_size = 36  # in mm


    def getPackedCoordinates(self, command, coordinates):
        vraceni = bytearray()
        vraceni.extend(command.to_bytes(self.command_size, byteorder='big'))
        vraceni.extend(int(coordinates[0]).to_bytes(self.coordinate_size, byteorder='big'))
        vraceni.extend(int(coordinates[1]).to_bytes(self.coordinate_size, byteorder='big'))
        return vraceni

    def coordinates_to_core_XY(self, coordinates):
        new_coordinates = numpy.array(coordinates, dtype=float)
        new_coordinates = numpy.flip(new_coordinates)
        new_coordinates = new_coordinates * self.steps_per_mm_XY
        new_coordinates = new_coordinates * self.board_square_size
        new_coordinates = numpy.dot(self.rotation_matrix, new_coordinates)
        new_coordinates = new_coordinates*(2**(0.5))

        new_coordinates = new_coordinates.astype(int) + self.base
        return new_coordinates


    def __clearBuffer(self):
        if self.Serial.in_waiting:
            serVstup = self.Serial.read()
            if serVstup == (69).to_bytes(1, byteorder='big'):
                self.BufferFilled -= self.BufferQueue.popleft()
                print("buffer cleared")
                return True
            elif serVstup == (42).to_bytes(1, byteorder='big'):
                response = self.Serial.readline().decode('UTF-8').rstrip()
                print(response)
        return False

    def send_move(self, coordinates):
        msg_size = self.command_size + 2*self.coordinate_size
        new_coordinates = self.coordinates_to_core_XY(coordinates)
        while self.BufferFilled + msg_size > self.BufferSize:
            self.__clearBuffer()
        self.Serial.write(self.getPackedCoordinates(1, new_coordinates))
        self.BufferQueue.append(msg_size)
        self.BufferFilled += msg_size
        print(self.BufferFilled)

    def send_bare_command(self, command):
        msg_size = self.command_size
        while self.BufferFilled + msg_size > self.BufferSize:
            self.__clearBuffer()
        msg = bytearray()
        msg.extend((command).to_bytes(self.command_size, byteorder='big'))
        self.Serial.write(msg)
        self.BufferQueue.append(msg_size)
        self.BufferFilled += msg_size
        print(self.BufferFilled)

def main():
    sender = SerialSender('COM7')
    sender.send_bare_command(5)
    for a in range(8):
        sender.send_move((0, 3))
        sender.send_move((3, 3))
        sender.send_move((3, 0))
        sender.send_move((0, 0))
    sender.send_bare_command(4)


if __name__ == "__main__":
    main()