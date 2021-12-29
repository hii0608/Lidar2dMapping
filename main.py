import sys
from PyQt5.QtWidgets import *
import numpy as np
from matplotlib import animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import time


def file_read(f):
    """
    Reading LIDAR laser beams (angles and corresponding distance data)
    """
    measures = [line.split(",") for line in open(f)]
    angles = []
    distances = []
    for measure in measures:
        angles.append(float(measure[0]))
        distances.append(float(measure[1]))
    angles = np.array(angles)
    distances = np.array(distances)
    return angles, distances

class AnimationWidget(QWidget):
    def __init__(self):
        QMainWindow.__init__(self)

        ang, dist = file_read("lidar01.csv")
        ox = np.sin(ang) * dist
        oy = np.cos(ang) * dist


        self.fig = plt.figure(figsize=(6, 10))

        plt.plot([oy, np.zeros(np.size(oy))], [ox, np.zeros(np.size(oy))], "ro-")  # lines from 0,0 to the
        plt.axis("equal")
        bottom, top = plt.ylim()  # return the current ylim
        plt.ylim((top, bottom))  # rescale y axis, to match the grid orientation
        plt.grid(True)
       # plt.show()

        self.canvas = FigureCanvas(self.fig)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)

        hbox = QHBoxLayout()
        self.start_button = QPushButton("start", self)
        self.stop_button = QPushButton("stop", self)
    #    self.start_button.clicked.connect(self.on_start)
     #   self.stop_button.clicked.connect(self.on_stop)

        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        dynamic_canvas = FigureCanvas(plt.figure(figsize=(4, 3)))
        vbox.addWidget(dynamic_canvas)

        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.timer = dynamic_canvas.new_timer(
            100, [(self.update_canvas, (), {})])
        self.timer.start()

    def update_canvas(self):
        self.dynamic_ax.clear()
        t = np.linspace(0, 2 * np.pi, 101)
        self.dynamic_ax.plot(t, np.sin(t + time.time()), color='deeppink')
        self.dynamic_ax.figure.canvas.draw()

    def on_start(self):
        self.ani = animation.FuncAnimation(self.canvas.figure, self.update_line, blit=True, interval=25)


    def on_stop(self):
        self.ani._stop()

if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    aw = AnimationWidget()
    aw.show()
    sys.exit(qApp.exec_())
