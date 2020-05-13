import os
import time
import pickle
import pyautogui as mc
from action_class import action

class sequence:
    def __init__(self, new=True, ret=False, preexisting=False):
        if new:
            self.seqlist = []  # Create a new sequence list with nothing initialized
            self.empty = True
            self.name = input('Chose a name to save this sequence: ')
            self.edit_sequence()
        elif not new:
            d = os.listdir('./mat/seq/')
            print('\nList of saved sequences:')
            count = 1
            for file in d:
                print(' ' + str(count) + '. ' + file)
                count = count + 1
            opt = eval(input('\n Pick a pre-existing sequence: '))
            pick = d[opt-1]
            with open('./mat/seq/' + pick + '/sequenceclass.pkl', 'rb') as f:
                pickload = pickle.load(f)
            f.close()
            self.seqlist = pickload.seqlist
            self.empty = pickload.empty
            if preexisting:
                self.name = input('Chose a name to save this sequence: ')
            else:
                self.name = pickload.name
            if ret:  # The ret value tells whether or not to return from loading the sequence, if False, the sequence is edited
                return
            else:
                self.edit_sequence()

    # edit_sequence gives the user options to chose from which will allow them to change the sequence that has been
    # passed into this function.
    def edit_sequence(self):
        print('\n\n Current sequence\n')

        loop = True  # Continue to loop until the user is finished making the sequence
        while loop:
            self.print_sequence()
            opt = eval(input('\nChoose an option:\n 1. Append an action\n 2. Delete an action\n '
                             '3. Swap actions\n 4. Insert an action\n 5. Edit an action\n 6. Print Current Sequence\n '
                             '7. Save sequence and continue\n 8. Save sequence and exit\n 9. Exit without saving\n '
                             'Option: '))  # Provide the user with a bunch of different options to edit the sequence
            if opt == 1:
                self.append_action()
            elif opt == 2:
                self.delete_action()
            elif opt == 4:
                self.insert_action()
            elif opt == 5:
                self.edit_action()
            elif opt == 6:
                continue
            elif opt == 7:
                if not os.path.exists('./mat/seq/' + self.name):  # Don't create the directory if this directory already exists
                    os.mkdir('./mat/seq/' + self.name)
                with open('./mat/seq/' + self.name + '/sequenceclass.pkl', 'wb') as f:  # Creating a pickle file that is writable
                    pickle.dump(self, f)
                print('Sequence ' + self.name + ' has been saved\n')
                f.close()
            elif opt == 8:
                if not os.path.exists('./mat/seq/' + self.name):  # Don't create the directory if this directory already exists
                    os.mkdir('./mat/seq/' + self.name)
                with open('./mat/seq/' + self.name + '/sequenceclass.pkl', 'wb') as f:  # Creating a pickle file that is writable
                    pickle.dump(self, f)
                print('Sequence ' + self.name + ' has been saved\n')
                f.close()
                loop = False
            elif opt == 9:
                loop = False

    def append_action(self):
        newaction = self.print_available_actions()
        if not (newaction == -1):
            self.seqlist.append(newaction)
            self.empty = False

    def delete_action(self):
        self.print_sequence()
        opt = eval(input('Which action do you want to delete from this sequence (-1 for none): '))
        if opt == -1:
            return
        else:
            self.seqlist.pop(opt - 1)
            if len(self.seqlist) == 0:
                self.empty = True

    def insert_action(self):
        self.print_sequence()
        opt = eval(input('Which action would you like the new action to go after? (-1 for none, 0 for first): '))
        print('Select the action you want inserted into the sequence: ')
        self.seqlist.insert(opt, self.print_available_actions())

    def edit_action(self):
        self.print_sequence()
        opt = eval(input('Which action would you like to edit?'))
        acttype = self.seqlist[opt - 1].type
        self.seqlist[opt - 1] = action(acttype)

    def print_available_actions(self):
        opt = eval(input('\nAvailable actions\n 1. Click\n 2. Keyboard Button\n 3. Insert Value\n 4. Insert String\n '
                          '5. Pause\n -1. Return\n Option: '))
        act = action(opt)
        return act

    def print_sequence(self):
        valuelist = ['X position', 'Y position', 'Z first', 'Z last']
        if self.empty:  # If the sequence list is empty, just print empty
            print('---Empty--- \n')
            return
        listlen = len(self.seqlist)  # Returns the number of actions in this sequence
        print('\nCurrent loaded sequence')
        for i in range(listlen):
            if self.seqlist[i].type == 1:  # Prints out the action depending on the action id at that step in the sequence
                print(str(i+1) + '. Click(' + str(self.seqlist[i].clickcount) + '), [X: ' +
                      str(self.seqlist[i].clickloc[0]) + ' Y: ' + str(self.seqlist[i].clickloc[1]) +
                      '], Speed: ' + str(self.seqlist[i].clickspeed) + ' sec')
            elif self.seqlist[i].type == 2:
                print(str(i + 1) + '. Keyboard Button(' + str(self.seqlist[i].button) + ')')
            elif self.seqlist[i].type == 3:
                print(str(i + 1) + '. Insert Value(' + valuelist[self.seqlist[i].value-1] + ')')
            elif self.seqlist[i].type == 4:
                print(str(i + 1) + '. Insert String(' + self.seqlist[i].string + ')')
            elif self.seqlist[i].type == 5:
                print(str(i + 1) + '. Pause(' + str(self.seqlist[i].pausewait) + ' sec)')

    def run_sequence(self, X=0, Y=0, Zf=0, Zl=0):
        vals = [X, Y, Zf, Zl]
        listlen = len(self.seqlist)  # Get the length of the sequence
        for i in range(listlen):  # Go through each action in the sequence
            act = self.seqlist[i]
            if act.type == 1:  # Click
                mc.moveTo(act.clickloc[0], act.clickloc[1], act.clickspeed)
                mc.click(clicks=act.clickcount)
            elif act.type == 2:  # Keyboard button
                mc.press(act.button)
            elif act.type == 3:  # Insert value
                mc.typewrite(str(vals[act.value - 1]))
            elif act.type == 4:  # Insert string
                mc.typewrite(act.string)
            elif act.type == 5:  # Pause
                time.sleep(act.pausewait)
