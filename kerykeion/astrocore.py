"""
    This is part of Kerykeion (C) 2020 Giacomo Battaglia
"""

import jsonpickle
import os.path
import swisseph as swe
from kerykeion.geoname import search
import pytz
import datetime
import math


class AstroData():
    """ 
    Colects all data from users and calculates the coordinates,
    it's utc and julian day.
    Args: name, year, month, day, hours, minuts, city,
    initial of the nation (Ex: "IT"),
    longitude, latitude and the timezone string are set to false so they will
    be calulated, if you want you can set them.
    Default values are set for now at greenwich time.
    """

    def __init__(
        self,
        name,
        year,
        month,
        day,
        hours,
        minuts,
        city,
        lon=False,
        lat=False,
        tz_str=False
    ):

        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.hours = hours
        self.minuts = minuts
        self.city = city
        self.city_long = lon
        self.city_lat = lat
        self.city_tz = tz_str
        self.json_dir = os.path.expanduser("~")

    def get_tz(self):
        return ""

    def get_utc(self):
        """Converts local time to utc time. """
        local_time = pytz.timezone(self.get_tz())

        naive_datetime = datetime.datetime(self.year, self.month,
                                           self.day, self.hours, self.minuts, 0)
        local_datetime = local_time.localize(naive_datetime, is_dst=None)
        utc_datetime = local_datetime.astimezone(pytz.utc)
        self.utc = utc_datetime
        return self.utc

    def get_jd(self):
        """ Calculates julian day from the utc time."""
        utc = self.get_utc()
        self.time_utc = utc.hour + utc.minute/60
        self.time = self.hours + self.minuts/60
        self.j_day = float(swe.julday(utc.year, utc.month, utc.day,
                                      self.time_utc))

        return self.j_day


