import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyautogui as ai

gVal = 1
col = []

def window():
    
   app = QApplication(sys.argv)
   win = QWidget()
   screenSize = ai.size()
   print(screenSize)
   win.setGeometry(0,100,1920,1031)
   win.setWindowTitle("Mock Zen")
   
   def remG():
       List.takeItem(List.currentRow())
   def setG():
       global count
       count = int(groupC.text())
       for i in range(1, count+1):
           List.addItem("Group"+str(i))
   def addG():
       global gVal
       global count
       if gVal > count:
            gVal = 1
       List.addItem("Group"+str(gVal))
       gVal += 1
   def printX():
       xtext = "X:"+xline.text()
       xlab.setText(xtext)
       
   def printY():
       ytext = "Y:"+yline.text()
       ylab.setText(ytext)
       
   def printzF():
       zftext = "Zf:"+zline.text()
       zflab.setText(zftext)

   def printzL():
       zltext = "Zl:"+zline.text()
       zllab.setText(zltext)
       
   def actc():
       global col
       if config.palette().button().color() == col:
           config.setStyleSheet("background-color:gray;");
       else: 
           config.setStyleSheet("background-color:red;");
           col = config.palette().button().color()
       
   xline = QLineEdit(win)
   xline.setValidator(QDoubleValidator(-5000.00,5000.00,2))
   xline.setGeometry(100,420,70,20)
   xline.editingFinished.connect(printX)
   
   xlab = QLabel(win)
   xlab.setText("X Position:")
   xlab.move(100, 400)
   xlab.setFont(QFont("Times", 8))
   
   yline = QLineEdit(win)
   yline.setValidator(QDoubleValidator(-25000.00,25000.00,2))
   yline.setGeometry(100,460,70,20)
   yline.editingFinished.connect(printY)
   
   ylab = QLabel(win)
   ylab.setText("Y Position:")
   ylab.move(100, 440)
   ylab.setFont(QFont("Times", 8))
   
   zline = QLineEdit(win)
   zline.setValidator(QDoubleValidator(-5000.00,5000.00,2))
   zline.setGeometry(100,500,70,20)
	
   zflab = QLabel(win)
   zflab.setText("Zf Position:")
   zflab.move(50, 500)
   zflab.setFont(QFont("Times", 8)) 
   
   zllab = QLabel(win)
   zllab.setText("Zl Position:")
   zllab.move(170,500)
   zllab.setFont(QFont("Times", 8)) 
   
   groupC = QLineEdit(win)
   groupC.setGeometry(530, 650, 70, 20)
   groupC.returnPressed.connect(setG)
   
   zFirst = QPushButton("First Z", win)
   zFirst.setFont(QFont("Times", 8))
   zFirst.setGeometry(200,600,60,15)
   zFirst.clicked.connect(printzF)
   
   zLast = QPushButton("Last Z", win)
   zLast.setFont(QFont("Times", 8))
   zLast.setGeometry(200,650,60,15)
   zLast.clicked.connect(printzL)
   
   List = QListWidget(win)
   List.setGeometry(300,600,200,250)
   
   add = QPushButton("Add", win)
   add.setGeometry(310, 580,30,20)
   add.clicked.connect(addG)
   
   rem = QPushButton("Rem.", win)
   rem.setGeometry(350, 580,30,20)
   rem.clicked.connect(remG)
   
   moveto = QPushButton("Move", win)
   moveto.setGeometry(390, 580, 30, 20)
   
   config = QPushButton("Configure", win)
   config.setGeometry(130, 180, 70, 70)
   config.clicked.connect(actc)    
   
   win.showMaximized()
	
   sys.exit(app.exec_())

if __name__ == '__main__':
   window()
   