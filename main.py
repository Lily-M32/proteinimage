import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLabel, QLineEdit, QToolBar, QMainWindow, QFileDialog, QGridLayout, QCheckBox, QHBoxLayout, QTableView, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
class TableModel(QtCore.QAbstractTableModel): #Creates Mass Table on Side
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
        self.x1 = 0
        self.y1 = 0
        self.temp = 0
        self.templist = []
        self.array = []
        self.temp1 = 0
        self.listname = ""
        self.TIClo = False
        self.normalused = False
        self.temp2 = 0
        self.imname0 = ''
        self.imname1 = ''
        self.massFound = 0
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
        self.toolbar.addAction('Load Folder for Normalization',self.normalload)
        self.toolbar.addSeparator()
        self.toolbar.addAction("Load TIC Folder",self.TICload)
        self.toolbar.addSeparator()
        self.toolbar.addAction('Save Image As',self.savepng)
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
        self.checkbox4 = QCheckBox("TIC Normalize Data")
        # Just some button connected to `heatmap` method
        self.button = QPushButton('Graph/Regraph')
        #vspacer = QtWidgets.QSpacerItem(500, 40)
        self.button.clicked.connect(self.heatmap)
        #self.setFixedSize(1000,1000)
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
        hlayout2.addWidget(self.checkbox4)
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
    def table(self): #setting up stuff for the table
        try:
            data = self.array1.tolist()
            #data = [[4,3,2],[5,2,3]] #table
            self.model = TableModel(data)
            self.table.setModel(self.model)
            self.table.show()
        except:
            pass
    def heatarrayg(self): #loads all our files
        if self.temp != 0: #resetting our class variable
            self.temp = 0
        loadlst = Window.loadlist(self)  #getting our list of files to load
        try:
            lengthload = len(loadlst)
        except:
            return
        list = []
        try: #loading our files
            for i in range(0, lengthload):
                a = 0
                a = np.genfromtxt(loadlst[i], delimiter=',',
                                  dtype=float)   # this is slow, but so is every other method. Could be optimized if all files are combined into one + loaded with pandas
                a = np.delete(a, 0, 0)  # removes first row
                a = a[:-1]  # removes last row
                a = np.delete(a, [3, 2], 1)  # removes last two columns
                list.append(a)
        except:
            print("error!")
        self.temp= list
        arr = self.temp
        try:
            self.array = arr[0]
        except:
            print("error!")
        try:
            self.array1 = arr[15388]  # getting abundances at a random pixel somewhere in the middle bc im lazy (to be specific the 29th line at pixel 250)
        except:
            try:
                self.array1 = arr[0]
            except:
                print("error!")
        Window.table(self)
    def normalload(self): #loads our files
        if self.temp1 != 0: #resetting our class variable
            self.temp1 = 0
        self.normalused = True
        loadlst = Window.loadlist(self)  #getting our list of files to load
        self.normalused = False
        try:
            lengthload = len(loadlst)
        except:
            return
        list = []
        try: #loading our files
            for i in range(0, lengthload):
                a = 0
                a = np.genfromtxt(loadlst[i], delimiter=',',
                                  dtype=float)  # this is slow, but so is every other method. Could be optimized if all files are combined into one + loaded with pandas
                a = np.delete(a, 0, 0)  # removes first row
                a = a[:-1]  # removes last row
                a = np.delete(a, [3, 2], 1)  # removes last two columns
                list.append(a)
        except:
            print("error!")
        self.temp1 = list
    def TICload(self): #loads TIC files
        self.TIClo = True
        loadlst = Window.loadlist(self)  # getting our list of files to load
        try:
            lengthload = len(loadlst)
        except:
            return
        list = []
        try:  # loading our files
            for i in range(0, lengthload):
                a = pd.read_csv(loadlst[i], delimiter=',',
                                  dtype=float, header=None)  #this is slow, even with pandas. loading >25 gigs takes time!
                b = a.to_numpy()
                b = b[:, 1]
                b = np.sum(b)
                if i % self.y1 == 0:
                    var = i / self.y1
                    print("File {ab} / {bc} Loaded".format(ab=int(var),bc=self.x1))
                # b = a[:,1]
                # np.sum(b)
                list.append(b)
        except:
             print("error!")
        self.temp2 = list
        self.TIClo = False
        print("Done Loading TIC!")

    def loadlist(self): #list of files to load, done dynamically!!!!!
        try:
            if self.TIClo == False:
                if self.templist !=0:
                    self.templist = []
                path1 = QFileDialog.getExistingDirectory(self) + '/' #get directory to parse files from
                self.templist = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))] #get all files
                self.templist = [x for x in self.templist if ".csv" in x] #remove files that dont have .csv
                self.templist = [path1 + ab for ab in self.templist] #add full filepath
                listToSort = []
                for ib in range(0,len(self.templist)):
                    string1 = Window.find_between_r(self, self.templist[ib], "/", "_p") #get our numbers
                    string1 = string1.replace("_", " ") #replace _ with " " to make .split work
                    b = [int(s) for s in string1.split() if s.isdigit()] #get two numbers
                    b.append(int(ib))
                    listToSort.append(b)
                npSort = np.array(listToSort) #turn list into np array
                npSort = npSort[np.lexsort((npSort[:,1],npSort[:,0]))] #sort list so 1,0 1,1 1,2 etc
                listSorted = npSort.tolist() #turn np array back into list
                listIndex = []
                for i in range(0,len(listSorted)): #get index of first list
                    temp = listSorted[i][2]
                    listIndex.append(temp)
                #print(len(self.templist),"2")
                listTemp1 = []
                for i in range(0,len(self.templist)): #make self.templist sorted list
                    temp = listIndex[i]
                    var = self.templist[temp]
                    listTemp1.append(var)
                self.templist = listTemp1
                #print(len(self.templist),"3")
                strVar = self.templist[-1] #get last file in array
                #print(strVar)
                string2 = Window.find_between_r(self, strVar, "/", "_p")  # get our numbers
                string2 = string2.replace("_", " ")  # replace _ with " " to make .split work
                b = [int(s) for s in string2.split() if s.isdigit()]  # get two numbers


                #print(npSort)
                #self.templist.sort(key=int)
                self.listname = self.templist[0][0]

                self.x1 = b[0] #get our x (eg *76*_521
                self.y1 = b[1] #get our y (eg 76_*521*
                self.y1 = self.y1 + 1 #add one to it to fix some for loop elsewhere
                if self.normalused == False:
                    self.imname0 = self.templist[0]
                if self.normalused == True:
                    self.imname1 = self.templist[0]
                return(self.templist)
            if self.TIClo == True:
                if self.templist != 0:
                    self.templist = []
                path1 = QFileDialog.getExistingDirectory(self) + '/'  # get directory to parse files from
                self.templist = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]  # get all files
                self.templist = [x for x in self.templist if ".csv" in x]  # remove files that dont have .csv
                self.templist = [path1 + ab for ab in self.templist]  # add full filepath
                # for i in range(0,len(self.templist)):
                # self.templist[i] = path1 + self.templist[i]
                listToSort = []
                # print(len(self.templist),"1")
                for ib in range(0, len(self.templist)):
                    string1 = Window.find_between_r(self, self.templist[ib], "/", ".csv")  # get our numbers
                    string1 = string1.replace("_", " ")  # replace _ with " " to make .split work
                    b = [int(s) for s in string1.split() if s.isdigit()]  # get two numbers
                    b.append(int(ib))
                    listToSort.append(b)
                npSort = np.array(listToSort)  # turn list into np array
                npSort = npSort[np.lexsort((npSort[:, 1], npSort[:, 0]))]  # sort list so 1,0 1,1 1,2 etc
                listSorted = npSort.tolist()  # turn np array back into list
                listIndex = []
                for i in range(0, len(listSorted)):  # get index of first list
                    temp = listSorted[i][2]
                    listIndex.append(temp)
                # print(len(self.templist),"2")
                listTemp1 = []
                for i in range(0, len(self.templist)):  # make self.templist sorted list
                    temp = listIndex[i]
                    var = self.templist[temp]
                    listTemp1.append(var)
                self.templist = listTemp1
                # print(len(self.templist),"3")
                strVar = self.templist[-1]
                # print(strVar)
                string2 = Window.find_between_r(self, strVar, "/", "_p")  # get our numbers
                string2 = string2.replace("_", " ")  # replace _ with " " to make .split work
                b = [int(s) for s in string2.split() if s.isdigit()]  # get two numbers

                # print(npSort)
                # self.templist.sort(key=int)
                self.listname = self.templist[0][0]

                self.x1 = b[0]
                self.y1 = b[1]
                self.y1 = self.y1 + 1
                return (self.templist)
        except:
            print("error!")
            return
    def savepng(self):
        try:
            name = QFileDialog.getSaveFileName(self, 'Save File')
            save = (name[0] + ".png")
            print(save)
            plt.savefig(save)
            print("saved!")
        except:
            return
    def find_between_r(self, s, first, last):  # used to find filenames
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""
    def arraymanipulation(self,x1,y1): #gives us our final array
        if self.checkbox4.isChecked() == True:
            arr = self.temp
            arr1 = self.temp2
            self.array = arr[0]
            lengthload = len(arr)
            heatarray = np.empty((0), float)  # create an emtpy float array
            arr1TIC = []
            arr2TIC = []
            # val1 = int(self.line.text())
            for i in range(0, lengthload):
                a = arr[i]
                ab = arr1[i]
                arr1TIC.append(np.sum(a[:, 1]))
                arr2TIC.append(ab)
            arr1TIC = np.asarray(arr1TIC)
            arr2TIC = np.asarray(arr2TIC)
            arr1TIC = np.reshape(arr1TIC, (self.x1, self.y1))
            arr2TIC = np.reshape(arr2TIC, (self.x1, self.y1))
            if self.checkbox3.isChecked() == False:
                heatarray1 = np.divide(arr1TIC, arr2TIC)
            else:
                heatarray1 = np.divide(arr2TIC, arr1TIC)
            return heatarray1
        if self.checkbox2.isChecked() == False:
            arr = self.temp
            try:
                self.array = arr[0]
            except:
                print("error!")
                return

            try:
                self.array1 = arr[15388] #getting abundances at a random pixel somewhere in the middle bc im lazy (to be specific the 29th line at pixel 250)
            except:
                self.array1=arr[0]
            lengthload = len(arr)
            heatarray = np.empty((0), float)
            try:
                val1 = int(self.line.text())
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('No Mass Set!')
                msg.setWindowTitle("Error")
                msg.exec_()
                return
            for i in range(0, lengthload):
                a = arr[i]
                a1 = a[:, 0] #a1 = first column of array
                value = val1
                array = np.asarray(a1) #no idea
                mass = a1[np.abs(array - value).argmin()] #search for a value closest to mass inputted
                rows, cols = np.where(a == mass) #find the row where the mass = the mass searched for
                abun = a[rows] # does something with the rows
                self.massFound = abun[0,0]
                abun = abun[0, 1] #retrives abundance from second row of the mass found row
                heatarray = np.append(heatarray, abun)# adds abundance to the empty array
            heatarray1 = np.reshape(heatarray, (self.x1, self.y1)) #reshapes the empty array into the size we want
            return heatarray1
        if self.checkbox2.isChecked() == True:
            arr = self.temp
            arr1 = self.temp1
            try:
                self.array = arr[0]
            except:
                print("error")
                return
            try:
                self.array1 = arr[15388] #getting abundances at a random pixel somewhere in the middle bc im lazy (to be specific the 29th line at pixel 250)
            except:
                self.array1=arr[0]
            lengthload = len(arr)
            heatarray = np.empty((0), float) #create an emtpy float array
            arr1TIC = []
            arr2TIC = []
            #val1 = int(self.line.text())
            for i in range(0, lengthload):
                a = arr[i]
                try:
                    ab = arr1[i]
                except:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText('No Protein Loaded To Normalize To!')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    return
                arr1TIC.append(np.sum(a[:,1]))
                arr2TIC.append(np.sum(ab[:,1]))
            #     a1 = a[:, 0] #a1 = first column of array
            #     value = val1
            #     array = np.asarray(a1) #converts our array into an array (lo)
            #     mass = a1[np.abs(array - value).argmin()] #search for a value closest to mass inputted
            #     rows, cols = np.where(a == mass) #find the row where the mass = the mass searched for
            #     abun = a[rows] # does something with the rows
            #     abun = abun[0, 1] #retrives abundance from second row of the mass found row
            #     heatarray = np.append(heatarray, abun)# adds abundance to the empty array
            # heatarray1 = np.reshape(heatarray, (x1, y1)) #reshapes the empty array into the size we want
            arr1TIC = np.asarray(arr1TIC)
            arr2TIC = np.asarray(arr2TIC)
            arr1TIC = np.reshape(arr1TIC, (self.x1,self.y1))
            arr2TIC = np.reshape(arr2TIC, (self.x1,self.y1))
            if self.checkbox3.isChecked() == False:
                heatarray1 = np.divide(arr1TIC,arr2TIC)
            else:
                heatarray1 = np.divide(arr2TIC,arr1TIC)
            return heatarray1

    def heatmap(self): #draw the heatmap
        try:
            if self.checkbox2.isChecked() == False:
                array = Window.arraymanipulation(self, self.x1, self.y1)
                if self.checkbox.isChecked() ==True:
                    array = array/np.linalg.norm(array)
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.set_axis_on()
                try:
                    array = array * (array >= 0)# if less than 0 make it 0
                except:
                    print("error!")
                    return
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
                x1 = self.x1
                cax = self.figure.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height]) #somehow makes my color bar axis the same height as my heatmap
                plt.colorbar(im,cax=cax) #colorbar
                ax.set_title(str(self.imname0)+ "   Mass: " + str(int(self.massFound)) + "\n",fontsize=10)
                self.canvas.draw()
                Window.table(self)
            else:
                array = Window.arraymanipulation(self, self.x1, self.y1)
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
                x1 = self.x1
                cax = self.figure.add_axes([ax.get_position().x1 + 0.01, ax.get_position().y0, 0.02,
                                            ax.get_position().height])  # somehow makes my color bar axis the same height as my heatmap
                plt.colorbar(im, cax=cax)  # colorbar
                title = str(self.imname0) + " normalized to " + "\n" + str(self.imname1) + "\n"
                ax.set_title(title,fontsize=10)
                self.canvas.draw()
                Window.table(self)
        except Exception as e:
            print(e)
            print("error!")
            return
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