class Calculator(AstroData):
    """
    Calculates all the astrological informations.
    Args: name, year, month, day, hours, minuts, city,
    initial of the nation (Ex: "IT"),
    longitude, latitude and the timezone string are set to false so they will
    be calulated, if you want you can set them.
    Default values are set for now at greenwich time.

    """
    now = datetime.datetime.now()

    def __init__(
        self,
        name="Now",
        year=now.year,
        month=now.month,
        day=now.day,
        hours=now.hour,
        minuts=now.minute,
        city="Greenwich",
        lon=False,
        lat=False,
        tz_str=False
    ):
        super().__init__(name, year, month, day, hours, minuts, city, lon, lat, tz_str)
        self.j_day = self.get_jd()
        self.zodiactype = "Tropic"

    def __str__(self):
        return f"Astrological data for: {self.name}, {self.utc} UTC"

    def get_number(self, name):
        """Internal function, gets number id from the name."""
        name = name.lower()

        if name == "sun":
            return 0
        elif name == "moon":
            return 1
        elif name == "mercury":
            return 2
        elif name == "venus":
            return 3
        elif name == "mars":
            return 4
        elif name == "jupiter":
            return 5
        elif name == "saturn":
            return 6
        elif name == "uranus":
            return 7
        elif name == "neptune":
            return 8
        elif name == "pluto":
            return 9
        elif name == "mean_node":
            return 10  # change!
        elif name == "true_node":
            return 11
        else:
            return int(name)

    def pos_calc(self, degree, number_name, label):
        """A function to be used in others to create a dictionary deviding 
        the houses or the planets list."""
        if degree < 30:
            hou_dic = {label: number_name, "quality": "Cardinal", "element":
                       "Fire", "sign": "Ari", "sign_num": 0, "pos": degree, "abs_pos": degree,
                       "emoji": "♈️"}
        elif degree < 60:
            result = degree - 30
            hou_dic = {label: number_name, "quality": "Fixed", "element":
                       "Earth", "sign": "Tau", "sign_num": 1, "pos": result, "abs_pos": degree,
                       "emoji": "♉️"}
        elif degree < 90:
            result = degree - 60
            hou_dic = {label: number_name, "quality": "Mutable", "element":
                       "Air", "sign": "Gem", "sign_num": 2, "pos": result, "abs_pos": degree,
                       "emoji": "♊️"}
        elif degree < 120:
            result = degree - 90
            hou_dic = {label: number_name, "quality": "Cardinal", "element":
                       "Water", "sign": "Can", "sign_num": 3, "pos": result, "abs_pos": degree,
                       "emoji": "♋️"}
        elif degree < 150:
            result = degree - 120
            hou_dic = {label: number_name, "quality": "Fixed", "element":
                       "Fire", "sign": "Leo", "sign_num": 4, "pos": result, "abs_pos": degree,
                       "emoji": "♌️"}
        elif degree < 180:
            result = degree - 150
            hou_dic = {label: number_name, "quality": "Mutable", "element":
                       "Earth", "sign": "Vir", "sign_num": 5, "pos": result, "abs_pos": degree,
                       "emoji": "♍️"}
        elif degree < 210:
            result = degree - 180
            hou_dic = {label: number_name, "quality": "Cardinal", "element":
                       "Air", "sign": "Lib", "sign_num": 6, "pos": result, "abs_pos": degree,
                       "emoji": "♎️"}
        elif degree < 240:
            result = degree - 210
            hou_dic = {label: number_name, "quality": "Fixed", "element":
                       "Water", "sign": "Sco", "sign_num": 7, "pos": result, "abs_pos": degree,
                       "emoji": "♏️"}
        elif degree < 270:
            result = degree - 240
            hou_dic = {label: number_name, "quality": "Mutable", "element":
                       "Fire", "sign": "Sag", "sign_num": 8, "pos": result, "abs_pos": degree,
                       "emoji": "♐️"}
        elif degree < 300:
            result = degree - 270
            hou_dic = {label: number_name, "quality": "Cardinal", "element":
                       "Earth", "sign": "Cap", "sign_num": 9, "pos": result, "abs_pos": degree,
                       "emoji": "♑️"}
        elif degree < 330:
            result = degree - 300
            hou_dic = {label: number_name, "quality": "Fixed", "element":
                       "Air", "sign": "Aqu", "sign_num": 10, "pos": result, "abs_pos": degree,
                       "emoji": "♒️"}
        elif degree < 360:
            result = degree - 330
            hou_dic = {label: number_name, "quality": "Mutable", "element":
                       "Water", "sign": "Pis", "sign_num": 11, "pos": result, "abs_pos": degree,
                       "emoji": "♓️"}
        else:
            hou_dic = {label: "pos_calc error", "sign": "pos_calc error",
                       "pos": "pos_calc error"}

        return hou_dic

    def houses(self):
        """Calculatetype positions and store them in dictionaries"""

        # creates the list of the house in 360°
        self.houses_degree_ut = swe.houses(self.j_day, self.city_lat,
                                           self.city_long)[0]
        # stores the house in signulare dictionaries.
        self.first_house = self.pos_calc(self.houses_degree_ut[0], "1", "name")
        self.second_house = self.pos_calc(
            self.houses_degree_ut[1], "2", "name")
        self.third_house = self.pos_calc(self.houses_degree_ut[2], "3", "name")
        self.fourth_house = self.pos_calc(
            self.houses_degree_ut[3], "4", "name")
        self.fifth_house = self.pos_calc(self.houses_degree_ut[4], "5", "name")
        self.sixth_house = self.pos_calc(self.houses_degree_ut[5], "6", "name")
        self.seventh_house = self.pos_calc(
            self.houses_degree_ut[6], "7", "name")
        self.eighth_house = self.pos_calc(
            self.houses_degree_ut[7], "8", "name")
        self.ninth_house = self.pos_calc(self.houses_degree_ut[8], "9", "name")
        self.tenth_house = self.pos_calc(
            self.houses_degree_ut[9], "10", "name")
        self.eleventh_house = self.pos_calc(
            self.houses_degree_ut[10], "11", "name")
        self.twelfth_house = self.pos_calc(
            self.houses_degree_ut[11], "12", "name")
        # creates a list of all the dictionaries of thetype.
        self.house_list = [self.first_house, self.second_house, self.third_house,
                           self.fourth_house, self.fifth_house, self.sixth_house, self.seventh_house,
                           self.eighth_house, self.ninth_house, self.tenth_house, self.eleventh_house,
                           self.twelfth_house]

        self.houses_degree = [self.house_list[0]["pos"], self.house_list[1]["pos"],
                              self.house_list[2]["pos"], self.house_list[3]["pos"], self.house_list[4]["pos"],
                              self.house_list[5]["pos"], self.house_list[6]["pos"], self.house_list[7]["pos"],
                              self.house_list[8]["pos"], self.house_list[9]["pos"], self.house_list[10]["pos"],
                              self.house_list[11]["pos"]]

        return self.house_list

    def planets_lister(self):
        """Sidereal or tropic mode."""
        self.iflag = swe.FLG_SWIEPH+swe.FLG_SPEED

        if self.zodiactype == "sidereal":
            self.iflag += swe.FLG_SIDEREAL
            mode = "SIDM_FAGAN_BRADLEY"
            swe.set_sid_mode(getattr(swe, mode))

        """Calculates the position of the planets and stores it in a list."""

        self.sun_deg = swe.calc(self.j_day, 0, self.iflag)[0][0]
        self.moon_deg = swe.calc(self.j_day, 1, self.iflag)[0][0]
        self.mercury_deg = swe.calc(self.j_day, 2, self.iflag)[0][0]
        self.venus_deg = swe.calc(self.j_day, 3, self.iflag)[0][0]
        self.mars_deg = swe.calc(self.j_day, 4, self.iflag)[0][0]
        self.jupiter_deg = swe.calc(self.j_day, 5, self.iflag)[0][0]
        self.saturn_deg = swe.calc(self.j_day, 6, self.iflag)[0][0]
        self.uranus_deg = swe.calc(self.j_day, 7, self.iflag)[0][0]
        self.neptune_deg = swe.calc(self.j_day, 8, self.iflag)[0][0]
        self.pluto_deg = swe.calc(self.j_day, 9, self.iflag)[0][0]
        self.mean_node_deg = swe.calc(self.j_day, 10, self.iflag)[0][0]
        self.true_node_deg = swe.calc(self.j_day, 11, self.iflag)[0][0]

        #print(swe.calc(self.j_day, 7, self.iflag)[3])

        self.planets_degs = [self.sun_deg, self.moon_deg, self.mercury_deg,
                             self.venus_deg, self.mars_deg, self.jupiter_deg, self.saturn_deg,
                             self.uranus_deg, self.neptune_deg, self.pluto_deg, self.mean_node_deg,
                             self.true_node_deg]

        return self.planets_degs

    def planets(self):
        """ Defines body positon in signs and informations and
         stores them in dictionaries"""
        self.planets_degs = self.planets_lister()
        # stores the planets in signulare dictionaries.
        self.sun = self.pos_calc(self.planets_degs[0], "Sun", "name")
        self.moon = self.pos_calc(self.planets_degs[1], "Moon", "name")
        self.mercury = self.pos_calc(self.planets_degs[2], "Mercury", "name")
        self.venus = self.pos_calc(self.planets_degs[3], "Venus", "name")
        self.mars = self.pos_calc(self.planets_degs[4], "Mars", "name")
        self.jupiter = self.pos_calc(self.planets_degs[5], "Jupiter", "name")
        self.saturn = self.pos_calc(self.planets_degs[6], "Saturn", "name")
        self.uranus = self.pos_calc(self.planets_degs[7], "Uranus", "name")
        self.neptune = self.pos_calc(self.planets_degs[8], "Neptune", "name")
        self.pluto = self.pos_calc(self.planets_degs[9], "Pluto", "name")
        self.mean_node = self.pos_calc(
            self.planets_degs[10], "Mean_Node", "name")
        self.true_node = self.pos_calc(
            self.planets_degs[11], "True_Node", "name")

        self.planets_list = [self.sun, self.moon, self.mercury, self.venus,
                             self.mars, self.jupiter, self.saturn, self.uranus, self.neptune,
                             self.pluto, self.mean_node, self.true_node]

        return self.planets_list

    def planets_house(self):
        """Calculates the house of the planet and updates 
        the planets dictionary."""
        self.planets()
        self.houses()

        def for_every_planet(planet, deg_planet):
            """Functio to do the calculation.
            Args: planet dictionary, planet degree"""

            def point_between(p1, p2, p3):
                """Finds if a point is between two other in a circle
                args: first point, second point, point in the middle"""
                p1_p2 = math.fmod(p2 - p1 + 360, 360)
                p1_p3 = math.fmod(p3 - p1 + 360, 360)
                if (p1_p2 <= 180) != (p1_p3 > p1_p2):
                    return True
                else:
                    return False

            if point_between(self.houses_degree_ut[0], self.houses_degree_ut[1],
                             deg_planet) == True:
                planet["house"] = "1st House"
            elif point_between(self.houses_degree_ut[1], self.houses_degree_ut[2],
                               deg_planet) == True:
                planet["house"] = "2nd House"
            elif point_between(self.houses_degree_ut[2], self.houses_degree_ut[3],
                               deg_planet) == True:
                planet["house"] = "3rd House"
            elif point_between(self.houses_degree_ut[3], self.houses_degree_ut[4],
                               deg_planet) == True:
                planet["house"] = "4th House"
            elif point_between(self.houses_degree_ut[4], self.houses_degree_ut[5],
                               deg_planet) == True:
                planet["house"] = "5th House"
            elif point_between(self.houses_degree_ut[5], self.houses_degree_ut[6],
                               deg_planet) == True:
                planet["house"] = "6th House"
            elif point_between(self.houses_degree_ut[6], self.houses_degree_ut[7],
                               deg_planet) == True:
                planet["house"] = "7th House"
            elif point_between(self.houses_degree_ut[7], self.houses_degree_ut[8],
                               deg_planet) == True:
                planet["house"] = "8th House"
            elif point_between(self.houses_degree_ut[8], self.houses_degree_ut[9],
                               deg_planet) == True:
                planet["house"] = "9th House"
            elif point_between(self.houses_degree_ut[9], self.houses_degree_ut[10],
                               deg_planet) == True:
                planet["house"] = "10th House"
            elif point_between(self.houses_degree_ut[10], self.houses_degree_ut[11],
                               deg_planet) == True:
                planet["house"] = "11th House"
            elif point_between(self.houses_degree_ut[11], self.houses_degree_ut[0],
                               deg_planet) == True:
                planet["house"] = "12th House"
            else:
                planet["house"] = "error!"

            return planet

        self.sun = for_every_planet(self.sun, self.sun_deg)
        self.moon = for_every_planet(self.moon, self.moon_deg)
        self.mercury = for_every_planet(self.mercury, self.mercury_deg)
        self.venus = for_every_planet(self.venus, self.venus_deg)
        self.mars = for_every_planet(self.mars, self.mars_deg)
        self.jupiter = for_every_planet(self.jupiter, self.jupiter_deg)
        self.saturn = for_every_planet(self.saturn, self.saturn_deg)
        self.uranus = for_every_planet(self.uranus, self.uranus_deg)
        self.neptune = for_every_planet(self.neptune, self.neptune_deg)
        self.pluto = for_every_planet(self.pluto, self.pluto_deg)
        self.mean_node = for_every_planet(self.mean_node, self.mean_node_deg)
        self.true_node = for_every_planet(self.true_node, self.true_node_deg)

        self.planets_list = [self.sun, self.moon, self.mercury, self.venus,
                             self.mars, self.jupiter, self.saturn, self.uranus, self.neptune,
                             self.pluto, self.mean_node, self.true_node]

        return self.planets_list

    def retrograde(self):
        """ Verify if a planet is retrograde. """

        self.planets_house()
        planets_ret = []
        for plan in self.planets_list:
            planet_number = self.get_number(plan["name"])
            if swe.calc(self.j_day, planet_number, self.iflag)[0][3] < 0:
                plan.update({'retrograde': True})
            else:
                plan.update({'retrograde': False})
            planets_ret.append(plan)

        self.planets_list = planets_ret

    def lunar_phase_calc(self):
        """ Function to calculate the lunar phase"""

        # anti-clockwise degrees between sun and moon
        moon, sun = self.planets_degs[1], self.planets_degs[0]
        degrees_between = moon - sun

        if degrees_between < 0:
            degrees_between += 360.0

        step = 360.0 / 28.0

        for x in range(28):
            low = x * step
            high = (x + 1) * step
            if degrees_between >= low and degrees_between < high:
                mphase = x + 1

        sunstep = [0, 30, 40,  50, 60, 70, 80, 90, 120, 130, 140, 150, 160, 170, 180,
                   210, 220, 230, 240, 250, 260, 270, 300, 310, 320, 330, 340, 350]

        for x in range(len(sunstep)):

            low = sunstep[x]

            if x == 27:
                high = 360
            else:
                high = sunstep[x+1]
            if degrees_between >= low and degrees_between < high:
                sphase = x + 1

        def moon_emoji(phase):
            if phase == 1:
                result = "🌑"
            elif phase == 14:
                result = "🌕"
            elif 7 <= phase <= 9:
                result = "🌓"
            elif 20 <= phase <= 22:
                result = "🌗"
            elif phase < 7:
                result = "🌒"
            elif phase < 14:
                result = "🌔"
            elif phase <= 28:
                result = "🌘"
            else:
                result = phase

            return result

        self.lunar_phase = {
            "degrees_between_s_m": degrees_between,
            "moon_phase": mphase,
            "sun_phase": sphase,
            "moon_emoji": moon_emoji(mphase)
        }

    def get_all(self):
        """ Gets all data from all the functions """

        self.planets_house()
        self.retrograde()
        self.lunar_phase_calc()

    def json_dump(self, dump=True):
        """
        Dumps the Kerykeion object to a json file located in the home folder.
        """

        try:
            self.sun
        except:
            self.get_all()

        self.json_path = os.path.join(
            self.json_dir, f"{self.name}_kerykeion.json")
        json_string = jsonpickle.encode(self)

        hiden_values = [
            f' "json_dir": "{self.json_dir}",', f', "json_path": "{self.json_path}"']

        for string in hiden_values:
            json_string = json_string.replace(string, "")

        if dump:
            with open(self.json_path, "w") as file:
                file.write(json_string)
                print("JSON file dumped.")
        else:
            pass
        return json_string


