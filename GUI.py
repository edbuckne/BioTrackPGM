import tkinter as tk
from tkinter import *


class StartPage:  # This class defines the layout of our start page
    def __init__(self, master):
        self.master = master  # Indicates the master of this object which should be root
        self.frame = tk.Frame(self.master, height=750, width=750)  # Creates a frame which we can use to put buttons on
        self.frame.pack_propagate(0)  # Allows the frame to decide its own height and width

        self.run_experiment_button = tk.Button(self.frame, text='Run Experiment', command=self.new_run_experiment_window)  # Buttons, command is what is called when button is pressed
        self.run_experiment_button.place(relx=0.2, rely=0.1, relheight=0.1, relwidth=0.6)  # Position and size of buttons
        self.setup_experiment_button = tk.Button(self.frame, text='Setup Experiment', command=self.new_setup_experiment_window)
        self.setup_experiment_button.place(relx=0.2, rely=0.2, relheight=0.1, relwidth=0.6)
        self.sequence_menu_button = tk.Button(self.frame, text='Sequence Menu', command=self.new_sequence_menu_window)
        self.sequence_menu_button.place(relx=0.2, rely=0.3, relheight=0.1, relwidth=0.6)
        self.run_simulation_button = tk.Button(self.frame, text='Run Simulation', command=self.new_run_simulation_window)
        self.run_simulation_button.place(relx=0.2, rely=0.4, relheight=0.1, relwidth=0.6)
        self.settings_button = tk.Button(self.frame, text='Settings', command=self.new_settings_window)
        self.settings_button.place(relx=0.2, rely=0.5, relheight=0.1, relwidth=0.6)
        self.frame.pack()

    def new_run_experiment_window(self):  # These functions create new windows
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.lift(self.master)
        self.newWindow.title('Run Experiment Options')
        self.app = run_experiment_window(self.newWindow)

    def new_setup_experiment_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title('Setup Experiment Options')
        self.app = setup_experiment_window(self.newWindow)

    def new_sequence_menu_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title('Sequence Menu')
        self.app = sequence_menu_window(self.newWindow)

    def new_run_simulation_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title('Run Simulation')
        self.app = run_simulation_window(self.newWindow)

    def new_settings_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title('Settings')
        self.app = settings_window(self.newWindow)

class run_experiment_window:  # Definitions of the windows being called
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        self.quitButton = tk.Label(self.frame, text = 'This would cause the experiment to start')
        self.quitButton.place(rely=0.5)
        self.frame.pack()

class setup_experiment_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=750, width=750)
        self.frame.pack_propagate(0)
        #self.run_experiment_button = tk.Button(self.frame, text='Create a new sequence',command=self.master.destroy)  # Buttons, command is what is called when button is pressed
        #self.run_experiment_button.place(relx=0.2, rely=0.2, relheight=0.1,relwidth=0.6)  # Position and size of buttons
        self.load_config_button = tk.Button(self.frame, text='Load Configuration', command=self.load_config_window)
        self.load_config_button.place(relx=0.2, rely=0.2, relheight=0.1, relwidth=0.6)  # Position and size of buttons
        self.create_config_button = tk.Button(self.frame, text='Create Configuration',command=self.create_config_window)
        self.create_config_button.place(relx=0.2, rely=0.3, relheight=0.1,relwidth=0.6)  # Position and size of buttons
        self.load_config_full_button = tk.Button(self.frame, text='Load Configuration-full',command=self.load_config_full_window)
        self.load_config_full_button.place(relx=0.2, rely=0.4, relheight=0.1,relwidth=0.6)  # Position and size of buttons
        self.return_button = tk.Button(self.frame, text='Return',command=self.master.destroy)
        self.return_button.place(relx=0.2, rely=0.5, relheight=0.1,relwidth=0.6)  # Position and size of buttons
        self.frame.pack()

    def load_config_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.lift(self.master)
        self.newWindow.title('Load Configuration')
        # how to ask for user input
        # pconfig=tkSimpleDialog.askstring('Configuration', prompt['Pick a configuration'])
        self.app = load_config_window(self.newWindow)

    def create_config_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.lift(self.master)
        self.newWindow.title('Create Configuration')
        self.app = create_config_window(self.newWindow)


    def load_config_full_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.lift(self.master)
        self.newWindow.title('Load Configuration-full')
        self.app = load_config_full_window(self.newWindow)

