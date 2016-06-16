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

# Introduction to Databases
# DB Browser for SQLite has been downloaded and can run SQL commands
# Relational Databases are designed for fast data retrieval - linking data
# Database - contains many tables
# Relation (or table) - contains tuples and attributes, specifically "set of tuples having the same attribute"
# Tuple (row) - set of fields representing an object (e.g., person)
# Attribute (column, field) - one of possibly many elements of data corresponding to the object
# The first row sometimes contains metadata (structure, schema) about the rest of the table
#
# Structured Query Language (SQL) is the language used to access the data - API (contract) between DB and software
# Create, Retrieve, Update (or Insert), Delete - the CRUD methodology
# The existence of the API means that SQL can talk to Oracel or MySQL or any other apps
# SQL is a simple and powerful language that depends on the data being pretty
# Python is more rough around the edges, but much better with manipulating dirty data
#
# Most database projects split the roles of Application Developer and Database Administrator
# The AD and DBA may build the data model together; only the DBA may typically access/modify the raw data
# In small projects, the AD and DBA may be the same person!
# SQLite is an "embedded database" that is so small it can be built in to the software (as it is for Python)
#
# Example of using DB Browser for SQLite
# File - New Database - Execute SQL tab
# CREATE TABLE Users ( name TEXT(128), email TEXT(128) )
# Go to the Browser tab and enter your data
# Chuck	    csev@umich.edu
# Colleen	vlt@umich.edu
# Sally	    sally@umich.edu
# Fred	    fred@umich.edu
# INSERT INTO Users (name, email) VALUES ("Kristin", "kf@umich.edu") <adds record>
# DELETE FROM Users WHERE email="fred@umich.edu" <will delete any records - 0 through all - matching query>
# UPDATE Users SET name="Charles" WHERE email="csev@umich.edu" <will change name everywhere it sees e-mail>
# SELECT * FROM Users <grab all records>
# SELECT * FROM Users WHERE email="csev@umich.edu" <just the records matching the e-mail address>
# SELECT * FROM Users ORDER BY email <sort the data by email>

# Read mbox.txt and count the domain names
# Commit the database to the .sqlite format

# First, import sqlite3, create SQLite using connect, and create a pointer using curson

import sqlite3

connSQL = sqlite3.connect('_notuse_BP004v001.sqlite')
myPointer = connSQL.cursor()

# The .execute asks to run a SQL command; can use ''' to open/close and split it over lines in Python
# Delete any existing table called counts and open a new table Counts
myPointer.execute('DROP TABLE IF EXISTS Counts')
myPointer.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Default to reading mbox.txt, but allow flexibility for others
fname = raw_input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox.txt'
fh = open(fname)

for line in fh:
    if not line.startswith('From: '):
        continue
    domName = line.split()[1].split("@")[1]

    # Find the lines that already match this domain name
    myPointer.execute('SELECT count FROM Counts WHERE org = ? ', (domName,))

    # The .fetchone() grabs the first matching row from the SQL query; will be None if non-existent
    # Basically, create the line (INSERT INTO) with count=1, or update (UPDATE) the line to count=count+1
    if myPointer.fetchone() is None:
        myPointer.execute('INSERT INTO Counts (org, count) VALUES ( ? , 1 )', (domName,))
    else:
        myPointer.execute('UPDATE Counts SET count=count+1 WHERE org = ?', (domName,))

# The .commit() writes to the DB; can put in the for loop (slower/safer) or leave outside
# Need to have the .commit() somewhere though, to make sure data is written out
connSQL.commit()
