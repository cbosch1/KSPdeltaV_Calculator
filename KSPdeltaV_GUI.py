import tkinter as tK
import KSPdeltaV as KSPlogic

class Flight_Plotter(tK.Frame):
    '''
    Builds a tKinter GUI based on body objects within list solar_system
    '''

    def __init__(self, solar_system, parent, *args, **kwargs):
        tK.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.solar_system = solar_system
        self.start_planet_button_values = tK.IntVar()
        self.end_planet_button_values = tK.IntVar()
        self.start_planet = self.solar_system[0]
        self.end_planet = self.solar_system[0]
        self.start_orbit = False
        self.end_orbit = False
        self.init_gui()

    def on_quit(self):

        quit()

    def set_start_planet(self):

        self.start_planet = self.solar_system[self.start_planet_button_values.get()]

    def set_end_planet(self):

        self.end_planet = self.solar_system[self.end_planet_button_values.get()]

    def toggle_start_orbit(self):

        if self.start_orbit:

            self.start_orbit = False

        else:

            self.start_orbit = True

    def toggle_end_orbit(self):

        if self.end_orbit:

            self.end_orbit = False

        else:

            self.end_orbit = True

    def set_gui_radiobuttons(self, column, variable, starting_planets):

        if starting_planets:

            calculate = self.set_start_planet

        else:

            calculate = self.set_end_planet

        self.radiobuttons = {}

        i = 0

        while i < len(self.solar_system):

            self.radiobuttons[i] = tK.Radiobutton(self, 
                                                  text=self.solar_system[i].get_object_name(), 
                                                  indicatoron=False, 
                                                  variable=variable,
                                                  value=i,
                                                  command=calculate                                                            )
            self.radiobuttons[i].grid(column=column, row=i)
            i += 1

    def init_gui(self):

        self.root.title('KSP Delta V Planner')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='nsew')

        self.set_gui_radiobuttons(1, self.start_planet_button_values, True)
        self.set_gui_radiobuttons(3, self.end_planet_button_values, False)

        tK.Label(self, text='Starting Planet:').grid(column=0, row=0, sticky='w')
        tK.Checkbutton(self, text='Orbiting?', command=self.toggle_start_orbit).grid(column=0, row=1, sticky='w')      

        tK.Label(self, text='Ending Planet:').grid(column=2, row=0, sticky='w')
        tK.Checkbutton(self, text='Orbiting?', command=self.toggle_end_orbit).grid(column=2, row=1, sticky='w')    

        tK.Button(self, text='Calculate', command=self.calculate_path).grid(column=5, row=5, sticky='e')
        tK.Label(self, text='Aproximation of Delta V:').grid(column=5, row=6, sticky='e')
        tK.Label(self, text='           ').grid(column=5, row=7, sticky='e')

        for child in self.winfo_children():

            child.grid_configure(padx=5, pady=5)

    def calculate_path(self):

        path = KSPlogic.Flight_Path(self.start_planet, self.end_planet, self.start_orbit, self.end_orbit)
        distance = path.calc_flight_path()

        tK.Label(self, text='           ').grid(column=5, row=7, sticky='e')
        tK.Label(self, text=str(distance)).grid(column=5, row=7, sticky='e')

if __name__ == '__main__':

    solar_system = KSPlogic.initalize_solar_system()
    root = tK.Tk()
    Flight_Plotter(solar_system, root)

    root.mainloop()
    if root:
        root.quit()