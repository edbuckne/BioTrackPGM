import tkinter as tk
from delegates.btp_buttons import btp_button

class StartPage:  # This class defines the layout of our start page
    def __init__(self, master):
        self.master = master  # Indicates the master of this object which should be root
        self.frame = tk.Frame(self.master, height=750, width=750)  # Creates a frame which we can use to put buttons on
        self.frame.pack_propagate(0)  # Allows the frame to decide its own height and width

        self.run_experiment_button = btp_button(self.frame, text='Run Experiment', command=self.new_run_experiment_window)  # Buttons, command is what is called when button is pressed
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
        self.app = setup_experiment_window(self.newWindow)

    def new_run_simulation_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title('Run Simulation')
        self.app = run_simulation_window(self.newWindow)

    def new_settings_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title('Settings')
        self.app = settings_window(self.newWindow)

# LEVEL 2
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
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.master.destroy)
        self.quitButton.pack()
        self.frame.pack()

class sequence_menu_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.master.destroy)
        self.quitButton.pack()
        self.frame.pack()

class run_simulation_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.master.destroy)
        self.quitButton.pack()
        self.frame.pack()

class settings_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, height=500, width=500)
        self.frame.pack_propagate(0)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.master.destroy)
        self.quitButton.pack()
        self.frame.pack()


def main():
    root = tk.Tk()
    root.title('bioTRACKpgm')
    app = StartPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()