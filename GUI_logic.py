# Connected to ui file generated from QTdesigner
# Contains the logic to make interface be able to interact with rest of code/command prompt
# Needs "TestGUIv2.ui" in same directory to work, XML type code

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSignal
import sys
# import sip
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (QComboBox, QMessageBox, QFileDialog,
                             QFormLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QScrollArea,
                             QTreeWidgetItem, qApp, QAbstractItemView, QListWidgetItem)

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

spec = 0  # total number of specimens
widgetNum = 0  # total number of widgets for specimen window
splits = 0  # total number of splits of array for specimen window # TODO minimize globals or make them unique enough


class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class clickBox(QtWidgets.QDialog):  # Is it bad to have class based variables? Accessible to the entire class?
    def appendClickPressed(self):
        item = QTreeWidgetItem()
        name = "Click: " + self.xClick.text() + ", " + self.yClick.text() + ", " + self.numClicks.text() + ", " + \
               self.timeClicks.text()
        # TODO figure out error thing so people don't enter settings that make no sense
        # if self.numClicks.text() or self.xClick.text() or self.yClick.text() or self.timeClicks.text() == "":
        #     saveError = QMessageBox()
        #     saveError.setText('An error has occurred during saving. Make sure all fields are filled')
        #     saveError.exec()
        # else:
        item.setText(0, name)
        self.sequenceBox.addTopLevelItem(item)
        self.close()

    def insertClickPressed(self):
        item = QTreeWidgetItem()
        name = "Click: " + self.xClick.text() + ", " + self.yClick.text() + ", " + self.numClicks.text() + ", " + \
               self.timeClicks.text()
        item.setText(0, name)
        row = self.sequenceBox.currentIndex().row()
        self.sequenceBox.insertTopLevelItem(row, item)
        self.close()

    def cancelClickPressed(self):
        self.close()

    def __init__(self, sequence):
        super(clickBox, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('clickBox.ui', self)  # Load the .ui file

        # Text Fields
        self.numClicks = self.findChild(QtWidgets.QLineEdit, 'numClicks')
        self.xClick = self.findChild(QtWidgets.QLineEdit, 'xClick')
        self.yClick = self.findChild(QtWidgets.QLineEdit, 'yClick')
        self.timeClicks = self.findChild(QtWidgets.QLineEdit, 'timeClicks')

        self.sequenceBox = sequence

        # Buttons
        self.appendClick = self.findChild(QtWidgets.QPushButton, 'appendClick')
        self.insertClick = self.findChild(QtWidgets.QPushButton, 'insertClick')
        self.cancelClick = self.findChild(QtWidgets.QPushButton, 'cancelClick')

        # Signals
        self.appendClick.clicked.connect(self.appendClickPressed)

        self.insertClick.clicked.connect(self.insertClickPressed)

        self.cancelClick.clicked.connect(self.cancelClickPressed)

        # Show the GUI
        self.show()


class stringBox(QtWidgets.QDialog):  # Is it bad to have class based variables? Accessible to the entire class?
    def appendActionPressed(self):
        item = QTreeWidgetItem()
        name = "String: " + self.stringName.text()
        # TODO figure out error thing so people don't enter settings that make no sense
        # if self.numClicks.text() or self.xClick.text() or self.yClick.text() or self.timeClicks.text() == "":
        #     saveError = QMessageBox()
        #     saveError.setText('An error has occurred during saving. Make sure all fields are filled')
        #     saveError.exec()
        # else:
        item.setText(0, name)
        self.sequenceBox.addTopLevelItem(item)
        self.close()

    def insertActionSequencePressed(self):
        item = QTreeWidgetItem()
        name = "String: " + self.stringName.text()
        item.setText(0, name)
        row = self.sequenceBox.currentIndex().row()
        self.sequenceBox.insertTopLevelItem(row, item)
        self.close()

    def cancelActionPressed(self):
        self.close()

    def __init__(self, sequence):
        super(stringBox, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('stringBox.ui', self)  # Load the .ui file

        # Text Fields
        self.stringName = self.findChild(QtWidgets.QLineEdit, 'stringName')

        self.sequenceBox = sequence

        # Buttons
        self.appendAction = self.findChild(QtWidgets.QPushButton, 'appendAction')
        self.insertActionSequence = self.findChild(QtWidgets.QPushButton, 'insertAction')
        self.cancelAction = self.findChild(QtWidgets.QPushButton, 'cancelAction')

        # Signals
        self.appendAction.clicked.connect(self.appendActionPressed)

        self.insertActionSequence.clicked.connect(self.insertActionSequencePressed)

        self.cancelAction.clicked.connect(self.cancelActionPressed)

        # Show the GUI
        self.show()


class valueBox(QtWidgets.QDialog):  # Is it bad to have class based variables? Accessible to the entire class?
    def appendActionPressed(self):
        item = QTreeWidgetItem()
        name = "Value: " + self.valueOption.currentText() + ", " + self.value.text() + ", " + \
               self.valueUnits.currentText()
        # TODO figure out error thing so people don't enter settings that make no sense
        # if self.numClicks.text() or self.xClick.text() or self.yClick.text() or self.timeClicks.text() == "":
        #     saveError = QMessageBox()
        #     saveError.setText('An error has occurred during saving. Make sure all fields are filled')
        #     saveError.exec()
        # else:
        item.setText(0, name)
        self.sequenceBox.addTopLevelItem(item)
        self.close()

    def insertActionSequencePressed(self):
        item = QTreeWidgetItem()
        name = "Value: " + self.valueOption.currentText() + ", " + self.value.text() + ", " + \
               self.valueUnits.currentText()
        item.setText(0, name)
        row = self.sequenceBox.currentIndex().row()
        self.sequenceBox.insertTopLevelItem(row, item)
        self.close()

    def cancelActionPressed(self):
        self.close()

    def __init__(self, sequence):
        super(valueBox, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('valueBox.ui', self)  # Load the .ui file

        # Text Fields
        self.value = self.findChild(QtWidgets.QLineEdit, 'value')
        self.valueOption = self.findChild(QtWidgets.QComboBox, 'valueOption')
        self.valueUnits = self.findChild(QtWidgets.QComboBox, 'valueUnits')

        self.sequenceBox = sequence

        # Buttons
        self.appendAction = self.findChild(QtWidgets.QPushButton, 'appendAction')
        self.insertActionSequence = self.findChild(QtWidgets.QPushButton, 'insertAction')
        self.cancelAction = self.findChild(QtWidgets.QPushButton, 'cancelAction')

        # Signals
        self.appendAction.clicked.connect(self.appendActionPressed)

        self.insertActionSequence.clicked.connect(self.insertActionSequencePressed)

        self.cancelAction.clicked.connect(self.cancelActionPressed)

        # Show the GUI
        self.show()


class specialKeyBox(QtWidgets.QDialog):  # Is it bad to have class based variables? Accessible to the entire class?
    def appendActionPressed(self):
        item = QTreeWidgetItem()
        name = self.specialKey.currentText()
        # TODO figure out error thing so people don't enter settings that make no sense
        # if self.numClicks.text() or self.xClick.text() or self.yClick.text() or self.timeClicks.text() == "":
        #     saveError = QMessageBox()
        #     saveError.setText('An error has occurred during saving. Make sure all fields are filled')
        #     saveError.exec()
        # else:
        item.setText(0, name)
        self.sequenceBox.addTopLevelItem(item)
        self.close()

    def insertActionSequencePressed(self):
        item = QTreeWidgetItem()
        name = self.specialKey.currentText()
        item.setText(0, name)
        row = self.sequenceBox.currentIndex().row()
        self.sequenceBox.insertTopLevelItem(row, item)
        self.close()

    def cancelActionPressed(self):
        self.close()

    def __init__(self, sequence):
        super(specialKeyBox, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('specialKeyBox.ui', self)  # Load the .ui file

        # Text Fields
        self.specialKey = self.findChild(QtWidgets.QComboBox, 'specialKey')

        self.sequenceBox = sequence

        # Buttons
        self.appendAction = self.findChild(QtWidgets.QPushButton, 'appendAction')
        self.insertActionSequence = self.findChild(QtWidgets.QPushButton, 'insertAction')
        self.cancelAction = self.findChild(QtWidgets.QPushButton, 'cancelAction')

        # Signals
        self.appendAction.clicked.connect(self.appendActionPressed)
        self.insertActionSequence.clicked.connect(self.insertActionSequencePressed)
        self.cancelAction.clicked.connect(self.cancelActionPressed)

        # Show the GUI
        self.show()


class pauseBox(QtWidgets.QDialog):  # Is it bad to have class based variables? Accessible to the entire class?
    def appendActionPressed(self):
        item = QTreeWidgetItem()
        name = "Pause: " + self.pause.text() + ", " + self.pauseUnits.currentText()
        # TODO figure out error thing so people don't enter settings that make no sense
        # if self.numClicks.text() or self.xClick.text() or self.yClick.text() or self.timeClicks.text() == "":
        #     saveError = QMessageBox()
        #     saveError.setText('An error has occurred during saving. Make sure all fields are filled')
        #     saveError.exec()
        # else:
        item.setText(0, name)
        self.sequenceBox.addTopLevelItem(item)
        self.close()

    def insertActionSequencePressed(self):
        item = QTreeWidgetItem()
        name = "Pause: " + self.pause.text() + ", " + self.pauseUnits.currentText()
        item.setText(0, name)
        row = self.sequenceBox.currentIndex().row()
        self.sequenceBox.insertTopLevelItem(row, item)
        self.close()

    def cancelActionPressed(self):
        self.close()

    def __init__(self, sequence):
        super(pauseBox, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('pauseBox.ui', self)  # Load the .ui file

        # Text Fields
        self.pause = self.findChild(QtWidgets.QLineEdit, 'pause')
        self.pauseUnits = self.findChild(QtWidgets.QComboBox, 'pauseUnits')

        self.sequenceBox = sequence

        # Buttons
        self.appendAction = self.findChild(QtWidgets.QPushButton, 'appendAction')
        self.insertActionSequence = self.findChild(QtWidgets.QPushButton, 'insertAction')
        self.cancelAction = self.findChild(QtWidgets.QPushButton, 'cancelAction')

        # Signals
        self.appendAction.clicked.connect(self.appendActionPressed)
        self.insertActionSequence.clicked.connect(self.insertActionSequencePressed)
        self.cancelAction.clicked.connect(self.cancelActionPressed)

        # Show the GUI
        self.show()


class specimenConfigDialog(QtWidgets.QDialog):

    def saveSpecConfigButtonPressed(self):  # TODO connect with backend
        specInfo = [0] * widgetNum
        global splits
        for i in range(0, widgetNum):
            if i % 9 == 8:
                splits = splits + 1
                widgInfo = self.form.itemAt(i, 1).widget()
                widgTxt = widgInfo.currentText()
                specInfo[i] = widgTxt
                continue
            widgInfo = self.form.itemAt(i, 1).widget()
            widgTxt = widgInfo.text()
            specInfo[i] = widgTxt
        specInfoParsed = np.array_split(specInfo, splits)  # Array you can access that has each specimen data set
        self.close()

    def cancelSpecConfigButtonPressed(self):
        self.close()

    def __init__(self, specimen=None, *args, **kwargs):
        super(specimenConfigDialog, self).__init__(*args, **kwargs)

        self.form = QFormLayout()

        self.setWindowTitle("Specimen Configuration")

        groupBox = QGroupBox("")

        global widgetNum

        for i in range(0, spec):
            blank = QLabel(" ")
            specName = QLabel("Specimen " + str(i + 1))
            sequence = QLabel("Sequence")
            seqList = QComboBox()
            sequencelist = loadSequenceList()
            for x in range(0, len(sequencelist)):  # sequenceTree Tree Widget
                seqList.addItem(sequencelist[x])
            self.form.addRow(blank)
            self.form.addRow(specName)
            self.form.addRow(QLabel("Initial X"), QLineEdit())
            self.form.addRow(QLabel("Initial X growth"), QLineEdit())
            self.form.addRow(QLabel("Initial Y"), QLineEdit())
            self.form.addRow(QLabel("Initial Y growth"), QLineEdit())
            self.form.addRow(QLabel("Z1"), QLineEdit())
            self.form.addRow(QLabel("Z2"), QLineEdit())
            self.form.addRow(sequence, seqList)

            widgetNum = widgetNum + 9

            self.setLayout(self.form)

        self.cancelSpecConfig = QPushButton("Cancel")
        self.saveSpecConfig = QPushButton("Save")
        self.form.addRow(self.cancelSpecConfig, self.saveSpecConfig)

        # Signals
        self.saveSpecConfig.clicked.connect(self.saveSpecConfigButtonPressed)
        self.cancelSpecConfig.clicked.connect(self.cancelSpecConfigButtonPressed)

        # Layout and Scroll Area
        groupBox.setLayout(self.form)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

        # Shows GUI
        self.show()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        global spec
        # global trigger

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
        # Config Buttons and Connections
        self.button = self.findChild(QtWidgets.QPushButton, 'save')
        self.button.clicked.connect(self.saveButtonPressed)

        self.button2 = self.findChild(QtWidgets.QPushButton, 'configButton')
        self.button2.clicked.connect(self.windowButtonPressed)

        self.configDeleteButton = self.findChild(QtWidgets.QPushButton, 'deleteConfig')
        self.configDeleteButton.clicked.connect(self.removeItemTreeConfig)

        self.runSimButton = self.findChild(QtWidgets.QPushButton, 'runSimButton')
        self.runSimButton.clicked.connect(self.runSimButtonPressed)

        self.runExpButton = self.findChild(QtWidgets.QPushButton, 'runExpButton')
        self.runExpButton.clicked.connect(self.runExpButtonPressed)

        self.actionDialogBox = []  # TODO might break lmao

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
        self.microChannel = self.findChild(QtWidgets.QLineEdit, 'microChannel')

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

        # Sequence Children
        self.sequenceBuildArea = self.findChild(QtWidgets.QTreeWidget, 'sequenceBuildArea')  # QListWidget

        self.clickAction = self.findChild(QtWidgets.QPushButton, 'clickAction')
        self.clickAction.clicked.connect(self.clickActionPressed)

        self.stringAction = self.findChild(QtWidgets.QPushButton, 'stringAction')
        self.stringAction.clicked.connect(self.stringActionPressed)

        self.valueAction = self.findChild(QtWidgets.QPushButton, 'valueAction')
        self.valueAction.clicked.connect(self.valueActionPressed)

        self.Action = self.findChild(QtWidgets.QPushButton, 'specialKeyAction')
        self.specialKeyAction.clicked.connect(self.specialKeyActionPressed)

        self.pauseAction = self.findChild(QtWidgets.QPushButton, 'pauseAction')
        self.pauseAction.clicked.connect(self.pauseActionPressed)

        # Show the GUI
        self.show()

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
        except(ValueError, Exception):
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

        if (os.path.isdir('./mat/conf/' + conf.name)):  # If this configuration already exists, overwrite it
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

        global spec
        spec = self.specimennum.text()
        spec = int(float(spec))

        return conf

    # This function runs when the run simulation button has been pressed. It saves the configuration currently entered
    # into the fields, gathers them in a configuration object, and runs the simulation. If there is an error in running
    # this, an error message is printed on the terminal.
    def runSimButtonPressed(self):
        file = str(QFileDialog.getExistingDirectory(self, 'Select directory where images will be saved'))
        conf = self.saveButtonPressed()
        conf.path = file
        try:
            run_experiment(conf, 0, simulation=True)
        except(ValueError, Exception):  # TODO Make this dialog or sound?
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
        except(ValueError, Exception):
            print('Error running experiment')  # TODO Make this dialog or sound?
            return

# These functions open the related action dialog boxes

    def clickActionPressed(self):
        try:
            self.actionDialogBox = clickBox(self.sequenceBuildArea)
            self.actionDialogBox.exec_()

        except(ValueError, Exception):
            saveError = QMessageBox()
            saveError.setText('Sorry try again')
            saveError.exec()
            return

    def stringActionPressed(self):
        try:
            self.actionDialogBox = stringBox(self.sequenceBuildArea)
            self.actionDialogBox.exec_()

        except(ValueError, Exception):
            saveError = QMessageBox()
            saveError.setText('Sorry try again')
            saveError.exec()
            return

    def valueActionPressed(self):
        try:
            self.actionDialogBox = valueBox(self.sequenceBuildArea)
            self.actionDialogBox.exec_()

        except(ValueError, Exception):
            saveError = QMessageBox()
            saveError.setText('Sorry try again')
            saveError.exec()
            return

    def specialKeyActionPressed(self):
        try:
            self.actionDialogBox = specialKeyBox(self.sequenceBuildArea)
            self.actionDialogBox.exec_()

        except(ValueError, Exception):
            saveError = QMessageBox()
            saveError.setText('Sorry try again')
            saveError.exec()
            return

    def pauseActionPressed(self):
        try:
            self.actionDialogBox = pauseBox(self.sequenceBuildArea)
            self.actionDialogBox.exec_()

        except(ValueError, Exception):
            saveError = QMessageBox()
            saveError.setText('Sorry try again')
            saveError.exec()
            return

# Specimen Window function that enables editing specimen setting info

    def windowButtonPressed(self):
        global spec
        try:
            spec = self.specimennum.text()
            spec = int(float(spec))

            dlg = specimenConfigDialog(self)
            dlg.exec_()

        except(ValueError, Exception):
            saveError = QMessageBox()
            saveError.setText('Enter a Valid Number For Specimen Amount')
            saveError.exec()
            return

# This function is called when an item from the pre-existing configuration list. That configuration's information
# is loaded into a configuration object and the information from the object is parsed into the fields on the GUI.
    def showitemConfig(self, item, column):
        try:
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
        except(ValueError, Exception):
            print("config load failed")

    # TODO When an item is double clicked needs to update the boxes for settings and setup tabs

    def showitemSequence(self, item, column):
        print("Sequence has been double clicked:", item.text(column))

    def removeItemTreeConfig(self):
        row = self.configTree.currentIndex().row()
        name = self.configTree.currentItem().text(0)
        print(name)
        self.configTree.takeTopLevelItem(row)


app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
window = Ui()  # Create an instance of our class
app.exec_()  # Start the application
