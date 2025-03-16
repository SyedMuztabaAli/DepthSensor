import sys
from PyQt5 import QtWidgets
import pyqtgraph as pg
from sensor_reader import SensorReader
from plot_updater import PlotUpdater

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground('black')
        self.plot_graph.setTitle("Depth vs Time",color = 'grey', size="20px")
        style = {'color':'white','font-size':'18px'}
        self.plot_graph.setLabel('right','Depth(m)',**style)
        self.plot_graph.setLabel('bottom','Time(sec)',**style)

        self.plot_graph.showAxis('right')
        self.plot_graph.hideAxis('left')
        self.plot_graph.showGrid(x=True,y=True)

        self.plot_graph.invertY()

        self.plot_graph.addLegend()



        self.plot_updater = PlotUpdater(self.plot_graph)

        self.sensor_reader = SensorReader()
        self.sensor_reader.new_depth_data.connect(self.plot_updater.update_plot)


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())