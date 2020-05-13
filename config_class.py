import os
import pickle
from scipy import io
import numpy as np
from save_click_regions import collect_click_regions
from create_config import create_config
from sequence_class import sequence
from registration_class import registration

class config:
    def __init__(self, sett, create=True, load=True):
        self.sett = sett
        self.simulation = False  # Is true if the user is running a simulation
        if create and not load:  # Create option means we are creating a new configuration if true
            self.name = input('Name this configuration: ')
            try:
                self.create_directory()
            except:
                print('Directory already exists')

            # self.click_regions = collect_click_regions(5)
            # self.click_regions = {'xPos': 0}
            config_out = create_config()
            self.expConfig = config_out['expArray']
            self.initConfig = config_out['array']
            self.saveName = config_out['saveName']
            self.path = config_out['loadName']
            self.sequence = []

            self.registration = []  # Create a registration class for each specimen
            opt = eval(input('\n\n Which registration method would you like to use? \n  '
                             '1. Point matching image registration (PMIR) \n  2. Center of mass registration (CMOR) \n  '
                             '3. Trained root mean square registration (RMSR) \n  -1. Return \n  Option: '))

            if opt == 1:
                reg_method = 'PMIR'  # Point matching image registration
            elif opt == 2:
                reg_method = 'COMR'  # Center of mass registration
            elif opt == 3:
                reg_method = 'RMSR'  # Root mean square registration
            elif opt == -1:
                reg_method = 'None'  # No method has been selected
            else:
                Warning('The option you have chosen does not exist ... Using option 1')
                reg_method = 'PMIR'

            chan = eval(input('\n\n On which microscope channel would you like image registration to be performed? \n  '
                             'Option: '))

            for spm in range(int(self.expConfig[0])):
                self.registration.append(registration(reg_method, chan))  # Assign the same registration method for each specimen

            for spm in range(int(self.expConfig[0])):
                print('\nSelect a sequence for specimen ' + str(spm + 1))
                self.sequence.append(sequence(new=False, ret=True))
            # self.sequence = sequence(new=False, ret=True)

            with open('./mat/conf/' + self.name + '/configclass.pkl',
                      'wb') as f:  # Creating a pickle file that is writable
                pickle.dump(self, f)
            f.close()
            # io.savemat('./mat/conf/' + self.name + '/config.mat', {'name': self.name, 'expConfig': self.expConfig, 'initConfig': self.initConfig, 'saveName': self.saveName, 'path': self.path})
            # io.savemat('./mat/conf/' + self.name + '/click.mat', self.click_regions)
        elif create and load:
            d = os.listdir('./mat/conf/')

            count = 1
            for file in d:  # Print out the list of configurations that exist
                print(str(count) + '. ' + file)
                count = count + 1

            opt = eval(input('\n Pick a configuration: '))

            try:
                configName = d[opt-1]
            except:
                print('Error, not an option')
                return

            with open('./mat/conf/' + configName + '/configclass.pkl', 'rb') as f:  # Load the pickle file that contains a configuration object
                pickload = pickle.load(f)
            f.close()
            # confDict = io.loadmat('./mat/conf/' + configName + '/config.mat')
            # self.click_regions = io.loadmat('./mat/conf/' + configName + '/click.mat')

            self.name = pickload.name
            self.sequence = pickload.sequence
            self.expConfig = pickload.expConfig
            self.initConfig = pickload.initConfig
            self.saveName = pickload.saveName
            self.path = pickload.path
            self.registration = pickload.registration
            if 'self.registration[0].channel' not in locals(): # channel was added later. Check and replace with a 1 if it isn't there'
                self.registration = []
                for spm in range(int(self.expConfig[0])):
                    self.registration.append(registration(pickload.registration[spm].method, 1))
            self.edit_settings_menu()

            # config_out = create_config()
            # self.expConfig = config_out['expArray']
            # self.initConfig = config_out['array']
            # self.saveName = config_out['saveName']
            # self.path = config_out['loadName']
            #
            # io.savemat('./mat/conf/' + self.name + '/config.mat', {'name': self.name, 'expConfig': self.expConfig, 'initConfig': self.initConfig, 'saveName': self.saveName, 'path': self.path})
            # io.savemat('./mat/conf/' + self.name + '/click.mat', self.click_regions)
        elif load and not create:
            d = os.listdir('./mat/conf/')

            count = 1
            for file in d:
                print(str(count) + '. ' + file)
                count = count + 1

            opt = eval(input('\n Pick a configuration: '))

            try:
                configName = d[opt - 1]
            except:
                print('Error')
                return

            # confDict = io.loadmat('./mat/conf/' + configName + '/config.mat')
            # self.click_regions = io.loadmat('./mat/conf/' + configName + '/click.mat')
            #
            # self.name = str(confDict['name'][0])
            # self.expConfig = confDict['expConfig']
            # self.initConfig = confDict['initConfig']
            # self.saveName = str(confDict['saveName'][0])
            # self.path = str(confDict['path'][0])

            with open('./mat/conf/' + configName + '/configclass.pkl', 'rb') as f:
                pickload = pickle.load(f)
            f.close()
            # confDict = io.loadmat('./mat/conf/' + configName + '/config.mat')
            # self.click_regions = io.loadmat('./mat/conf/' + configName + '/click.mat')

            self.name = pickload.name
            self.sequence = pickload.sequence
            self.expConfig = pickload.expConfig
            self.initConfig = pickload.initConfig
            self.saveName = pickload.saveName
            self.path = pickload.path
            self.registration = pickload.registration
            try:  # channel was added later. Check and replace with a 1 if it isn't there'
                self.registration[0].channel
            except NameError:
                self.registration = []
                for spm in range(int(self.expConfig[0])):
                    self.registration.append(registration(pickload.registration[spm].method, 1))


    def return_convention_name(self, t, spm, name_conv):
        L = len(name_conv)  # How many parts are in the convention
        return_string = ''
        addon_string = ''
        for l in range(L):  # Go through each part and print a representation
            print_type = name_conv[l][0]
            if print_type == '{Config Name}':  # Print the name specified in the configuration object
                addon_string = self.saveName
            elif print_type == '{Time Stamp}' or print_type == '{Specimen}':  # Print the time stamp or specimen number
                if print_type == '{Time Stamp}':
                    numstring = t + 1 + name_conv[l][2]
                elif print_type == '{Specimen}':
                    numstring = spm + 1 + name_conv[l][2]
                if name_conv[l][1] == 0:
                    addon_string = str(numstring)
                elif name_conv[l][1] == 1:
                    addon_string = '%0.1d' % numstring
                elif name_conv[l][1] == 2:
                    addon_string = '%0.2d' % numstring
                elif name_conv[l][1] == 3:
                    addon_string = '%0.3d' % numstring
                elif name_conv[l][1] == 4:
                    addon_string = '%0.4d' % numstring
                elif name_conv[l][1] == 5:
                    addon_string = '%0.5d' % numstring
            elif print_type == '{String}':  # Print an arbitrary string
                addon_string = name_conv[l][1]
            return_string = return_string + addon_string
        return return_string

    # Creates a directory in the mat directory with the name given by the user
    def create_directory(self):
        os.mkdir('./mat/conf/' + self.name)

    def edit_settings_menu(self):
        loop = True
        while loop:
            opt = eval(input('\nChose an option?\n '
                             '1. Edit experimental settings\n 2. Edit specimen settings\n 3. Save settings\n 4. None\n '
                             'Option: '))
            if opt == 1:
                self.edit_experimental_settings()
            elif opt == 2:
                self.specimen_settings_menu()
            elif opt == 3:
                with open('./mat/conf/' + self.name + '/configclass.pkl', 'wb') as f:  # Creating a pickle file that is writable
                    pickle.dump(self, f)
                f.close()
            elif opt == 4:
                loop = False
            else:
                print('\nInvalid option')

    def edit_experimental_settings(self):
        loop = True
        while loop:
            print('\n Experimental settings for ' + self.name)
            print(' 1. Save Name: ' + self.saveName)
            print(' 2. Path: ' + self.path)
            print(' 3. Number of specimen: ' + str(int(self.expConfig[0])))
            print(' 4. Number of time stamps: ' + str(int(self.expConfig[4])))
            print(' 5. Image capture frequency: ' + str(self.expConfig[5]) + ' minutes')
            print(' 6. Height of image: ' + str(int(self.expConfig[1])))
            print(' 7. Width of image: ' + str(int(self.expConfig[2])))
            print(' 8. 16-bit threshold value: ' + str(int(self.expConfig[6])))
            print(' 9. Lateral resolution (XY): ' + str(self.expConfig[3]) + ' microns/pixel')
            print(' 10. Axial resolution (Z): ' + str(self.expConfig[7]) + ' microns/z-stack')
            print(' 11. Specimen Tracking Method: ' + self.registration[0].method)
            print(' 12. Microscope Channel for Tracking: ' + str(self.registration[0].channel))
            print(' -1. Return')
            opt = eval(input('Which setting would you like to edit?: '))
            if opt == -1:  # Return option
                loop = False
                continue
            if (opt == 1) or (opt == 2): # String options
                newval = input('What do you want to change this option to? ')
                if opt == 1:  # Name to save the files
                    variable = 'saveName'
                else:  # Path to save the files
                    variable = 'path'
                exec('self.' + variable + '=' + '\'' + newval + '\'')
            elif opt == 11:  # Categorical options
                optreg = eval(input('\n\n Which registration method would you like to use? \n  '
                                 '1. Point matching image registration (PMIR) \n  2. Center of mass registration (CMOR) \n  '
                                 '3. Trained root mean square registration (RMSR) \n  -1. Return \n  Option: '))  # Change the registration method
                if optreg == 1:
                    reg_method = 'PMIR'  # Point matching image registration
                elif optreg == 2:
                    reg_method = 'COMR'  # Center of mass registration
                elif optreg == 3:
                    reg_method = 'RMSR'  # Root mean square registration
                elif optreg == -1:
                    reg_method = 'None'  # No method has been selected
                else:
                    Warning('The option you have chosen does not exist ... Using option 1')
                    reg_method = 'PMIR'
                for spm in range(int(self.expConfig[0])):
                    self.registration[spm].method = reg_method
            elif opt == 12:  # Change the channel to do the image registration
                newval = input('What do you want to change this value to? ')
                for spm in range(int(self.expConfig[0])):
                    self.registration[spm].channel = newval
            else:  # Numeric options
                newval = input('What do you want to change this value to? ')
                if opt == 3:
                    variable = 'expConfig[0]'
                    self.sequence = []
                    for spm in range(int(newval)):
                        self.get_specimen_data(spm)
                        print('\nSelect a sequence for specimen ' + str(spm + 1))
                        self.sequence.append(sequence(new=False, ret=True))
                elif opt == 4:
                    variable = 'expConfig[4]'
                elif opt == 5:
                    variable = 'expConfig[5]'
                elif opt == 6:
                    variable = 'expConfig[1]'
                elif opt == 7:
                    variable = 'epxConfig[2]'
                elif opt == 8:
                    variable = 'expConfig[6]'
                elif opt == 9:
                    variable = 'expConfig[3]'
                elif opt == 10:
                    variable = 'expConfig[7]'
                else:
                    print('Invalid')
                    continue
                exec('self.' + variable + '=' + newval)

    def specimen_settings_menu(self):
        loop = True
        while loop:
            for spm in range(int(self.expConfig[0])):
                print('\n')
                self.print_specimen_settings(spm)
            print('\nWhich specimen do you want to change the settings for? ')
            print(' 1. All specimen')
            count = 2
            for spm in range(int(self.expConfig[0])):
                print(' ' + str(count) + '. Specimen ' + str(spm + 1))
                count = count + 1
            print(' -1. Return')
            opt = eval(input(' Option: '))
            if opt == -1:
                return
            self.edit_specimen_settings(opt)

    def edit_specimen_settings(self, opt):
        if opt == 1:
            for spm in range(int(self.expConfig[0])):
                self.get_specimen_data(spm)
        else:
            spm = opt - 2
            self.get_specimen_data(spm)

    def get_specimen_data(self, spm):
        print('Insert the information for specimen ' + str(spm + 1) + '\n')
        x_start = eval(input("What is the initial x coordinate? "))
        y_start = eval(input("What is the initial y coordinate? "))
        z1_start = eval(input("What is the z1 coordinate? "))
        z2_start = eval(input("What is the z2 coordinate? "))
        delta_x = eval(input("What is delta x? "))
        delta_y = eval(input("What is delta y? "))
        ang = eval(input("What is the angle? "))
        # storing the values in the config data matrix
        self.initConfig[spm][0] = spm
        self.initConfig[spm][1] = x_start
        self.initConfig[spm][2] = y_start
        self.initConfig[spm][3] = z1_start
        self.initConfig[spm][4] = z2_start
        self.initConfig[spm][5] = delta_x
        self.initConfig[spm][6] = delta_y
        self.initConfig[spm][7] = ang
        self.sequence[spm] = sequence(new=False, ret=True)

    def print_specimen_settings(self, spm):
        print('Settings for specimen: ' + str(spm + 1))
        print('Initial x coordinate: ' + str(self.initConfig[spm][1]))
        print('Initial y coordinate: ' + str(self.initConfig[spm][2]))
        print('Zfirst coordinate: ' + str(self.initConfig[spm][3]))
        print('Zlast corrdinate: ' + str(self.initConfig[spm][4]))
        print('Growth in x: ' + str(self.initConfig[spm][5]))
        print('Growth in y: ' + str(self.initConfig[spm][6]))
        print('Sequence: ' + self.sequence[spm].name)
