import pyautogui as mc
import sys
import time

class action:
    def __init__(self, type):
        self.type = type  # This could be a click, keyboard stroke, etc. The numbering is determined in the sequence class
        self.clickcount = 0
        self.clickspeed = 0
        self.clickloc = [0, 0]
        self.button = 'None'
        self.value = 0
        self.string = 'None'
        self.pausewait = 0
        if type == 1:  # If the type of action is a click
            self.get_click_count()  # Get the number of clicks from the user
            self.get_click_location()  # Get the location in which to click
            self.get_click_speed()  # Get the speed in which to move the mouse to the click location
        elif type == 2:  # If the type of action is a button press
            self.get_button()
        elif type == 3:  # If the type of action is a value insert
            self.get_value()
        elif type == 4:  # If the type of action is a string insert
            self.get_string()
        elif type == 5:  # If the type of action is a pause
            self.get_pause_value()

    def get_click_count(self):
        self.clickcount = eval(input('How many clicks are specified for this action?: '))

    def get_click_speed(self):
        self.clickspeed = eval(input('How quickly do you want this click to occur (seconds)?: '))

    def get_click_location(self):  # Prompts the user to put the mouse where they want to make a click and saves that location tied to this action
        print('Move mouse to location of click (you have ' + str(5) + ' seconds)')  # Getting the x input coordinates
        for i in range(5, 0, -1):
            sys.stdout.write(str(i) + ' ')
            sys.stdout.flush()
            time.sleep(1)
        xInput = mc.position()
        self.clickloc = [xInput.x, xInput.y]
        print('\n')
        print('Screen coordinates')
        print('X:' + '{0:5d}'.format(self.clickloc[0]) + ', Y:' + '{0:5d}'.format(self.clickloc[1]) + '\n')

    def get_button(self):
        opt = eval(input('\nWhich button do you want to press?\n 1. Enter\n Option: '))
        if opt == 1:
            self.button = 'enter'

    def get_value(self):
        self.value = eval(input('\nWhich value do you want inserted?\n 1. X position\n 2. Y position\n 3. Z first\n '
                                '4. Z last\n Option: '))

    def get_string(self):
        opt = eval(input('\nWhich option do you want for your string?:\n 1. Save name\n 2. Custom\n Option:'))
        if opt == 1:
            self.string = 'saveName'
        elif opt == 2:
            self.string = input('Enter the string you want: ')

    def get_pause_value(self):
        self.pausewait = eval(input('How long would you like to pause for? '))
