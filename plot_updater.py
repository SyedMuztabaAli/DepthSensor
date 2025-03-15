import pyqtgraph as pg
from PyQt5 import QtGui,QtCore

class PlotUpdater:
    def __init__(self, plot_graph):
        self.plot_graph = plot_graph
        self.time = [0]  # Start with time = 0
        self.depth = [0]  # Start with depth = 0

        # Set up the plot line
        pen = pg.mkPen(color=(255, 0, 0))  # Red line
        self.line = self.plot_graph.plot(
            self.time,
            self.depth,
            name="Depth Sensor",
            pen=pen
        )

        # Add a blue fill for the water (from the line to y=0)
        self.water_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),  # Fill down to y=0
            brush=pg.mkBrush(color=(0, 191, 255, 150))  # Water-like blue color
        )
        self.plot_graph.addItem(self.water_fill)

        # Add a muddy fill for the area above the line (from max y-value to the line)
        self.muddy_fill = pg.FillBetweenItem(
            self.line,
            pg.PlotDataItem([0], [0]),  # Placeholder, will be updated dynamically
            brush=pg.mkBrush(color=(139, 69, 19, 150))  # Muddy brown color
        )
        self.plot_graph.addItem(self.muddy_fill)

        self.fixed_distance = 5  # Fixed distance from y=0
        self.above_zero_line = pg.InfiniteLine(
            pos=-self.fixed_distance,  # Position the line at y=-5 (above y=0 due to inverted y-axis)
            angle=0,  # Horizontal line
            pen=pg.mkPen(color="yellow", width=2, style=QtCore.Qt.DashLine)  # Yellow dashed line
        )
        self.plot_graph.addItem(self.above_zero_line)

    def update_plot(self, depth):
        # Increment time by 1 second
        new_time = self.time[-1] + 1 if self.time else 0

        # Update time and depth data
        self.time.append(new_time)
        self.depth.append(depth)

        # Limit the number of visible points to 20 (optional)
        if len(self.time) > 20:
            self.time = self.time[-20:]
            self.depth = self.depth[-20:]

        # Update the plot
        self.line.setData(self.time, self.depth)

        # Calculate the maximum y-value for the muddy fill
        max_depth = max(self.depth)
        padding = 5  # Add some padding for better visualization
        max_y_value = max_depth + padding  # Set the upper boundary for the muddy fill

        # Update the fill areas
        self.water_fill.setCurves(self.line, pg.PlotDataItem(self.time, [0] * len(self.time)))
        self.muddy_fill.setCurves(self.line, pg.PlotDataItem(self.time, [max_y_value] * len(self.time)))

        self.above_zero_line.setPos(-self.fixed_distance)

        # Dynamically adjust the y-axis range, ensuring 0 is always included
        min_depth = min(self.depth)
        self.plot_graph.setYRange(
            min(min_depth - padding, 0 - self.fixed_distance),  # Ensure y=0 and y=5 are included
            max(max_y_value, self.fixed_distance)  # Ensure y=5 is included
        )