from tkinter import *

class btp_button(Button):
    def __init__(self, master, text, command):
        Button.__init__(self, master, text=text, command=command,
                        activebackground='blue', bg = 'green', font=("Times", 18, "bold"),
                        relief=RIDGE)

