from random import randint
from PyQt5 import QtCore

class SensorReader(QtCore.QObject):
    new_depth_data = QtCore.pyqtSignal(float)  # Signal to emit new depth data

    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_sensor)
        self.timer.start(1000)  # Emit data every 1 second

    def read_sensor(self):
        # Simulate sensor data (replace this with actual sensor reading logic)
        depth = randint(5, 300)  # Random depth between 20 and 40 meters
        self.new_depth_data.emit(depth)  # Emit the new depth value