import sys
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np


class PlotUpdater:
    def __init__(self, plot_graph, main_window):
        self.main_window = main_window
        self.plot_graph = plot_graph
        self.time = []
        self.depth = []
        self.temperature = []

        # Plot the initial line
        pen = pg.mkPen(color=(255, 0, 0))
        self.line = self.plot_graph.plot(
            self.time,
            self.depth,
            pen=pen
        )

        # Add water fill
        self.water_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),
            brush=pg.mkBrush(color='#000000')
        )
        self.plot_graph.addItem(self.water_fill)

        # Add muddy fill
        self.muddy_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),
            brush=pg.mkBrush(color='#C18136')
        )
        self.plot_graph.addItem(self.muddy_fill)

        # Add vehicle fill
        self.vehicle_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),
            brush=pg.mkBrush(color='#52d8f8')
        )
        self.plot_graph.addItem(self.vehicle_fill)

        # Add a fixed line
        self.distance = 50
        self.fixed_line = pg.InfiniteLine(
            pos=-self.distance,
            angle=0,
            pen=pg.mkPen(color='white', width=2, style=QtCore.Qt.DashLine)
        )
        self.plot_graph.addItem(self.fixed_line)

        # Add a zero line
        self.zero_line = pg.InfiniteLine(
            pos=0,
            angle=0,
            pen=pg.mkPen(color='d', width=2, style=QtCore.Qt.DashLine)
        )
        self.plot_graph.addItem(self.zero_line)

        # Static text for labels
        self.static_depth_text = pg.TextItem(anchor=(0, 1), color='#000000')
        self.static_temp_text = pg.TextItem(anchor=(0, 1), color='#000000')
        static_font1 = QtGui.QFont('Arial', 16)
        static_font2 = QtGui.QFont('Arial', 12)
        static_font1.setBold(True)
        static_font2.setBold(True)

        self.static_depth_text.setFont(static_font1)
        self.static_temp_text.setFont(static_font2)

        self.static_depth_text.setText("Depth :")
        self.static_temp_text.setText("Temp      :")
        #self.static_depth_text.setPos(0, -self.distance / 2 + 5)  # Position of static depth text
        #self.static_temp_text.setPos(0, -self.distance / 2 + 5)  # Position of static temp text
        self.plot_graph.addItem(self.static_depth_text)
        self.plot_graph.addItem(self.static_temp_text)

        # Dynamic text for values
        self.dynamic_depth_text = pg.TextItem(anchor=(0, 1), color='#000000')
        self.dynamic_temp_text = pg.TextItem(anchor=(0, 1), color='#000000')
        dynamic_font1 = QtGui.QFont('Arial', 16)
        dynamic_font2 = QtGui.QFont('Arial', 12)
        dynamic_font1.setBold(True)
        dynamic_font2.setBold(True)
        self.dynamic_depth_text.setFont(dynamic_font1)
        self.dynamic_temp_text.setFont(dynamic_font2)
        self.plot_graph.addItem(self.dynamic_depth_text)
        self.plot_graph.addItem(self.dynamic_temp_text)

    def update_plot(self, depth, temperature):
        new_time = self.time[-1] + 1 if self.time else 0
        self.time.append(new_time)
        self.depth.append(depth)
        self.temperature.append(temperature)

        # Retrieve window size
        window_size = self.main_window.size()
        print(f"Window size: {window_size.width()} x {window_size.height()}")

        data_end_point = 30

        # Keep only the last 20 data points
        if len(self.time) > data_end_point:
            self.time = self.time[-data_end_point:]
            self.depth = self.depth[-data_end_point:]
            self.temperature = self.temperature[-data_end_point:]

        # Update the line data
        self.line.setData(self.time, self.depth)

        # Update the fill areas
        max_depth = max(self.depth) if self.depth else depth
        min_depth = min(self.depth) if self.depth else depth

        self.distance = max_depth / 4
        self.fixed_line.setPos(-self.distance)

        self.water_fill.setCurves(
            self.line,
            pg.PlotDataItem(self.time, [0] * len(self.time))
        )
        self.muddy_fill.setCurves(
            self.line,
            pg.PlotDataItem(self.time, [max_depth] * len(self.time))
        )
        self.vehicle_fill.setCurves(
            pg.PlotDataItem(self.time, [-self.distance] * len(self.time)),
            pg.PlotDataItem(self.time, [0] * len(self.time))
        )

        # Update the plot range
        self.plot_graph.setYRange(
            min(min_depth, -self.distance),
            max(max_depth, 0),
            padding=0
        )
        self.plot_graph.setXRange(self.time[-1] - (data_end_point-1), self.time[-1], padding=0)
        self.plot_graph.enableAutoRange(axis='x', enable=False)

        # Calculate the Static position
        static_text_x = self.time[0]
        static_depth_text_y = (-self.distance / 2) + (self.distance/15)
        static_temp_text_y = (-self.distance / 2) + (self.distance/5)
        self.static_depth_text.setPos(static_text_x, static_depth_text_y)
        self.static_temp_text.setPos(static_text_x, static_temp_text_y)

        # Calculate the position for dynamic values
        static_depth_text_width = self.static_depth_text.boundingRect().width()  # Width of static depth text
        static_temp_text_width = self.static_temp_text.boundingRect().width()  # Width of static temp text

        dynamic_depth_text_x = 0
        dynamic_temp_text_x = 0
        if window_size.width() <= 640:
            dynamic_depth_text_x = static_text_x + 2.5  # Add some padding
            dynamic_temp_text_x = static_text_x + 2.5  # Add some padding
        else:
            dynamic_depth_text_x = static_text_x + 1.5
            dynamic_temp_text_x = static_text_x + 1.5

        dynamic_depth_text_y = static_depth_text_y
        dynamic_temp_text_y = static_temp_text_y

        print(f"Static Depth Text Position : {static_text_x}, {static_depth_text_y}")
        print(f"Static Temp Text Position : {static_text_x}, {static_temp_text_y}")
        print(f"Dynamic Depth Text Position: ({dynamic_depth_text_x}, {dynamic_depth_text_y})")
        print(f"Dynamic Temp Text Position: ({dynamic_temp_text_x}, {dynamic_temp_text_y})")

        # Update the dynamic values
        self.dynamic_depth_text.setPos(dynamic_depth_text_x, dynamic_depth_text_y)
        self.dynamic_temp_text.setPos(dynamic_temp_text_x, dynamic_temp_text_y)
        self.dynamic_depth_text.setText(f"{self.depth[-1]}m")
        self.dynamic_temp_text.setText(f"{self.temperature[-1]}{chr(176)}C")