import serial
from PyQt5 import QtCore

class SensorReader(QtCore.QObject):
    new_depth_data = QtCore.pyqtSignal(float)

    def __init__(self, port, baudrate):
        super().__init__()
        self.serial = serial.Serial(port, baudrate)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_sensor)
        self.timer.start(1000)  # Read data every 1 second

    def read_sensor(self):
        if self.serial.in_waiting:
            data = self.serial.readline().decode('utf-8').strip()
            try:
                depth = float(data)  # Convert sensor data to float
                self.new_depth_data.emit(depth)
            except ValueError:
                print("Invalid sensor data")