from collections import deque
import serial
import time
import numpy
import math

class SerialSender:
    BUFFER_SIZE = 64  # in bytes
    COMMAND_SIZE = 1  # in bytes
    COORDINATE_SIZE = 3  # in bytes (max size of number to be sent as number of steps)
    # for COORDINATE_SIZE=2 and self.steps_per_mm_XY=40: max range = (-579.26, 579.26) mm
    # for COORDINATE_SIZE=3 and self.steps_per_mm_XY=80: max range = (-74145.52, 74145.52) mm
    SPEED_SIZE = 2  # in bytes
    ACCELERATION_SIZE = 2 # in bytes

    STEPS_PER_MM_XY = numpy.array([40.0, 40.0])
    BASE = numpy.array([int((2 ** (8 * COORDINATE_SIZE - 1))), int((2 ** (8 * COORDINATE_SIZE - 1)))])
    THETA = numpy.deg2rad(-45)
    ROTATION_MATRIX = numpy.array([[math.cos(THETA), -math.sin(THETA)], [math.sin(THETA), math.cos(THETA)]])
    BOARD_SQUARE_SIZE = 36  # in mm

    def __init__(self, device = 'COM6'):
        self.Serial = serial.Serial(device, 115200, timeout=.1)
        time.sleep(2)
        self.BufferQueue = deque()
        self.BufferFilled = 0  # in bytes
        self.board_square_size = 36  # in mm

    def __get_packed_coordinates(self, command: int, coordinates: numpy.ndarray) -> bytearray:
        """
        :param command: command number, in case of simple movement: command = 1
        :param coordinates: 2 int coordinates in a tuple/array/numpy array. for example: (1432, 1230)
        :return: byte array ready to be sent via Serial.
        """
        vraceni = bytearray()
        vraceni.extend(command.to_bytes(self.COMMAND_SIZE, byteorder='big'))
        vraceni.extend(int(coordinates[0]).to_bytes(self.COORDINATE_SIZE, byteorder='big'))
        vraceni.extend(int(coordinates[1]).to_bytes(self.COORDINATE_SIZE, byteorder='big'))
        return vraceni

    def __coordinates_to_core_XY(self, coordinates: numpy.ndarray) -> numpy.ndarray:
        """
        Rotates, scales and translates coordinates.
        rotation: -45°
        scale: sqrt(2) * board_square_size * steps_per_mm_XY
        translation: base (the rotation would otherwise reach negative numbers not suitable for sending as unsigned int (harder to parse on arduino))
        :param coordinates: coordinates on the chess board (0-7, 0-7). units: chessboard squares.
        :return: coordinates for core-xy cnc machine. units: steps (for stepper motors)
        """
        new_coordinates = numpy.array(coordinates, dtype=float)
        new_coordinates = numpy.flip(new_coordinates)
        new_coordinates = new_coordinates * self.STEPS_PER_MM_XY
        new_coordinates = new_coordinates * self.board_square_size
        new_coordinates = numpy.dot(self.ROTATION_MATRIX, new_coordinates)
        new_coordinates = new_coordinates*(2**(0.5))

        new_coordinates = new_coordinates.astype(int) + self.BASE
        return new_coordinates


    def __clearBuffer(self):
        """
        checks whether the arduino has completed a command.
        If so, this function then adjusts the internal representation of arduino buffer.
        It can also read any string message arduino sends starting with the byte 42.
        :return: true if the buffer has been cleared. False otherwise.
        """
        if self.Serial.in_waiting:
            serVstup = self.Serial.read()
            if serVstup == (69).to_bytes(1, byteorder='big'):
                self.BufferFilled -= self.BufferQueue.popleft()
                return True
            elif serVstup == (42).to_bytes(1, byteorder='big'):
                response = self.Serial.readline().decode('UTF-8').rstrip()
                print(response)
        return False

    def send_bytearray(self, msg):
        msg_size = len(msg)
        print(msg_size)
        while self.BufferFilled + msg_size > self.BUFFER_SIZE:
            self.__clearBuffer()
        self.Serial.write(msg)
        self.BufferQueue.append(msg_size)
        self.BufferFilled += msg_size

    def send_move(self, coordinates):
        new_coordinates = self.__coordinates_to_core_XY(coordinates)
        self.send_bytearray(self.__get_packed_coordinates(1, new_coordinates))

    def send_bare_command(self, command):
        self.send_bytearray((command).to_bytes(self.COMMAND_SIZE, byteorder='big'))

    def send_set_speed(self, speed):  # speed in mm/sec
        msg = bytearray()
        msg.extend((6).to_bytes(self.COMMAND_SIZE, byteorder='big'))
        msg.extend(int(speed*2**(0.5)).to_bytes(self.SPEED_SIZE, byteorder='big'))
        self.send_bytearray(msg)
    def send_set_acceleraton(self, acceleration):  # acceleration in mm/sec^2
        msg = bytearray()
        msg.extend((7).to_bytes(self.COMMAND_SIZE, byteorder='big'))
        msg.extend(int(acceleration*2**(0.5)).to_bytes(self.ACCELERATION_SIZE, byteorder='big'))
        self.send_bytearray(msg)


def main():
    sender = SerialSender('COM7')
    sender.send_bare_command(5)
    sender.send_set_speed(400)
    sender.send_set_acceleraton(500)
    for a in range(8):
        sender.send_move((6, 6))
        sender.send_move((0, 0))
    sender.send_bare_command(4)


if __name__ == "__main__":
    main()