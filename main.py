import sys
from PyQt5 import QtWidgets
import pyqtgraph as pg
from sensor_reader import SensorReader  # Import the sensor reader module
from plot_updater import PlotUpdater  # Import the plot updater module

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the plot
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("black")
        self.plot_graph.setTitle("Depth vs Time", color="b", size="20pt")
        styles = {"color": "red", "font-size": "18px"}
        self.plot_graph.setLabel("left", "Depth (m)", **styles)
        self.plot_graph.setLabel("bottom", "Time (sec)", **styles)

        # Move the y-axis to the right side
        self.plot_graph.showAxis('right')
        self.plot_graph.hideAxis('left')
        self.plot_graph.getAxis('right').setLabel('Depth (m)', **styles)

        self.plot_graph.invertY(True)
        self.plot_graph.addLegend()
        self.plot_graph.showGrid(x=True, y=True)

        # Initialize the plot updater
        self.plot_updater = PlotUpdater(self.plot_graph)

        # Set up the sensor reader
        self.sensor_reader = SensorReader()
        self.sensor_reader.new_depth_data.connect(self.plot_updater.update_plot)  # Connect signal to slot

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())