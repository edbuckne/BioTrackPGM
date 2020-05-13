import pickle

class settings:
    def __init__(self, create=False):
        if create:
            # Settings concerned with the simulation
            self.SIMULATION_IMAGE_ADJUST = True
            self.SIMULATION_IMAGE_PRINT = True
            self.SIMULATION_CHANNEL_PRINT = 2
            # Settings concerned with the microscope
            self.MICROSCOPE_X_ORIENTATION_POSITIVE = True
            self.MICROSCOPE_Y_ORIENTATION_POSITIVE = True
            self.MICROSCOPE_Z_ORIENTATION_POSITIVE = True
            self.MICROSCOPE_SAVE_CONFIGURATION = [['{Config Name}', '~'], ['{Time Stamp}', 2, 0]]
            self.MICROSCOPE_LOAD_CONFIGURATION = [['{Config Name}', '~'], ['{Time Stamp}', 2, 0], ['{String}', '_G'], ['{Specimen}', 0, 0]]

            self.save_settings()
        else:
            pklreturn = self.load_settings()

            self.SIMULATION_IMAGE_ADJUST = pklreturn.SIMULATION_IMAGE_ADJUST
            self.SIMULATION_IMAGE_PRINT = pklreturn.SIMULATION_IMAGE_PRINT
            # self.SIMULATION_CHANNEL_PRINT = pklreturn.SIMULATION_CHANNEL_PRINT  # Add this functionality in the future

            self.MICROSCOPE_X_ORIENTATION_POSITIVE = pklreturn.MICROSCOPE_X_ORIENTATION_POSITIVE
            self.MICROSCOPE_Y_ORIENTATION_POSITIVE = pklreturn.MICROSCOPE_Y_ORIENTATION_POSITIVE
            self.MICROSCOPE_Z_ORIENTATION_POSITIVE = pklreturn.MICROSCOPE_Z_ORIENTATION_POSITIVE
            self.MICROSCOPE_SAVE_CONFIGURATION = pklreturn.MICROSCOPE_SAVE_CONFIGURATION
            self.MICROSCOPE_LOAD_CONFIGURATION = pklreturn.MICROSCOPE_LOAD_CONFIGURATION
        return


    def print_name_convention(self, name_conv, List=False):
        if List:  # The end of our lines will be different depending on if we want a list or an inline print
            endline = '\n'
        else:
            endline = ''
        L = len(name_conv)  # How many parts are in the convention
        for l in range(L):  # Go through each part and print a representation
            if List:
                print('%d' % (l + 1), end='')
                print('. ', end='')
            print_type = name_conv[l][0]
            if print_type == '{Config Name}':  # Print the name specified in the configuration object
                print(print_type, end=endline)
            elif print_type == '{Time Stamp}':  # Print the time stamp
                print('(', end='')
                if name_conv[l][1] == 0:  # Print TIME or TTT...
                    print('TIME', end='')
                else:
                    for i in range(name_conv[l][1]):
                        print('T', end='')
                if name_conv[l][2] != 0:
                    print('+' + str(name_conv[l][2]), end='')
                print(')', end=endline)
            elif print_type == '{String}':  # Print an arbitrary string
                print(name_conv[l][1], end=endline)
            elif print_type == '{Specimen}':  # Print the specimen number
                print('(', end='')
                if name_conv[l][1] == 0:  # Print SPM or SSS...
                    print('SPM', end='')
                else:
                    for i in range(name_conv[l][1]):
                        print('S', end='')
                if name_conv[l][2] != 0:
                    print('+' + str(name_conv[l][2]), end='')
                print(')', end=endline)
        print('')
        return 'None'


    # Just prints out the options that a user can have for naming conventions
    def print_convention_options(self):
        print(' 1. {Config Name}\n 2. {Time Stamp}\n 3. {Specimen}\n 4. {String}')


    # Creates a list item that can be inserted into the convention list
    def return_a_convention_item(self, option):
        if option == 1:  # Configuration name
            return ['{Config Name}', '~']
        elif option == 2:  # Time stamp
            dig = eval(input('How many digits do you want to use for the time stamp (0 - Only necessary)? '))
            offset = eval(input('What is the offset you want to add to the time stamp? '))
            return ['{Time Stamp}', dig, offset]
        elif option == 3:  # Specimen number
            dig = eval(input('How many digits do you want to use for the specimen (0 - Only necessary)? '))
            offset = eval(input('What is the offset you want to add to the specimen? '))
            return ['{Specimen}', dig, offset]
        elif option == 4:  # String
            strins = input('What string do you want to include? ')
            return ['{String}', strins]
        else:
            return


    def edit_naming_convention(self, saveload):
        if saveload == 'Save':  # Copy the configuration we want to edit depending on the input
            name_conv = self.MICROSCOPE_SAVE_CONFIGURATION
        elif saveload == 'Load':
            name_conv = self.MICROSCOPE_LOAD_CONFIGURATION
        else:
            return
        loop = True  # Continue to loop until the user is finished making the edits
        while loop:
            print('\n\n')  # Just print a couple of newlines to space out visually
            self.print_name_convention(name_conv, List=False)
            self.print_name_convention(name_conv, List=True)
            opt = eval(input('\nChoose an option:\n 1. Append\n 2. Delete\n 3. Insert\n '
                             '4. Save and continue\n 5. Save and exit\n 6. Exit without saving\n Option: '))  # Provide the user with a bunch of different options to edit the sequence
            print('')
            if opt == 1:
                self.print_convention_options()
                convopt = eval(input('What kind of item to you want to append? '))
                appenditem = self.return_a_convention_item(convopt)
                name_conv.append(appenditem)
            elif opt == 2:
                convopt = eval(input('Which would you like to delete? '))
                name_conv.pop(convopt-1)
            elif opt == 3:
                indopt = eval(input('Which item would you like the new item to go after? '))
                self.print_convention_options()
                convopt = eval(input('Option: '))
                insertitem = self.return_a_convention_item(convopt)
                name_conv.insert(indopt, insertitem)
            elif opt == 4:
                if saveload == 'Save':  # Copy the configuration we want to save depending on the input
                    self.MICROSCOPE_SAVE_CONFIGURATION = name_conv
                elif saveload == 'Load':
                    self.MICROSCOPE_LOAD_CONFIGURATION = name_conv
                self.save_settings()
            elif opt == 5:
                if saveload == 'Save':  # Copy the configuration we want to save depending on the input
                    self.MICROSCOPE_SAVE_CONFIGURATION = name_conv
                elif saveload == 'Load':
                    self.MICROSCOPE_LOAD_CONFIGURATION = name_conv
                self.save_settings()
                loop = False
            elif opt == 6:
                loop = False


    def print_microscope_settings(self):
        x_orientation_print = 'True' if self.MICROSCOPE_X_ORIENTATION_POSITIVE else 'False'
        print('1. Positive orientation of X axis: ' + x_orientation_print)
        y_orientation_print = 'True' if self.MICROSCOPE_Y_ORIENTATION_POSITIVE else 'False'
        print('2. Positive orientation of Y axis: ' + y_orientation_print)
        z_orientation_print = 'True' if self.MICROSCOPE_Z_ORIENTATION_POSITIVE else 'False'
        print('3. Positive orientation of Z axis: ' + z_orientation_print)
        print('4. Save name: ', end='')
        self.print_name_convention(self.MICROSCOPE_SAVE_CONFIGURATION)
        print('5. Load name: ', end='')
        self.print_name_convention(self.MICROSCOPE_LOAD_CONFIGURATION)


    def print_simulation_settings(self):
        image_adjust = 'True' if self.SIMULATION_IMAGE_ADJUST else 'False'
        print('1. Shift images during simulation to simulate repositioning: ' + image_adjust)
        image_print = 'True' if self.SIMULATION_IMAGE_PRINT else 'False'
        print('2. Print images during simulation to simulate repositioning: ' + image_print)


    # This function negates the True/False setting that is chosen by the user
    def edit_microscope_settings(self):
        self.print_microscope_settings()
        opt = eval(input('\n Which setting would you like to change (-1: None)? '))
        if opt == 1:
            self.MICROSCOPE_X_ORIENTATION_POSITIVE = not self.MICROSCOPE_X_ORIENTATION_POSITIVE
        elif opt == 2:
            self.MICROSCOPE_Y_ORIENTATION_POSITIVE = not self.MICROSCOPE_Y_ORIENTATION_POSITIVE
        elif opt == 3:
            self.MICROSCOPE_Z_ORIENTATION_POSITIVE = not self.MICROSCOPE_Z_ORIENTATION_POSITIVE
        elif opt == 4:
            self.edit_naming_convention('Save')
        elif opt == 5:
            self.edit_naming_convention('Load')
        elif opt == -1:
            print('No settings were changed')
        else:
            print('Not an option, not changing anything')
        self.print_microscope_settings()


    def edit_simulation_settings(self):
        self.print_simulation_settings()
        opt = eval(input('\n Which setting would you like to change (-1: None)? '))
        if opt == 1:
            self.SIMULATION_IMAGE_ADJUST = not self.MICROSCOPE_X_ORIENTATION_POSITIVE
        elif opt == 2:
            self.SIMULATION_IMAGE_PRINT = not self.SIMULATION_IMAGE_PRINT
        elif opt == -1:
            print('No settings were changed')
        else:
            print('Not an option, not changing anything')
        self.print_simulation_settings()


    def save_settings(self):
        with open('./mat/settings/settings.pkl', 'wb') as f:  # Creating a pickle file that is writable
            pickle.dump(self, f)
        f.close()


    def load_settings(self):
        with open('./mat/settings/settings.pkl', 'rb') as f:  # Load the pickle file that contains a settings object
            pickload = pickle.load(f)
        f.close()
        return pickload


    def settings_menu(self, opt=0):
        while opt != -1:
            opt = eval(input('\n\nChoose an option\n 1. Microscope Settings\n 2. Simulation Settings\n 3. Save Settings'
                             '\n -1: Return \n\n Option: '))
            if opt == 1:
                self.edit_microscope_settings()
            elif opt == 2:
                self.edit_simulation_settings()
            elif opt == 3:
                self.save_settings()
            elif opt == -1:
                print('Exiting')
            else:
                print('Invalid option')