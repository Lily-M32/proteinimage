import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLabel, QLineEdit, QToolBar, QMainWindow, QFileDialog, QGridLayout, QCheckBox, QHBoxLayout, QTableView, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import os
import traceback
#This code needs a cleanup bady. Might do it if i feel like it

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
        self.array2 = []
        self.temp1 = 0
        self.listname = ""
        self.TIClo = False
        self.normalused = False
        self.temp2 = 0
        self.imname0 = ''
        self.imname1 = ''
        self.massFound = 0
        self.massFound1 = 0
        self.toupleab = ''
        super(Window, self).__init__(parent)
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # Toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.addAction("         ")
        self.toolbar.addAction("         ")
        self.toolbar.addSeparator()
        self.toolbar.addAction('Load Folder',self.heatarrayg)
        self.toolbar.addSeparator()
        self.toolbar.addAction('Load Folder for Normalization',self.normalload)
        self.toolbar.addSeparator()
        self.toolbar.addAction("Load TIC File",self.TICload)
        self.toolbar.addSeparator()
        self.toolbar.addAction('Save Image As',self.savepng)
        # mass search textbox
        self.label = QLabel(self)
        self.checkbox = QCheckBox("Normalize Axis")
        self.line = QLineEdit("Enter Protein Mass")
        self.line.setFixedSize(200,25)
        self.line1 = QLineEdit("Enter Color Scalar")
        self.line1.setFixedSize(200,25)
        self.line2 = QLineEdit("Enter 2nd Protein Mass")
        self.line2.setFixedSize(200,25)
        self.label = QLabel("           ")
        self.checkbox1 = QCheckBox("Apply Color Scalar")
        self.table = QTableView()
        self.table1 = QTableView()
        self.checkbox2 = QCheckBox("Normalize Data")
        self.checkbox3 = QCheckBox("Flip Normalization")
        self.checkbox4 = QCheckBox("TIC Normalize Data")
        self.checkbox5 = QCheckBox("Sum Array 1")
        self.checkbox6 = QCheckBox("Sum Array 2")
        # Just some button connected to `heatmap` method
        self.button = QPushButton('Graph/Regraph')
        #vspacer = QtWidgets.QSpacerItem(500, 40)
        self.button.clicked.connect(self.heatmap)
        #self.setFixedSize(1000,1000)
        #creating sublayout for row
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.line)
        hlayout.addWidget(self.line2)
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
        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(self.checkbox5)
        hlayout3.addWidget(self.checkbox6)
        #another sublayout for column of table
        vlayout = QGridLayout()
        self.table.setFixedSize(150,500)
        self.table1.setFixedSize(150,500)
        vlayout.addWidget(self.table,0,0)
        vlayout.addWidget(self.table1,0,1)
        # set the layout
        layout = QGridLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addLayout(hlayout,3,0)
        layout.addLayout(hlayout3,4,0)
        layout.addLayout(hlayout1,5,0)
        layout.addLayout(vlayout,1,1)
        layout.addLayout(hlayout2,6,0)
        #layout.addLayout(self.table,5,0)
        self.setLayout(layout)
        self.setFixedSize(1000,750)
    def table(self): #setting up stuff for the table
        try:
            data = self.array1.tolist()
            #data = [[4,3,2],[5,2,3]] #table
            self.model = TableModel(data)
            self.table.setModel(self.model)
            self.table.show()
        except:
            pass
    def table2(self):
        try:
            data = self.array2.tolist()
            #data = [[4,3,2],[5,2,3]] #table
            self.model1 = TableModel(data)
            self.table1.setModel(self.model1)
            self.table1.show()
        except:
            print(traceback.format_exc())
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
                #print(i)
                a = np.genfromtxt(loadlst[i], delimiter=',',
                                  dtype=float)   # this is slow, but so is every other method. Could be optimized if all files are combined into one + loaded with pandas
                a = np.delete(a, 0, 0)  # removes first row
                a = a[:-1]  # removes last row
                a = np.delete(a, [3, 2], 1)  # removes last two columns
                list.append(a)
        except:
            print("heatarray error")
        self.temp= list
        arr = self.temp
        try:
            self.array = arr[0]
        except:
            print("heatarray error")
        try:
            self.array1 = arr[15388]  # getting abundances at a random pixel somewhere in the middle bc im lazy (to be specific the 29th line at pixel 250)
        except:
            try:
                self.array1 = arr[0]
            except:
                print("heatarray error")
        Window.table(self)
    def normalload(self): #loads our files
        if self.temp1 != 0: #resetting our class variable
            self.temp1 = 0
        self.normalused = True
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
                                  dtype=float)  # this is slow, but so is every other method. Could be optimized if all files are combined into one + loaded with pandas
                a = np.delete(a, 0, 0)  # removes first row
                a = a[:-1]  # removes last row
                a = np.delete(a, [3, 2], 1)  # removes last two columns
                list.append(a)
        except:
            print("normalload error")
        self.temp1 = list
        try:
            self.array2 = self.temp1[15388]  # getting abundances at a random pixel somewhere in the middle bc im lazy (to be specific the 29th line at pixel 250)
        except:
            try:
                self.array2 = self.temp1[0]
            except:
                print("normalload error")
        Window.table2(self)
    def TICload(self): #loads TIC files
        self.TIClo = True
        path = QFileDialog.getOpenFileName()
        list = np.loadtxt(str(path[0]),delimiter=",",dtype=float)
        # list = np.reshape(list,(76,522))
        list = list.tolist()
        # loadlst = Window.loadlist(self)  # getting our list of files to load
        # try:
        #     lengthload = len(loadlst)
        # except:
        #     return
        # list = []
        # try:  # loading our files
        #     for i in range(0, lengthload):
        #         a = pd.read_csv(loadlst[i], delimiter=',',
        #                           dtype=float, header=None)  #this is slow, even with pandas. loading >25 gigs takes time!
        #         b = a.to_numpy()
        #         b = b[:, 1]
        #         b = np.sum(b)
        #         # if (i+1) % self.y1 == 0:
        #         #     var = i / self.y1
        #         #     print("File {ab} / {bc} Loaded".format(ab=int(var),bc=self.x1))
        #         # b = a[:,1]
        #         # np.sum(b)
        #         list.append(b)
        #         if (i+1) % 500 == 0:
        #             print(f"Tic load %: {(i/lengthload)*100}")
        # except Exception as e:
        #      print(f"TICload error{traceback.format_exc()}")
        # try:
        #     array1save = np.asarray(list)
        #     np.savetxt("kidneyTIC1.csv",array1save,delimiter=',') #this doesnt work, fix before next time! delimiter
        # except Exception as e:
        #     print(e)
        #     pass
        self.temp2 = list
        self.TIClo = False
        print("TIC Loaded!")

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
                self.toupleab = b

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
                print(self.templist[-1])
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
                #
                # self.x1 = b[0]
                # self.y1 = b[1]
                # self.y1 = self.y1 + 1
                return (self.templist)
        except:
            print(f"loadlist error: {traceback.format_exc()}")
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
        if self.checkbox4.isChecked() == True: #normalization to TIC
            arr = self.temp
            arr1 = self.temp2
            self.array = arr[0]
            lengthload = len(arr)
            heatarray = np.empty((0), float)  # create an emtpy float array
            arr1TIC = []
            arr2TIC = []
            # val1 = int(self.line.text())
            if self.checkbox5.isChecked() == False:
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
                if self.checkbox5.isChecked() == True:
                    arr1TIC.append(np.sum(a[:,1]))
                else:
                    a1 = a[:, 0]  # a1 = first column of array
                    value = val1
                    array = np.asarray(a1)  # turns array into np array
                    mass = a1[np.abs(array - value).argmin()]  # search for a value closest to mass inputted
                    rows, cols = np.where(a == mass)  # find the row where the mass = the mass searched for
                    abun = a[rows]  # does something with the rows
                    self.massFound = abun[0, 0]
                    abun = abun[0, 1]  # retrives abundance from second row of the mass found row
                    heatarray = np.append(heatarray, abun)  # adds abundance to the empty array
                    arr1TIC = heatarray
                ab = arr1[i]
                arr2TIC.append(ab)
            ablen = self.toupleab[0] * (self.toupleab[1]+1)
            if len(arr1TIC) != ablen:
                subtract = ablen - len(arr1TIC)
                list = []
                for i in range(0, subtract):
                    list.append(.0001)
                arr1TIC = np.append(arr1TIC, list)
            # brain = [1] #some code somewhere makes us lose a single thing here so this fixes it, brain only, no idea tbh
            # arr1TIC = np.append(arr1TIC, brain)
            arr1TIC = np.asarray(arr1TIC)
            arr2TIC = np.asarray(arr2TIC)
            arr1TIC = np.reshape(arr1TIC, (self.x1, self.y1))
            if len(arr2TIC) != ablen:
                subtract = ablen - len(arr2TIC)
                list = []
                for i in range(0, subtract):
                    list.append(.0001)
                arr2TIC = np.append(arr2TIC, list)
            # brain = [1]  # some code somewhere makes us lose a single thing here so this fixes it, brain only, no idea tbh
            # arr2TIC = np.append(arr2TIC, brain)
            arr2TIC = np.reshape(arr2TIC, (self.x1, self.y1))
            if self.checkbox3.isChecked() == False:
                heatarray1 = np.divide(arr1TIC, arr2TIC)
            else:
                heatarray1 = np.divide(arr2TIC, arr1TIC)
            return heatarray1
        if self.checkbox2.isChecked() == False: #non normalzied image
            arr = self.temp
            try:
                self.array = arr[0]
            except:
                print("arr manip error")
                return

            try:
                self.array1 = arr[15388] #getting abundances at a random pixel somewhere in the middle bc im lazy (to be specific the 29th line at pixel 250)
            except:
                self.array1=arr[0]
            lengthload = len(arr)
            heatarray = np.empty((0), float)
            if self.checkbox5.isChecked() == False:
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
                if self.checkbox5.isChecked() == True:
                    temp = np.sum(a[:,1])
                    heatarray = np.append(heatarray, temp)
                else:
                    a1 = a[:, 0] #a1 = first column of array
                    value = val1
                    array = np.asarray(a1) #turns array into np array
                    mass = a1[np.abs(array - value).argmin()] #search for a value closest to mass inputted
                    rows, cols = np.where(a == mass) #find the row where the mass = the mass searched for
                    abun = a[rows] # does something with the rows
                    self.massFound = abun[0,0]
                    abun = abun[0, 1] #retrives abundance from second row of the mass found row
                    heatarray = np.append(heatarray, abun)# adds abundance to the empty array
            ablen = self.toupleab[0] * (self.toupleab[1]+1)
            if len(heatarray) != ablen:
                subtract = ablen - len(heatarray)
                list = []
                for i in range(0,subtract):
                    list.append(.0001)
                heatarray = np.append(heatarray,list)
            heatarray1 = np.reshape(heatarray, (self.x1, self.y1)) #reshapes the empty array into the size we want
            return heatarray1
        if self.checkbox2.isChecked() == True: #image normalized to other image
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
            try:
                self.array2 = arr1[15388]
            except:
                self.array2 = arr1[0]
            lengthload = len(arr)
            heatarray = np.empty((0), float) #create an emtpy float array
            arr1TIC = []
            arr2TIC = []
            try:
                if self.checkbox5.isChecked() == False:
                    val1 = int(self.line.text())
                else:
                    pass
                if self.checkbox6.isChecked() == False:
                    val2 = int(self.line2.text())
                else:
                    pass
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('No Mass Set!')
                msg.setWindowTitle("Error")
                msg.exec_()
                return
            try:
                ab = arr1[1]
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('No Protein Loaded To Normalize To!')
                msg.setWindowTitle("Error")
                msg.exec_()
                return
            #val1 = int(self.line.text())
            for i in range(0, lengthload):
                a = arr[i]
                if self.checkbox5.isChecked() == True:
                    arr1TIC.append(np.sum(a[:,1]))
                else:
                    a1 = a[:, 0]  # a1 = first column of array
                    value = val1
                    array = np.asarray(a1)  # turns array into np array
                    mass = a1[np.abs(array - value).argmin()]  # search for a value closest to mass inputted
                    rows, cols = np.where(a == mass)  # find the row where the mass = the mass searched for
                    abun = a[rows]  # does something with the rows
                    self.massFound = abun[0, 0]
                    abun = abun[0, 1]  # retrives abundance from second row of the mass found row
                    heatarray = np.append(heatarray, abun)  # adds abundance to the empty array
                    arr1TIC = heatarray
            heatarray1 = np.empty((0), float)
            for i in range(0,lengthload):
                ab = arr1[i]
                if self.checkbox6.isChecked() == True:
                    arr2TIC.append(np.sum(ab[:,1]))
                else:
                    a2 = ab[:, 0]  # a1 = first column of array
                    value = val2
                    array = np.asarray(a2)  # turns array into np array
                    mass = a2[np.abs(array - value).argmin()]  # search for a value closest to mass inputted
                    rows, cols = np.where(ab == mass)  # find the row where the mass = the mass searched for
                    abun1 = ab[rows]  # does something with the rows
                    self.massFound1 = abun1[0, 0]
                    abun1 = abun1[0, 1]  # retrives abundance from second row of the mass found row
                    heatarray1 = np.append(heatarray1, abun1)  # adds abundance to the empty array
                    arr2TIC = heatarray1

                # arr1TIC.append(np.sum(a[:,1]))
                # arr2TIC.append(np.sum(ab[:,1]))
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
            ablen = self.toupleab[0] * (self.toupleab[1] + 1)
            if len(arr1TIC) != ablen:
                subtract = ablen - len(arr1TIC)
                list = []
                for i in range(0, subtract):
                    list.append(.0001)
                arr1TIC = np.append(arr1TIC, list)
            # brain = [1]  # some code somewhere makes us lose a single thing here so this fixes it, brain only, no idea tbh
            # arr1TIC = np.append(arr1TIC, brain)
            arr1TIC = np.reshape(arr1TIC, (self.x1,self.y1))
            if len(arr2TIC) != ablen:
                subtractor = ablen - len(arr2TIC)
                list = []
                for i in range(0, subtractor):
                    list.append(.00001)
                arr2TIC = np.append(arr2TIC, list)
            # brain = [1]  # some code somewhere makes us lose a single thing here so this fixes it, brain only, no idea tbh
            # arr2TIC = np.append(arr2TIC, brain)
            arr2TIC = np.reshape(arr2TIC, (self.x1,self.y1))
            if self.checkbox3.isChecked() == False:
                heatarray1 = np.divide(arr1TIC,arr2TIC)
            else:
                heatarray1 = np.divide(arr2TIC,arr1TIC)
            self.normalused = False
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
                    array = array * (array >= .0001)# if less than 0 make it 0
                except:
                    print("arr maniu error")
                    return
                plt.axis('off')
                if self.checkbox1.isChecked() == True:
                    quantile = np.quantile(array, 0.99)
                    quantile = quantile * float(self.line1.text())
                    im = ax.imshow(array,cmap='hot',interpolation='none',vmax=quantile)
                if self.checkbox1.isChecked() ==False:
                    if (self.checkbox2.isChecked() == True) or (self.checkbox4.isChecked() == True):
                        quantile = np.quantile(array, 0.99)
                        quantile = quantile * float(1)
                        im = ax.imshow(array, cmap='hot', interpolation='none', vmax=quantile)
                    else:
                        im = ax.imshow(array, cmap='hot', interpolation='none')
                ax.set_aspect(5)
                #divider = make_axes_locatable(ax)
                #cax = divider.append_axes("right",size="5%",pad=0.05)
                x1 = self.x1
                cax = self.figure.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height]) #somehow makes my color bar axis the same height as my heatmap
                plt.colorbar(im,cax=cax) #colorbar
                if self.checkbox4.isChecked() == True:
                    if self.checkbox5.isChecked() == True:
                        ax.set_title(str(self.imname0) + "\n" + "TIC Normalized " + " Mass: SUMMED" + "\n",fontsize=10)
                    else:
                        ax.set_title(str(self.imname0)  + "\n" +  "TIC Normalized " +  " Mass: "+ str(int(self.massFound)) + "\n", fontsize=10)
                else:
                    if self.checkbox5.isChecked() == True:
                        ax.set_title(str(self.imname0) + "\n" + "   Mass: SUMMED" + "\n", fontsize=10)
                    else:
                        ax.set_title(str(self.imname0)+ "\n" +"   Mass: " + str(int(self.massFound)) + "\n",fontsize=10)
                self.canvas.draw()
                Window.table(self)
            else:
                array = Window.arraymanipulation(self, self.x1, self.y1)
                if self.checkbox.isChecked() == True:
                    array = array / np.linalg.norm(array)
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.set_axis_on()
                array = array * (array >= .0001)  # if less than 0 make it 0
                plt.axis('off')
                if self.checkbox1.isChecked() == True:
                    quantile = np.quantile(array, 0.99)
                    quantile = quantile * float(self.line1.text())
                    im = ax.imshow(array, cmap='hot', interpolation='none', vmax=quantile)
                if self.checkbox1.isChecked() == False:
                    if (self.checkbox2.isChecked() == True) or (self.checkbox4.isChecked() == True):
                        quantile = np.quantile(array, 0.99)
                        quantile = quantile * float(1)
                        im = ax.imshow(array, cmap='hot', interpolation='none', vmax=quantile)
                    else:
                        im = ax.imshow(array, cmap='hot', interpolation='none')
                ax.set_aspect(5)
                # divider = make_axes_locatable(ax)
                # cax = divider.append_axes("right",size="5%",pad=0.05)
                x1 = self.x1
                cax = self.figure.add_axes([ax.get_position().x1 + 0.01, ax.get_position().y0, 0.02,
                                            ax.get_position().height])  # somehow makes my color bar axis the same height as my heatmap
                plt.colorbar(im, cax=cax)  # colorbar
                #Im aware this is terrible but a smart way would take me longer than writing this monstricity did
                if self.checkbox3.isChecked() == False:
                    if self.checkbox5.isChecked() == True:
                        title = str(self.imname0) + " Mass: SUMMED" + " normalized to " + "\n" + str(self.imname1) + " Mass: " + str(int(self.massFound1)) + "\n"
                    if self.checkbox6.isChecked() == True:
                        title = str(self.imname0) + " Mass: " + str(int(self.massFound)) + " normalized to " + "\n" + str(self.imname1) + " Mass: SUMMED" + "\n"
                    if (self.checkbox5.isChecked() == True) and (self.checkbox6.isChecked() == True):
                        title = str(self.imname0) + " Mass: SUMMED" + " normalized to " + "\n" + str(self.imname1) + " Mass: SUMMED" + "\n"
                    if (self.checkbox5.isChecked() == False) and (self.checkbox6.isChecked() == False):
                        title = str(self.imname0) + " Mass: " + str(int(self.massFound)) + " normalized to " + "\n" + str(self.imname1) + " Mass: "+ str(int(self.massFound1))+ "\n"
                if self.checkbox3.isChecked() == True:
                    if self.checkbox5.isChecked() == True:
                        title = str(self.imname1) + " Mass: SUMMED" + " normalized to " + "\n" + str(self.imname0) + " Mass: "+ str(int(self.massFound))+ "\n"
                    if self.checkbox6.isChecked() == True:
                        title = str(self.imname1) + " Mass: " + str(int(self.massFound1)) + " normalized to " + "\n" + str(self.imname0) + " Mass: SUMMED" + "\n"
                    if (self.checkbox5.isChecked() == True) and (self.checkbox6.isChecked() == True):
                        title = str(self.imname1) + " Mass: SUMMED" + " normalized to " + "\n" + str(self.imname0) + " Mass: SUMMED" + "\n"
                    if (self.checkbox5.isChecked() == False) and (self.checkbox6.isChecked() == False):
                        title = str(self.imname1) + " Mass: " + str(int(self.massFound1)) + " normalized to " + "\n" + str(self.imname0) + " Mass: "+ str(int(self.massFound))+ "\n"
                ax.set_title(title,fontsize=8)
                self.canvas.draw()
                Window.table(self)
        except Exception as e:
            print(traceback.format_exc())
            print("heatmap error")
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