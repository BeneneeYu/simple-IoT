# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the definition of supported messages
#

# import the needed packages
import sys
import time
from enum import Enum  # for enumerated types

# @TODO import whatever more packages are needed
from typing import List
from typing import Dict
from typing import Tuple
from typing import Any
from enum import Enum  # for enumerated types
from dataclasses import dataclass

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert(0, "../")


############################################
#  Enumeration for Message Types
############################################
class MessageTypes(Enum):
    # One can extend this as needed. For now only these two
    UNKNOWN = -1
    GROCERY = 1
    HEALTH = 2
    RESPONSE = 3


@dataclass
class Message:
    """ Our message in native representation"""
    message_type: str
    data: Any

    def __init__(self):
        pass

    def __str__(self):
        '''Pretty print the contents of the message'''
        res = ("Dumping contents of {} Message".format(self.message_type))
        res += self.data.__str__()
        return res

    def dump(self):
        print(self.__str__())


class BreadType(Enum):
    whole_wheat = 1
    half_wheat = 2
    rye = 3
    brioche = 4
    focaccia = 5


class MeatType(Enum):
    pork = 1
    chicken = 2
    beef = 3
    shrimp = 4
    lamb = 5


class MilkType(Enum):
    one_pct = 1
    oat = 2
    whole = 3
    fat_free = 4
    cashew = 5


class VeggiesType(Enum):
    tomato = 1
    potato = 2
    broccoli = 3
    carrot = 4
    spinach = 5


############################################
#  Grocery Order Message
############################################
@dataclass
class GroceryOrderMessage:
    '''Grocery Order Message in native representation'''
    ts: float
    veggies: Dict[str, float]
    drinks: Dict[str, Dict[str, int]]
    milk: List[Tuple[str, float]]
    bread: List[Tuple[str, float]]
    meat: List[Tuple[str, float]]

    def __init__(self):
        self.milk = []
        self.bread = []
        self.meat = []
        self.veggies = {}
        self.drinks = {}
        self.ts = time.time()

    def add_veggies(self, index, quantity):
        self.veggies[VeggiesType(index).name] = quantity

    def add_milk(self, index, quantity):
        self.milk.append((MilkType(index).name, quantity))

    def add_bread(self, index, quantity):
        self.bread.append((BreadType(index).name, quantity))

    def add_meat(self, index, quantity):
        self.meat.append((MeatType(index).name, quantity))

    def to_string(self):
        res = ""
        res += ("type: {}".format("ORDER") + "\n")
        res += ("contents:" + "\n")
        veggiesStr = ""
        for key, value in self.veggies.items():
            veggiesStr += ("\n\t" + key + ": " + str(value))
        res += ("  veggies: {}".format(veggiesStr) + "\n")
        drinksStr = ""
        for package, dict in self.drinks.items():
            drinksStr += ("\n\t" + package + ": ")
            for key, value in dict.items():
                drinksStr += ("\n\t\t" + key + ": " + str(value))
        res += ("  drinks: {}".format(drinksStr) + "\n")
        res += ("  milk: {}".format(self.milk) + "\n")
        res += ("  bread: {}".format(self.bread) + "\n")
        res += ("  meat: {}".format((self.meat)) + "\n")
        return res

    def __str__(self):
        return self.to_string()

    def dump(self):
        print(self.to_string())


class Decision(Enum):
    OPTIMAL = 1
    PARTIAL = 2
    BLOCKAGE = 3


class Status(Enum):
    GOOD = 1
    BAD = 2


############################################
#  Health Status Message
############################################
@dataclass
class HealthStatusMessage:
    '''Health Status Message'''
    ts: float
    dispenser: str
    icemaker: int
    lightbulb: str
    fridge_temp: int
    freezer_temp: int
    sensor_status: str

    def __init__(self):
        self.ts = time.time()

    def to_string(self):
        res = ""
        res += ("type: {}".format("HEALTH") + "\n")
        res += ("contents:" + "\n")
        res += ("  dispenser: {}".format(self.dispenser) + "\n")
        res += ("  icemaker: {}".format(self.icemaker) + "\n")
        res += ("  lightbulb: {}".format(self.lightbulb) + "\n")
        res += ("  fridge_temp: {}".format(self.fridge_temp) + "\n")
        res += ("  freezer_temp: {}".format(self.freezer_temp) + "\n")
        res += ("  sensor_status: {}".format(self.sensor_status) + "\n")
        return res

    def __str__(self):
        '''Pretty print the contents of the message'''
        return self.to_string()

    def dump(self):
        print(self.to_string())

    def set_dispenser(self, index):
        self.dispenser = Decision(index).name

    def set_lightbulb(self, index):
        self.lightbulb = Status(index).name

    def set_sensor_status(self, index):
        self.sensor_status = Status(index).name


class ResponseCode(Enum):
    OK = 1
    BAD_REQUEST = 2


############################################
#  Response Message
############################################
@dataclass
class ResponseMessage:
    '''Response Message'''
    ts: float
    code: str
    contents: str

    def __init__(self):
        self.code = ""
        self.contents = ""
        self.ts = time.time()

    def set_code(self, index):
        self.code = ResponseCode(index).name

    def to_string(self):
        res = ""
        res += ("  type: {}".format("RESPONSE") + "\n")
        res += ("  code: {}".format(self.code) + "\n")
        res += ("  contents: {}".format(self.contents) + "\n")
        return res

    def __str__(self):
        '''Pretty print the contents of the message'''
        return self.to_string()

    def dump(self):
        print(self.to_string())
