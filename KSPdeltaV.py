'''
KSP Delta V calculator. This program takes a log of the planets in
Kerbal Space Program and calculates potental flight paths and their
required Delta V based on Kerbal Space Program Delta V Map version 1.3.0
While originally implimented as a text program, this now provides the
buisness code to the KSPdeltaV_GUI program.
'''

class Body (object):
    '''
    Body object is basis of Planet and Satellite objects
    Not intended to be an implemented class
    '''

    def __init__(self, 
                 name, 
                 has_atmosphere, 
                 dV_land_to_orbit, 
                 dV_orbit_to_elliptic):

        self.object_name = str(name)
        self.atmosphere = bool(has_atmosphere)
        self.land_to_orbit = int(dV_land_to_orbit)
        self.orbit_to_elliptic = int(dV_orbit_to_elliptic)

    def get_object_name(self):

        return self.object_name

    def get_atmosphere(self):

        return self.atmosphere

    def get_land_to_orbit(self):

        return self.land_to_orbit

    def get_orbit_to_elliptic(self):

        return self.orbit_to_elliptic

    def calc_start_ellip(self, orbiting):

        if orbiting:

            start_ellip = self.get_orbit_to_elliptic()

        else:

            start_ellip = (self.get_land_to_orbit()
                         + self.get_orbit_to_elliptic()
                          )

        return start_ellip

    def calc_start_exit(self, orbiting):
        #If not overriden by subclass, returns distance to elliptic.

        start_exit = self.calc_start_ellip(orbiting)

        return start_exit

class Planet (Body):
    '''
    Planet object, holds values and a calculations concerning the distance
    from itself to the edge of the gravitational influence of Kerbin.
    Has an atmosphere value but currently does nothing.
    '''

    def __init__(self, 
                 name, 
                 has_atmosphere, 
                 dV_land_to_orbit, 
                 dV_orbit_to_elliptic,
                 dV_elliptical_to_escape):

        Body.__init__(self, name, has_atmosphere, dV_land_to_orbit, dV_orbit_to_elliptic)
        self.elliptic_to_escape = int(dV_elliptical_to_escape)

    def get_elliptic_to_escape(self):

        return self.elliptic_to_escape

    def calc_start_exit(self, orbiting):

        start_exit = super(Planet, self).calc_start_exit(orbiting)

        start_exit += self.get_elliptic_to_escape()

        return start_exit

class Satellite (Body):
    '''
    Satellite object, holds values and a calculations concerning the distance
    from itself to the edge of the gravitational influence of Kerbin. With
    added values and overrided methods to account for the required path through
    it's parent planet. Has an atmosphere value but currently does nothing.
    '''
    def __init__(self, 
                 name, 
                 has_atmosphere, 
                 dV_land_to_orbit,
                 dV_orbit_to_elliptic,
                 dV_elliptic_to_parent,
                 parent_planet):

        Body.__init__(self, name, has_atmosphere, dV_land_to_orbit, dV_orbit_to_elliptic)
        self.elliptic_to_parent = int(dV_elliptic_to_parent)

        if isinstance(parent_planet, Planet):

            self.parent = parent_planet

        else:

            raise Exception('parent_planet is not of type Planet.')

    def get_elliptic_to_parent(self):

        return self.elliptic_to_parent

    def get_parent(self):

        return self.parent

    def calc_start_ellip(self, orbiting):

        start_ellip = super(Satellite, self).calc_start_ellip(orbiting)

        start_ellip += self.get_elliptic_to_parent()
        
        return start_ellip        

    def calc_start_exit(self, orbiting):

        start_exit = super(Satellite, self).calc_start_exit(orbiting)

        self_parent = self.get_parent()

        parent_escape = self_parent.get_elliptic_to_escape()

        start_exit += parent_escape

        return start_exit

