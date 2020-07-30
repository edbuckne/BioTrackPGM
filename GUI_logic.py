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
# from fun.dataHandle import loadConfigurationList # TODO move files so these imports work
# from fun.dataHandle import loadSequenceList()
# from setting_class import settings

spec = 0  # global variable of number of specimens
preload = ["config", "threshold", "zres", "xyres", "imagefreq", "width", "height", "timestamps", "1"]


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

        # TODO figure out scroll bar
        # self.scroll = QScrollArea
        # self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scroll.setWidgetResizable(True)
        # self.scroll.setWidget(self.widget)

        if spec == 0:
            print("Please Enter a Specimen Number and try again")  # TODO make this dialog box
        else:
            for i in range(0, spec):
                x = "Specimen " + str(i + 1)
                form.addRow(QLabel(x))
                form.addRow(QLabel("Initial X"), QLineEdit())
                form.addRow(QLabel("X Guess"), QLineEdit())
                form.addRow(QLabel("Initial Y"), QLineEdit())
                form.addRow(QLabel("Y Guess"), QLineEdit())
                form.addRow(QLabel("Z1"), QLineEdit())
                form.addRow(QLabel("Z2"), QLineEdit())

                self.setLayout(form)
        form.addRow(QPushButton("Cancel"), QPushButton("Save")) # TODO Connect buttons to action

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
        self.setupFile = self.findChild(QtWidgets.QTreeWidget, 'setupSavedFiles')
        self.setupFile.itemDoubleClicked.connect(self.showitem)

        # Loads list into tree widget(s)
        for x in range(0, len(preload)): # setupFile Tree Widget
            item = QTreeWidgetItem()
            item.setText(0, preload[x])  # file name
            item.setText(1, "?")  # date modified

            self.setupFile.addTopLevelItem(item)

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

        # Sets text of predetermined settings on start only
        self.config.setText(preload[0])
        self.thresh.setText(preload[1])
        self.zres.setText(preload[2])
        self.xyres.setText(preload[3])
        self.imagefreq.setText(preload[4])
        self.width.setText(preload[5])
        self.height.setText(preload[6])
        self.timestamps.setText(preload[7])
        self.specimennum.setText(preload[8])

        spec = self.specimennum.text()
        spec = int(float(spec))

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
        spec = self.specimennum.text()
        spec = int(float(spec))

        dlg = CustomDialog(self)

        if dlg.exec_():
            print("Configuration Saved!")
        else:
            print("Configuration Not Saved!")

    def showitem(self, item, column):
        print("Item has been double clicked:", item.text(column))


app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
window = Ui()  # Create an instance of our class
app.exec_()  # Start the application
