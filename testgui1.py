import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLabel, QLineEdit, QToolBar, QMainWindow, QAction, QFileDialog, QGridLayout, QCheckBox, QHBoxLayout, QTableView
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
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
# x1 = 76  # len1_len2_peaklist.csv
# y1 = 521 # <= why is this hardcoded lo
x1 = 4 # len1_len2_peaklist.csv
y1 = 4
class TableModel(QtCore.QAbstractTableModel): #I dont know i just stole all this code
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class Window(QDialog,QMainWindow):
    def __init__(self, parent=None):
        self.temp = 0
        self.templist = []
        self.array = []
        self.temp1 = 0
        super(Window, self).__init__(parent)
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # Toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.addAction('Load Folder        ',self.heatarrayg)
        self.toolbar.addAction('Load Folder for Normalization')
        self.toolbar.addSeparator()
        # mass search textbox
        self.label = QLabel(self)
        self.checkbox = QCheckBox("Normalize Axis")
        self.line = QLineEdit("Enter Mass")
        self.line.setFixedSize(300,25)
        self.line1 = QLineEdit("Enter Color Scalar")
        self.line1.setFixedSize(200,25)
        self.label = QLabel("           ")
        self.checkbox1 = QCheckBox("Apply Color Scalar")
        self.table = QTableView()
        self.checkbox2 = QCheckBox("Normalize Data")
        self.checkbox3 = QCheckBox("Flip Normalization")
        # Just some button connected to `heatmap` method
        self.button = QPushButton('Graph/Regraph')
        #vspacer = QtWidgets.QSpacerItem(500, 40)
        self.button.clicked.connect(self.heatmap)
        #creating sublayout for row
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.line)
        hlayout.addWidget(self.checkbox)
        #another sublayout
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.checkbox1)
        hlayout1.addWidget(self.line1)
        hlayout1.addWidget(self.label)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.checkbox2)
        hlayout2.addWidget(self.checkbox3)
        #another sublayout for column of table
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.table)
        # set the layout
        layout = QGridLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addLayout(hlayout,3,0)
        layout.addLayout(hlayout1,4,0)
        layout.addLayout(vlayout,1,1)
        layout.addLayout(hlayout2,5,0)
        #layout.addLayout(self.table,5,0)
        self.setLayout(layout)
    def table(self):
        try:
            data = self.array1.tolist()
            #data = [[4,3,2],[5,2,3]] #table
            self.model = TableModel(data)
            self.table.setModel(self.model)
            self.table.show()
        except:
            pass
    def heatarrayg(self): #this function would be faster if all csvs were combined into one and pd was used but i dont feel like it
        if self.temp != 0: #resetting our class variable
            self.temp = 0
        loadlst = Window.loadlist(self)  #getting our list of files to load
        lengthload = len(loadlst)
        list = []
        try: #loading our files
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
    def normalload(self): #this function would be faster if all csvs were combined into one and pd was used but i dont feel like it
        if self.temp1 != 0: #resetting our class variable
            self.temp1 = 0
        loadlst = Window.loadlist(self)  #getting our list of files to load
        lengthload = len(loadlst)
        list = []
        try: #loading our files
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
        self.temp1 = list

    def loadlist(self): #list of files to load (what a mess)
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

    # def heatarray(self):
    #     lengthload = len(Window.loadlist(self))
    #     loadlst = Window.loadlist(self)
    #     list = []
    #     for i in range(0, lengthload):
    #         a = pd.read_csv(loadlst[i], delimiter=',', dtype=float) #this is slow, but so is every other method. Not sure if it can be optimized.
    #         a.to_numpy()
    #         a = np.delete(a, 0, 0) #removes first row
    #         a = a[:-1] #removes last row
    #         a = np.delete(a, [3, 2], 1) #removes last two columns
    #         list.append(a)
    #     return(list)

    def arraymanipulation(self,x1,y1): #gives us our final array
        if self.checkbox2.isChecked() == False:
            arr = self.temp
            self.array = arr[0]
            try:
                self.array1 = arr[15388] #getting abundances at a random pixel somewhere in the middle bc im lazy (to be specific the 29th line at pixel 250)
            except:
                self.array1=arr[0]
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
        else:
            arr = self.temp
            arr1 = self.temp1
            self.array = arr[0]

    def heatmap(self): #draw that shit
        if self.checkbox2.isChecked() == False:
            array = Window.arraymanipulation(self, x1, y1)
            if self.checkbox.isChecked() ==True:
                array = array/np.linalg.norm(array)
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.set_axis_on()
            array = array * (array >= 0)# if less than 0 make it 0
            plt.axis('off')
            if self.checkbox1.isChecked() == True:
                quantile = np.quantile(array, 0.99)
                quantile = quantile * float(self.line1.text())
                im = ax.imshow(array,cmap='hot',interpolation='none',vmax=quantile)
            if self.checkbox1.isChecked() ==False:
                im = ax.imshow(array, cmap='hot', interpolation='none')
            ax.set_aspect(5)
            #divider = make_axes_locatable(ax)
            #cax = divider.append_axes("right",size="5%",pad=0.05)
            cax = self.figure.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height]) #somehow makes my color bar axis the same height as my heatmap
            plt.colorbar(im,cax=cax) #colorbar
            self.canvas.draw()
            Window.table(self)
        else:
            array = Window.arraymanipulation(self, x1, y1)
            if self.checkbox.isChecked() == True:
                array = array / np.linalg.norm(array)
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.set_axis_on()
            array = array * (array >= 0)  # if less than 0 make it 0
            plt.axis('off')
            if self.checkbox1.isChecked() == True:
                quantile = np.quantile(array, 0.99)
                quantile = quantile * float(self.line1.text())
                im = ax.imshow(array, cmap='hot', interpolation='none', vmax=quantile)
            if self.checkbox1.isChecked() == False:
                im = ax.imshow(array, cmap='hot', interpolation='none')
            ax.set_aspect(5)
            # divider = make_axes_locatable(ax)
            # cax = divider.append_axes("right",size="5%",pad=0.05)
            cax = self.figure.add_axes([ax.get_position().x1 + 0.01, ax.get_position().y0, 0.02,
                                        ax.get_position().height])  # somehow makes my color bar axis the same height as my heatmap
            plt.colorbar(im, cax=cax)  # colorbar
            self.canvas.draw()
            Window.table(self)
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