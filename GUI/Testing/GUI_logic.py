# Connected to ui file generated from QTdesigner
# Contains the logic to make interface be able to interact with rest of code/command prompt
# Needs "TestGUIv2.ui" in same directory to work, XML type code

from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('TestGUIv2.ui', self) # Load the .ui file

        self.button = self.findChild(QtWidgets.QPushButton, 'save') # Find the button with the name "save"
        self.button.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!

        self.config = self.findChild(QtWidgets.QLineEdit, 'config')

        self.show() # Show the GUI

    def printButtonPressed(self):
        # This is executed when the button is pressed
        print(self.config.text())

app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
window = Ui()  # Create an instance of our class
app.exec_()  # Start the application