from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
import sys
# from win32api import GetSystemMetrics
#
#
# # Set Dynamic Window Size
# xpos = GetSystemMetrics(0)/3;
# ypos = GetSystemMetrics(1)/3;
# width = GetSystemMetrics(0)/2;
# height = GetSystemMetrics(1)/2;


def window(): # Basic Main Window
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(100, 100, 500, 500) # xpos, ypos, width, height, relative to top left of screen
    win.setWindowTitle("Root Tracker") # Title of Window at top

    # lA = QtWidgets.QLabel(window)
    # lB = QtWidgets.QLabel(window)
    # lC = QtWidgets.QLabel(window)
    # lD = QtWidgets.QLabel(window)
    # lE = QtWidgets.QLabel(window)
    #
    #
    # lA.setText("Setup")
    # lB.setText("Run")
    # lC.setText("Sequence")
    # lD.setText("Simulation")
    # lE.setText("Settings")

    win.show()
    sys.exit(app.exec_()) # allows for exiting

window()

