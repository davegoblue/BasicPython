# This document is to summarize a series of web services exercises from UM Python Cousera
#
# Object-Oriented Background (Week 01)
# "Objects" have a specific shape (schema) by definition
# "Methods" are like functions that are inherently part of an object
# "Construct" means to create a new object
# "Deconstruct" means to kill an existing objects (happens automatically at end of program, if not sooner)
#
# An "object" is a bit of self-contained code and data
# "Object Oriented Programming" (OOP) is a program written of cooperating objects
# Advantages of OOP include 1) breaking problems in to smaller pieces, 2) consistency, and 3) keeping boundaries
# Specifically, the object can have a lot of complexity programmed in to it; this is invisible to the end user
#
# Class - template or cookie-cutter or blueprint/factory/pattern (e.g., a dog)
# Method or Message - pre-defined capability of a class (e.g., bark)
# Field or Attribute - piece of data in a class
# Object or Instance - particular instance of a class; the actual cookie or factory output (e.g., Lassie)


class PartyAnimal:
    x = 0

    def party(self):
        self.x = self.x + 1
        print "So far", self.x


myAnimal = PartyAnimal()
myAnimal.party()  # So far 1
myAnimal.party()  # So far 2
myAnimal.party()  # So far 3

print dir(myAnimal)  # Shows all the methods and data available ['__doc__', '__module__', 'party', 'x']

# The methods with leading __ are for Python-only (help with sorting and the like
# The __init__ method, if it exists, is called whenever the object is constructed
# The __del__ method, if it exists, is called whenever the object is deconstructed (__del__ is rarely used)
# Each distinct object is stored on its own, so self.x will (can) be different for every PartyAnimal object
# Can also pass arguments to the class; known as aliasing
#
# Inheritance is the idea that a sub-class can take on all the properties of an existing class
# This is a form of "store and reuse", also known as "extending a class"
# The new class (child) inherits all capabilities of the old class (parent), plus new ones


class FootballFan(PartyAnimal):  # This asks FootballFan to inherit PartyAnimal
    points = 0  # FootballFan will now have x and name (from PartyAnimal) and points (per below)

    def touchdown(self):
        self.points = self.points + 7
        self.party()
        print "points", self.points


myFan = FootballFan()
myFan.party()  # So far 1
myFan.touchdown()  # So far 2  points 7
myFan.party()  # So far 3