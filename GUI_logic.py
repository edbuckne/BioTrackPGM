# Connected to ui file generated from QTdesigner
# Contains the logic to make interface be able to interact with rest of code/command prompt
# Needs "TestGUIv2.ui" in same directory to work, XML type code

from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QWidget, QScrollBar, QScrollArea, QTreeWidgetItem)

# Eli's custom functions
from fun.dataHandle import loadConfigurationList
from fun.dataHandle import loadSequenceList
from setting_class import settings

spec = 0  # global variable of number of specimens


#  preload = ["config", "threshold", "zres", "xyres", "imagefreq", "width", "height", "timestamps", "1"]


class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class CustomDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        form = QFormLayout()

        self.setWindowTitle("Specimen Configuration")

        groupBox = QGroupBox("")

        for i in range(0, spec):
            y = " "
            x = "Specimen " + str(i + 1)
            form.addRow(QLabel(y))
            form.addRow(QLabel(x))
            form.addRow(QLabel("Initial X"), QLineEdit())
            form.addRow(QLabel("X Guess"), QLineEdit())
            form.addRow(QLabel("Initial Y"), QLineEdit())
            form.addRow(QLabel("Y Guess"), QLineEdit())
            form.addRow(QLabel("Z1"), QLineEdit())
            form.addRow(QLabel("Z2"), QLineEdit())

            self.setLayout(form)
        cancelSpecConfig = QPushButton("Cancel")
        saveSpecConfig = QPushButton("Save")
        form.addRow(cancelSpecConfig, saveSpecConfig)  # TODO Connect buttons to action

        groupBox.setLayout(form)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

        self.show()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        global spec

        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('TestGUIv2.ui', self)  # Load the .ui file

        # Buttons and Connections
        self.button = self.findChild(QtWidgets.QPushButton, 'save')  # Find the button with the name "save"
        self.button.clicked.connect(self.saveButtonPressed)

        self.button2 = self.findChild(QtWidgets.QPushButton, 'configbutton')
        self.button2.clicked.connect(self.windowButtonPressed)

        # Tree Widget(s) and connections
        self.configTree = self.findChild(QtWidgets.QTreeWidget, 'configTree')
        self.configTree.itemDoubleClicked.connect(self.showitemConfig)

        self.sequenceTree = self.findChild(QtWidgets.QTreeWidget, 'sequenceTree')
        self.sequenceTree.itemDoubleClicked.connect(self.showitemSequence)

        # Loads list into tree widget(s)
        configlist = loadConfigurationList()
        for x in range(0, len(configlist)):  # configTree Tree Widget
            item = QTreeWidgetItem()
            item.setText(0, configlist[x])  # file name

            self.configTree.addTopLevelItem(item)

        sequencelist = loadSequenceList()
        for x in range(0, len(sequencelist)):  # sequenceTree Tree Widget
            item = QTreeWidgetItem()
            item.setText(0, sequencelist[x])  # file name

            self.sequenceTree.addTopLevelItem(item)

        # Text box names
        self.config = self.findChild(QtWidgets.QLineEdit, 'config')
        self.thresh = self.findChild(QtWidgets.QLineEdit, 'thresh')
        self.zres = self.findChild(QtWidgets.QLineEdit, 'zres')
        self.xyres = self.findChild(QtWidgets.QLineEdit, 'xyres')
        self.imagefreq = self.findChild(QtWidgets.QLineEdit, 'imagefreq')
        self.width = self.findChild(QtWidgets.QLineEdit, 'width')
        self.height = self.findChild(QtWidgets.QLineEdit, 'height')
        self.timestamps = self.findChild(QtWidgets.QLineEdit, 'timestamps')
        self.specimennum = self.findChild(QtWidgets.QLineEdit, 'specimennum')

        # Settings Children
        self.shiftCheckBox = self.findChild(QtWidgets.QCheckBox, 'shiftCheckBox')
        self.printCheckBox = self.findChild(QtWidgets.QCheckBox, 'printCheckBox')
        self.xPosCheckBox = self.findChild(QtWidgets.QCheckBox, 'xPosCheckBox')
        self.xNegCheckBox = self.findChild(QtWidgets.QCheckBox, 'xNegCheckBox')
        self.yPosCheckBox = self.findChild(QtWidgets.QCheckBox, 'yPosCheckBox')
        self.yNegCheckBox = self.findChild(QtWidgets.QCheckBox, 'yNegCheckBox')
        self.zPosCheckBox = self.findChild(QtWidgets.QCheckBox, 'zPosCheckBox')
        self.zNegCheckBox = self.findChild(QtWidgets.QCheckBox, 'zNegCheckBox')
        self.settingsSaveName = self.findChild(QtWidgets.QLineEdit, 'settingsSaveName')
        self.settingsLoadName = self.findChild(QtWidgets.QLineEdit, 'settingsLoadName')

        # Sets text of predetermined settings on start only
        # self.config.setText(preload[0])
        # self.thresh.setText(preload[1])
        # self.zres.setText(preload[2])
        # self.xyres.setText(preload[3])
        # self.imagefreq.setText(preload[4])
        # self.width.setText(preload[5])
        # self.height.setText(preload[6])
        # self.timestamps.setText(preload[7])
        # self.specimennum.setText(preload[8])

        # spec = self.specimennum.text()
        # spec = int(float(spec))

        self.show()  # Show the GUI

    def saveButtonPressed(self):
        # This is executed when the button is pressed
        global spec  # TODO add variables to save all the fields
        spec = self.specimennum.text()
        spec = int(float(spec))
        x = "Configuration " + self.config.text() + " has been saved!"
        print(x)
        # TODO add method to constantly update GUI for live updating
        # self.setupFile.addItem(self.config.text()) method 1
        # item = QTreeWidgetItem method 2
        # item.setText(0, self.config.text())
        # item.setText(1, "?")

    def windowButtonPressed(self):

        global spec
        try:
            spec = self.specimennum.text()
            spec = int(float(spec))
        except(ValueError, Exception):
            print("Put a valid integer for Specimen Number")  # TODO Make this dialog box
            spec = 0

        dlg = CustomDialog(self)

        if dlg.exec_():
            print("Configuration Saved!")
        else:
            print("Configuration Not Saved!")

    def showitemConfig(self, item, column):
        print("Config has been double clicked:", item.text(column))
        # TODO When an item is double clicked needs to update the boxes for settings and setup tabs

    def showitemSequence(self, item, column):
        print("Sequence has been double clicked:", item.text(column))


app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
window = Ui()  # Create an instance of our class
app.exec_()  # Start the application
