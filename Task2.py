from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd


class TimeDomainCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = fig.add_subplot(111)
        super(TimeDomainCanvas, self).__init__(fig)


class FrequencyDomainCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = fig.add_subplot(111)
        super(FrequencyDomainCanvas, self).__init__(fig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1088, 673)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Time Domain Layout
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 821, 281))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.timeDomainCanvas = TimeDomainCanvas(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.timeDomainCanvas)

        # Frequency Domain Layout
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 340, 821, 281))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.frequencyDomainCanvas = FrequencyDomainCanvas(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.addWidget(self.frequencyDomainCanvas)
        
        # Labels
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 310, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # GroupBox
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(840, 30, 241, 591))
        self.groupBox.setObjectName("groupBox")
        self.zoomInButton = QtWidgets.QPushButton(self.groupBox)
        self.zoomInButton.setGeometry(QtCore.QRect(20, 40, 93, 28))
        self.zoomInButton.setObjectName("zoomInButton")
        self.zoomOutButton = QtWidgets.QPushButton(self.groupBox)
        self.zoomOutButton.setGeometry(QtCore.QRect(130, 40, 93, 28))
        self.zoomOutButton.setObjectName("zoomOutButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1088, 26))
        self.menubar.setObjectName("menubar")
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.setObjectName("menuOpen")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuOpen.menuAction())

        # Add open action to menu
        self.actionOpenFile = QtWidgets.QAction("Open File", MainWindow)
        self.menuOpen.addAction(self.actionOpenFile)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect the open action
        self.actionOpenFile.triggered.connect(self.open_ecg_file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Time Graph:"))
        self.label_2.setText(_translate("MainWindow", "Frequency Graph:"))
        self.groupBox.setTitle(_translate("MainWindow", "Controls"))
        self.zoomInButton.setText(_translate("MainWindow", "Zoom In"))
        self.zoomOutButton.setText(_translate("MainWindow", "Zoom Out"))
        self.menuOpen.setTitle(_translate("MainWindow", "Open"))

    def open_ecg_file(self):
    # Open a file dialog to select a CSV file
        file_path, _ = QFileDialog.getOpenFileName(None, "Open ECG CSV File", "", "CSV Files (*.csv)")
        if file_path:
                # Read the CSV file (with headers assumed)
            data = pd.read_csv(file_path)
    
            data = pd.read_csv(file_path, header=None)
            time = data[0]  # First column for time
            ecg = data[1]  # Second column for ECG

                # Plot the ECG data
            self.timeDomainCanvas.axes.clear()
            self.timeDomainCanvas.axes.plot(time, ecg, label="ECG Signal")
            self.timeDomainCanvas.axes.set_title("ECG Signal - Time Domain")
            self.timeDomainCanvas.axes.set_xlabel("Time (s)")
            self.timeDomainCanvas.axes.set_ylabel("Amplitude")
            self.timeDomainCanvas.axes.legend()
            self.timeDomainCanvas.draw()
            

            


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