class CalculatorPosition(Calculator):
    def __init__(self,
                 name,
                 year,
                 month,
                 day,
                 hours,
                 minuts,
                 lon,
                 lat,
                 tz_str):
        super().__init__(name, year, month, day, hours, minuts, "", lon, lat, tz_str)

    def get_tz(self):
        return self.city_tz


class CalculatorCitySearch(Calculator):
    def __init__(self,
                 name,
                 year,
                 month,
                 day,
                 hours,
                 minuts,
                 city="Greenwich"):
        super().__init__(name, year, month, day, hours, minuts, city)

    def get_tz(self):
        """Gets the nerest time zone for the calculation"""

        self.city_data = search(self.city, self.nation)[0]

        self.city_long = float(self.city_data["lng"])
        self.city_lat = float(self.city_data["lat"])
        self.city_tz = self.city_data["timezonestr"]

        if self.city_lat > 66.0:
            self.city_lat = 66.0
            print("polar circle override for houses, using 66 degrees")

        elif self.city_lat < -66.0:
            self.city_lat = -66.0
            print("polar circle override for houses, using -66 degrees")

        return self.city_tz


if __name__ == "__main__":
    kanye = Calculator("Kanye", 1977, 6, 8, 8, 45, "Atlanta",
                       lon=50, lat=50, tz_str="Europe/Rome")
    kanye = Calculator("Kanye", 1977, 6, 8, 8, 45, "Atlanta")
    kanye.get_all()
    print(kanye.city_tz)
    print(kanye.fifth_house["pos"])
    print(Calculator().city)
    print(Calculator())

    #############################

    # f = kanye.json_dump(dump=True)
    # print(kanye.city)
    # print(f)
    # print(kanye.lunar_phase)
    # kanye.json_dump()

    # for p in kanye.planets_list:
    #     print(p)
