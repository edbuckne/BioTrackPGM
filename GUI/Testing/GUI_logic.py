# Connected to ui file generated from QTdesigner
# Contains the logic to make interface be able to interact with rest of code/command prompt
# Needs "TestGUIv2.ui" in same directory to work, XML type code

from PyQt5 import QtWidgets, uic
import sys

spec = 0 #global variable of number of specimens

class CustomDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Specimen Configuration")


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('TestGUIv2.ui', self) # Load the .ui file

        self.button = self.findChild(QtWidgets.QPushButton, 'save') # Find the button with the name "save"
        self.button.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!

        self.button2 = self.findChild(QtWidgets.QPushButton, 'configbutton')
        self.button2.clicked.connect(self.windowButtonPressed)

        self.config = self.findChild(QtWidgets.QLineEdit, 'config')

        self.show() # Show the GUI

    def printButtonPressed(self):
        # This is executed when the button is pressed
        print(self.config.text())

    def windowButtonPressed(self):

        dlg = CustomDialog(self)

        if dlg.exec_():
            print("Configuration Saved!")
        else:
            print("Configuration Not Saved!")


app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
window = Ui()  # Create an instance of our class
app.exec_()  # Start the application