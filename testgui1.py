import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLabel, QLineEdit, QToolBar, QMainWindow, QAction, QFileDialog, QGridLayout
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import tkinter as tk
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# slider for color scalar
# show what mass was found
# show what file is loaded
# print that with jpeg option
# tic add up all values in second column of original csvs then divide by integration if whatever mass you want
#display color bar
# x1 = 76  # len1_len2_peaklist.csv
# y1 = 521
x1 = 4 # len1_len2_peaklist.csv
y1 = 4
class Window(QDialog,QMainWindow):
    def __init__(self, parent=None):
        self.temp = 0
        self.templist = []
        super(Window, self).__init__(parent)
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # Toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.addAction('Load Folder',self.heatarrayg)
        self.toolbar.addSeparator()
        # mass search textbox
        self.label = QLabel(self)
        self.line = QLineEdit("Enter Mass")
        self.line.setFixedSize(100,25)
        # Just some button connected to `heatmap` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.heatmap)
        # set the layout
        layout = QGridLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.line,3,0)
        self.setLayout(layout)
    def heatarrayg(self):
        if self.temp != 0:
            self.temp = 0
        loadlst = Window.loadlist(self)
        lengthload = len(loadlst)
        list = []
        try:
            for i in range(0, lengthload):
                a = 0
                a = np.genfromtxt(loadlst[i], delimiter=',',
                                  dtype=float)  # this is slow, but so is every other method. Not sure if it can be optimized.
                a = np.delete(a, 0, 0)  # removes first row
                a = a[:-1]  # removes last row
                a = np.delete(a, [3, 2], 1)  # removes last two columns
                list.append(a)
        except:
            print("error!")
        self.temp= list
    def loadlist(self):
        if self.templist !=0:
            self.templist = []
        path1 = QFileDialog.getExistingDirectory(self) + '/'
        for x in range(1, x1 + 1):  # x_blah
            for y in range(0, y1):  # blah_y
                pathnumx = str(x)
                pathnumy = str(y)
                pathnum = pathnumx + "_" + pathnumy + "_peaklist.csv"
                path = path1 + pathnum
                self.templist.append(path)
        return(self.templist)
    def heatarray(self):
        lengthload = len(Window.loadlist(self))
        loadlst = Window.loadlist(self)
        list = []
        for i in range(0, lengthload):
            a = pd.read_csv(loadlst[i], delimiter=',', dtype=float) #this is slow, but so is every other method. Not sure if it can be optimized.
            a.to_numpy()
            a = np.delete(a, 0, 0) #removes first row
            a = a[:-1] #removes last row
            a = np.delete(a, [3, 2], 1) #removes last two columns
            list.append(a)
        return(list)
    def arraymanipulation(self,x1,y1):
        arr = self.temp
        lengthload = len(arr)
        heatarray = np.empty((0), float)
        val1 = int(self.line.text())
        for i in range(0, lengthload):
            a = arr[i]
            a1 = a[:, 0] #a1 = first column of array
            value = val1
            array = np.asarray(a1) #no idea
            mass = a1[np.abs(array - value).argmin()] #search for a value closest to mass inputted
            rows, cols = np.where(a == mass) #find the row where the mass = the mass searched for
            abun = a[rows] # does something with the rows
            abun = abun[0, 1] #retrives abundance from second row of the mass found row
            heatarray = np.append(heatarray, abun)# adds abundance to the empty array
        heatarray1 = np.reshape(heatarray, (x1, y1)) #reshapes the empty array into the size we want
        return heatarray1

    def heatmap(self):
        array = Window.arraymanipulation(self, x1, y1)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_axis_on()
        array = array * (array >= 0)# if less than 0 make it 0
        plt.axis('off')
        ax.imshow(array,cmap='hot',interpolation='none')
        ax.set_aspect(5)
        ax.color
        self.canvas.draw()
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # ax = plt.Axes(fig, [0., 0., 1., 1.])
        # ax.set_axis_off()
        # fig.add_axes(ax)
        # # array = array.flatten()
        # # histo = np.histogram(array)
        # # plt.hist(histo, bins='auto')
        # quantile = np.quantile(array, 0.99)
        # quantile = quantile * 2
        # fig = ax.imshow(array, cmap='hot', interpolation='none', vmax=quantile)  # vmax
        # ax.set_aspect(5)
        # plt.axis('off')
        # fig.axes.get_xaxis().set_visible(False)
        # fig.axes.get_yaxis().set_visible(False)
        # plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())