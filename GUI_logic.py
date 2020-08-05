# Connected to ui file generated from QTdesigner
# Contains the logic to make interface be able to interact with rest of code/command prompt
# Needs "TestGUIv2.ui" in same directory to work, XML type code

from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QMessageBox, QFileDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QWidget, QScrollBar, QScrollArea, QTreeWidgetItem)

# Eli's custom functions
from fun.dataHandle import loadConfigurationList
from fun.dataHandle import loadSequenceList
from registration_class import registration
from bioTRACKai import run_experiment
from setting_class import settings
from config_class import config
import numpy as np
import pickle
import os

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
            form.addRow(QLabel("Initial X growth"), QLineEdit())
            form.addRow(QLabel("Initial Y"), QLineEdit())
            form.addRow(QLabel("Initial Y growth"), QLineEdit())
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

        # Parsing the information of files available for loading into a selectable list
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

        # Making connections in this code to the objects in the ui file
        # Buttons and Connections
        self.button = self.findChild(QtWidgets.QPushButton, 'save')  # Find the button with the name "save"
        self.button.clicked.connect(self.saveButtonPressed)

        self.button2 = self.findChild(QtWidgets.QPushButton, 'configbutton')
        self.button2.clicked.connect(self.windowButtonPressed)

        self.runSimButton = self.findChild(QtWidgets.QPushButton, 'pushButton_3')  # TODO change name in ui file to runSimButton
        self.runSimButton.clicked.connect(self.runSimButtonPressed)

        self.runExpButton = self.findChild(QtWidgets.QPushButton, 'pushButton_4')  # TODO change name in ui file to runExpButton
        self.runExpButton.clicked.connect(self.runExpButtonPressed)

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

        # Drop down boxes
        self.registrationDropDown = self.findChild(QtWidgets.QComboBox, 'comboBox')
        self.zAxisUnits = self.findChild(QtWidgets.QComboBox, 'zAxisUnits')
        self.xyResUnits = self.findChild(QtWidgets.QComboBox, 'xyResUnits')
        self.imageFreqUnits = self.findChild(QtWidgets.QComboBox, 'imageFreqUnits')

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

        # spec = self.specimennum.text()
        # spec = int(float(spec))

        self.show()  # Show the GUI

    # This function is called when the save configuration button is pressed on the configuration page. It takes all of
    # the information in the fields, creates a configuration object with that information, and saves/overwrites the
    # file that holds that information.
    def saveButtonPressed(self):
        conf = config(settings(), create=False, load=True, configLoad='default')
        conf.name = self.config.text()

        try:
            exp_matrix = np.empty([8])
            exp_matrix[0] = int(float(self.specimennum.text()))  # Number of specimen
            exp_matrix[1] = int(float(self.height.text()))  # Height of image in pixels
            exp_matrix[2] = int(float(self.width.text()))  # Width of image in pixels
            exp_matrix[3] = float(self.xyres.text())  # Lateral resolution of pixels in microns
            exp_matrix[4] = int(float(self.timestamps.text()))  # Number of images to take in the time course
            exp_matrix[5] = int(float(self.imagefreq.text()))  # Frequency in capturing images in minutes
            exp_matrix[6] = int(float(self.thresh.text()))  # 16-bit threshold value for determining what is GFP signal
            exp_matrix[7] = float(self.zres.text())  # The axial resolutions of z-slices in microns
            conf.expConfig = exp_matrix
        except:
            saveError = QMessageBox()
            saveError.setText('An error has occurred during saving. Make sure all fields are filled')
            saveError.exec()
            return


        registrationChannel = 1  # Need to collect the registration channel when this gets put in
        regInd = self.registrationDropDown.currentIndex()  # Collect and save the registration method
        for spm in range(int(exp_matrix[0])):
            if regInd == 0:
                conf.registration.append(registration('PMIR', registrationChannel))
            elif regInd == 1:
                conf.registration.append(registration('COMR', registrationChannel))
            elif regInd == 2:
                conf.registration.append(registration('RMSR', registrationChannel))

        conf.axialUnits = self.zAxisUnits.currentIndex()  # Collect and save the indices for the units
        conf.lateralUnits = self.xyResUnits.currentIndex()
        conf.imageFrequencyUnits = self.imageFreqUnits.currentIndex()

        if(os.path.isdir('./mat/conf/' + conf.name)):  # If this configuration already exists, overwrite it
            os.remove('./mat/conf/' + conf.name + '/configclass.pkl')
        else:  # Otherwise create a new file
            os.mkdir('./mat/conf/' + conf.name)  # Create and save new configuration
            item = QTreeWidgetItem()  # Update the list to include this item
            item.setText(0, conf.name)  # file name
            self.configTree.addTopLevelItem(item)
        with open('./mat/conf/' + conf.name + '/configclass.pkl',
                  'wb') as f:  # Creating a pickle file that is writable
            pickle.dump(conf, f)
        f.close()

        # This is executed when the button is pressed
        global spec
        spec = self.specimennum.text()
        spec = int(float(spec))

        return conf


    # This function runs when the run simulation button has been pressed. It saves the configuration currently entered
    # into the fields, gathers them in a configuration object, and runs the simulation. If there is an error in running
    # this, an error message is printed on the terminal.
    def runSimButtonPressed(self):
        file = str(QFileDialog.getExistingDirectory(self, 'Select directory where images will be saved'))
        conf = self.saveButtonPressed()  # Save this current configuration
        conf.path = file
        try:
            run_experiment(conf, 0, simulation=True)
        except:
            print('Error running simulation')
            return


    # This function runs when the run simulation button has been pressed. It saves the configuration currently entered
    # into the fields, gathers them in a configuration object, and runs the simulation. If there is an error in running
    # this, an error message is printed on the terminal.
    def runExpButtonPressed(self):
        file = str(QFileDialog.getExistingDirectory(self, 'Select directory where images will be saved'))
        conf = self.saveButtonPressed()  # Save this current configuration
        conf.path = file
        try:
            run_experiment(conf, 0, simulation=False)
        except:
            print('Error running experiment')
            return


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


    # This function is called when an item from the pre-existing configuration list. That configuration's information
    # is loaded into a configuration object and the information from the object is parsed into the fields on the GUI.
    def showitemConfig(self, item, column):
        sett = settings()
        conf = config(sett, create=False, load=True, configLoad=item.text(column))

        self.config.setText(conf.name)  # Parsing the data from the clicked object into the fields
        self.thresh.setText(str(conf.expConfig[6]))
        self.zres.setText(str(conf.expConfig[7]))
        self.xyres.setText(str(conf.expConfig[3]))
        self.imagefreq.setText(str(conf.expConfig[5]))
        self.width.setText(str(conf.expConfig[1]))
        self.height.setText(str(conf.expConfig[2]))
        self.timestamps.setText(str(conf.expConfig[4]))
        self.specimennum.setText(str(conf.expConfig[0]))

        if conf.registration[0].method == 'PMIR':  # Set the drop down to match what is in the configuration file
            self.registrationDropDown.setCurrentIndex(0)
        elif conf.registration[0].method == 'COMR':
            self.registrationDropDown.setCurrentIndex(1)
        elif conf.registration[0].method == 'RMSR':
            self.registrationDropDown.setCurrentIndex(2)

        self.zAxisUnits.setCurrentIndex(conf.axialUnits)  # Set the units of the dropdowns for the units
        self.xyResUnits.setCurrentIndex(conf.lateralUnits)
        self.imageFreqUnits.setCurrentIndex(conf.imageFrequencyUnits)
        # TODO When an item is double clicked needs to update the boxes for settings and setup tabs

    def showitemSequence(self, item, column):
        print("Sequence has been double clicked:", item.text(column))


app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
window = Ui()  # Create an instance of our class
app.exec_()  # Start the application
