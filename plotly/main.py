import time
import random
import pyqtgraph as pg
from collections import deque
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
from scipy.interpolate import make_interp_spline

import csv


class Graph:
    def __init__(self, ):

        self.maxLen = 50  # max number of data points to show on graph
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()

        self.p1 = self.win.addPlot(colspan=2)
        self.p1.setRange(yRange=[-20, 130])
        self.p1.showGrid(x=True, y=True, alpha=0.3)
        self.p1.addLine(y=15)
        self.p1.addLine(y=85)
        self.win.nextRow()

        self.curve1 = self.p1.plot(pen='r')
        self.curve2 = self.p1.plot(pen='g')

        graphUpdateSpeedMs = 50
        timer = QtCore.QTimer()  # to create a thread that calls a function at intervals
        timer.timeout.connect(self.update)  # the update function keeps getting called at intervals
        timer.start(graphUpdateSpeedMs)
        QtGui.QApplication.instance().exec_()

    def update(self):
        with open(r'C:\Users\aliiq\PycharmProjects\plotly\csvs\buy.csv', 'r') as csvfile:
            self.myBuyList = []
            next(csvfile)  # skip the header ('BUY')
            for row in csv.reader(csvfile, delimiter=';'):
                self.myBuyList.append(row[0])  # careful here with [0]

        self.myBuyList = list(map(int, self.myBuyList))  # convert list of strings to list of integers

        with open(r'C:\Users\aliiq\PycharmProjects\plotly\csvs\sell.csv', 'r') as csvfile:
            self.mySellList = []
            next(csvfile)  # skip the header ('BUY')
            for row in csv.reader(csvfile, delimiter=';'):
                self.mySellList.append(row[0])  # careful here with [0]

        self.mySellList = list(map(int, self.mySellList))  # convert list of strings to list of integers

        if len(self.myBuyList) > self.maxLen:
            self.myBuyList.popleft()  # remove oldest
        if len(self.mySellList) > self.maxLen:
            self.mySellList.popleft()  # remove oldest
            # self.dat2.popleft()  # remove oldest
        # self.dat.append(random.randint(0, 100));
        # self.dat2.append(random.randint(0, 100));

        self.myBuyList_ = np.array(self.myBuyList)
        self.x_ = np.array(range(0, len(self.myBuyList)))
        self.X_Y_Spline = make_interp_spline(self.x_, self.myBuyList_)
        self.X_ = np.linspace(self.x_.min(), self.x_.max(), 500)
        self.Y_ = self.X_Y_Spline(self.X_)

        self.mySellList_ = np.array(self.mySellList)
        self.x2_ = np.array(range(0, len(self.mySellList)))
        self.X2_Y2_Spline = make_interp_spline(self.x2_, self.mySellList_)
        self.X2_ = np.linspace(self.x2_.min(), self.x2_.max(), 500)
        self.Y2_ = self.X2_Y2_Spline(self.X2_)

        self.curve1.setData(self.X_, self.Y_)
        self.curve2.setData(self.X2_, self.Y2_)

        self.app.processEvents()


if __name__ == '__main__':
    g = Graph()