class Flight_Path (object):
    '''
    Flight_Path object, takes in two body objects as well as two bools
    that determine if the intent is to orbit the repective body.
    Calculates total distance between the two bodies, taking into
    account potential parents as well as land to orbit of the same body.
    '''

    def __init__(self, body_1, body_2, is_orbiting_1, is_orbiting_2):

        if isinstance(body_1, Body):

            self.body_start = body_1

        else:

            raise Exception('body_1 is not of type Body.')

        if isinstance(body_2, Body):

            self.body_end = body_2

        else:

            raise Exception('body_2 is not of type Body.')

        self.is_orbiting_start = is_orbiting_1
        self.is_orbiting_end = is_orbiting_2
    
    def get_body_start(self):

        return self.body_start

    def get_body_end(self):

        return self.body_end

    def get_is_orbiting_start(self):

        return self.is_orbiting_start

    def get_is_orbiting_end(self):

        return self.is_orbiting_end

    def calc_ellip_distance(self):

        travel_distance = (self.get_body_start().calc_start_ellip(self.get_is_orbiting_start()) 
                         + self.get_body_end().calc_start_ellip(self.get_is_orbiting_end()))

        return travel_distance

    def calc_exit_distance(self):

        travel_distance = (self.get_body_start().calc_start_exit(self.get_is_orbiting_start()) 
                         + self.get_body_end().calc_start_exit(self.get_is_orbiting_end()))

        return travel_distance

    def calc_flight_path(self):

        planet_start = self.get_body_start()
        planet_end = self.get_body_end()
        
        if planet_start == planet_end:

            if self.get_is_orbiting_start():

                if not self.get_is_orbiting_end():

                    return planet_start.get_land_to_orbit()

            if self.get_is_orbiting_end():

                if not self.get_is_orbiting_start():

                    return planet_start.get_land_to_orbit()

            return 0

        else:

            if isinstance(planet_start, Satellite):

                if isinstance(planet_end, Satellite):

                    if planet_start.get_parent() == planet_end.get_parent():

                        return self.calc_ellip_distance()
                        
                if planet_start.get_parent() == planet_end:

                    return self.calc_ellip_distance()

            if isinstance(planet_end, Satellite):

                if planet_end.get_parent() == planet_start:

                    return self.calc_ellip_distance()

            return self.calc_exit_distance()

def initalize_solar_system():
    ''' 
    Values pulled from Kerbal Space Program Delta V Map, version 1.3.0
    Aggregated certain values that if used, would always be used together.
    '''
    
    kerbin = Planet('Kerbin', True, 3400, 0, 950)
    mun = Satellite('Mun', False, 580, 310, 860, kerbin)
    minmus = Satellite('Minmus', False, 180, 160, 930, kerbin)
    kerbol = Planet('Kerbol', False, 67000, 13700, 6000)
    eeloo = Planet('Eeloo', False, 620, 1370, 1140)
    moho = Planet('Moho', False, 870, 2410, 760)
    eve = Planet('Eve', False, 8000, 1330, 170)
    gilly = Satellite('Gilly', False, 30, 410, 60, eve)
    duna = Planet('Duna', False, 1450, 360, 380)
    ike = Satellite('Ike', False, 390, 180, 30, duna)
    dres = Planet('Dres', False, 430, 1290, 610)
    jool = Planet('Jool', False, 14000, 2810, 1140)
    pol = Satellite('Pol', False, 130, 820, 160, jool)
    bop = Satellite('Bop', False, 230, 900, 220, jool)
    tylo = Satellite('Tylo', False, 2270, 1100, 400, jool)
    vall = Satellite('Vall', False, 860, 910, 620, jool)
    laythe = Satellite('Laythe', True, 2900, 1070, 930, jool)

    solar_system = [kerbin, mun, minmus,
                    kerbol,
                    eeloo,
                    moho,
                    eve, gilly,
                    duna, ike,
                    dres,
                    jool, pol, bop, tylo, vall, laythe
                    ]

    return solar_system

if __name__ == '__main__':

    pass