class sequence_menu_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=750, width=750)
        self.frame.pack_propagate(0)

        self.create_sequence_button = tk.Button(self.frame, text='Create a new sequence',command=self.create_sequence_window)  # Buttons, command is what is called when button is pressed
        self.create_sequence_button.place (relx=0.2, rely=0.2, relheight=0.1, relwidth=0.6) # Position and size of buttons
        self.load_sequence_button = tk.Button(self.frame, text='Load a sequence', command=self.master.destroy)
        self.load_sequence_button.place(relx=0.2, rely=0.3, relheight=0.1, relwidth=0.6)
        self.run_sequence_button = tk.Button(self.frame, text='Run a sequence', command=self.master.destroy)
        self.run_sequence_button.place(relx=0.2, rely=0.4, relheight=0.1, relwidth=0.6)
        self.create_sequence_existing_button = tk.Button(self.frame, text='Create new sequence from existing', command=self.master.destroy)
        self.create_sequence_existing_button .place(relx=0.2, rely=0.5, relheight=0.1, relwidth=0.6)
        self.return_button = tk.Button(self.frame, text='Return', command=self.master.destroy)
        self.return_button.place(relx=0.2, rely=0.6, relheight=0.1, relwidth=0.6)
        self.frame.pack()

    def create_sequence_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.lift(self.master)
        self.newWindow.title('Create Sequence')
        self.app = create_sequence_window(self.newWindow)



class run_simulation_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        self.quitButton = tk.Button(self.frame, text='QuitA', width=25, command=self.master.destroy)
        self.quitButton.pack()
        self.frame.pack()

class settings_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        #self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.master.destroy)
        #self.quitButton.pack()
        self.micro_settings_button = tk.Button(self.frame, text='Microscope Settings', command=self.micro_settings_window)
        self.micro_settings_button.place(relx=0.2, rely=0.2, relheight=0.1, relwidth=0.6)  # Position and size of buttons
        self.sim_settings_button = tk.Button(self.frame, text='Simulation Settings',command=self.master.destroy)
        self.sim_settings_button.place(relx=0.2, rely=0.3, relheight=0.1, relwidth=0.6)  # Position and size of buttons
        self.save_settings_button = tk.Button(self.frame, text='Save Settings', command=self.master.destroy)
        self.save_settings_button.place(relx=0.2, rely=0.4, relheight=0.1,relwidth=0.6)  # Position and size of buttons
        self.return_button = tk.Button(self.frame, text='Return', command=self.master.destroy)
        self.return_button.place(relx=0.2, rely=0.5, relheight=0.1, relwidth=0.6)  # Position and size of buttons
        self.frame.pack()

    def micro_settings_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.lift(self.master)
        self.newWindow.title('Run Experiment Options')
        self.app = micro_settings_window(self.newWindow)

# Definition of the classes of new windows
class create_config_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        self.e1 = Entry(master)
        # self.seq_name=sequence_name # want to use command to save the name in the insert field
        self.e1.insert(1, "")
        # The "1" here represents where to insert the text, and can be read as "line 1". This refers to the first line;
        self.e1.pack()
        self.quitButton = tk.Button(self.frame, text='Press Enter', width=25, command=self.master.destroy)
        self.quitButton = tk.Button(self.frame, text='Enter Configuration Name', width=25, command=self.master.destroy)
        self.quitButton.pack()
        self.frame.pack()

class load_config_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        # ask for the name of the sequence and save it to a dictionary for the sequence section
        self.e1 = Entry(master)
        # self.seq_name=sequence_name # want to use command to save the name in the insert field
        self.e1.insert(1, "")
        # The "1" here represents where to insert the text, and can be read as "line 1". This refers to the first line;
        self.e1.pack()
        self.quitButton = tk.Button(self.frame, text='Chose Configuration', width=25, command=self.master.destroy)
        self.quitButton.pack()
        self.frame.pack()

class load_config_full_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        self.quitButton = tk.Button(self.frame, text='Quit- Load Config full', width=25, command=self.master.destroy)
        self.quitButton.pack()
        self.frame.pack()


class create_sequence_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        # ask for the name of the sequence and save it to a dictionary for the sequence section
        self.e1 = Entry(master)
        #self.seq_name=sequence_name # want to use command to save the name in the insert field
        self.e1.insert(1,"Chose a name for this Sequence")
        #The "1" here represents where to insert the text, and can be read as "line 1". This refers to the first line;
        self.e1.pack()
        self.quitButton = tk.Button(self.frame, text='Press Enter', width=25, command=self.master.destroy)
        self.quitButton.pack()
        self.frame.pack()

def main():
    root = tk.Tk()
    root.title('bioTRACKpgm')
    app = StartPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()