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

# The .close() closes out the cursor, and the fh.close() closes out the file handle
myPointer.close()
fh.close()
print fh  # <closed file 'mbox.txt', mode 'r' at 0x02352BD0>


# Data Models and Relational SQL
# A data model links various tables together
# Database design is an art form, with particular skills and experience
# Goal is to avoid bad mistakes -- build a clean, easily understood database
# Typically, there will ba a picture showing the relationships among the tables
# Smart data models will run MUCH faster than having everything in one place
# The gist is that numbers and indices are vastly faster for look-ups than text
# One of the basic "rules" is to have only one copy of each "real world thing" in the database
# For every piece of information, identify whether it is an object, or an attribute of another object
# 	Where you start is not all that important, though starting in a good place (the most central feature)
#   often makes the picture better
#   For example, if you are selling tracks, you probably want the track to be the centerpiece of the system
#   Suppose that the data is Track - Album - Artist - Genre - Length - Rating - Count
#       Length, Rating, Count, Genre (because it can be different for the same Album/Artist) are attributes of Track
#       Album, Artist, are NOT attributes of Track -- they are instead connected to tracks
#       Tracks would belong to Albums, Albums would belong to Artists
#   Basically, the exercise is about what "belongs" to who
#
# Next, the goal is to map the data model picture in to a data model with tables
# 	So, we might take the Track table and start with a primary key, ID
# 		There will also be Title, Rating, Length, and Count
# 		There will also be Album ID, since we agreed that tracks belong to Albums
# 	There will then be an Album table with primary key ID and then Title
# 	Can think of the hierarchy as
# 		Table (name)
# 		Primary Key (using ID in this case)
# 		Logical Key (things about the object that should have a shortcut to them -- likely WHERE or ORDER BY clause)
# 		Foreign Key (links to ID in other tables)
#		There are also attributes that do not have any keys -- we do not plan to search/source on them
# 	Generally, comply with the naming conventions of the organizations that you work with (e.g., "Ruby on Rails")
# 	Gives an example of using DB Broswer for SQLite to create a new table
#		The check boxes are for "create field" are "Not Null", "Primary Key", "AutoIncrement", and "Unique"
# 	Typical approach is to work from outwards in on the diagram
# 		The foreign keys are set as integers, usually with a reasonable name to say
#       what foreign table they are linking to
#
# Next, the goal is to create the relational data
# 	The key words in SQL are case independent (interesting), so INSERT INTO can be written Insert Into or insert into
# 	When an auto-increment is requested, it would just be INSERT INTO Artist (name) VALUES ("Led Zeppelin")
# 		INSERT INTO Genre (name) VALUES ("Rock")
# 			Note that we created the table Genre even though it is an attribute of Track;
#           this is due to integers taking up much less space than strings
#       The ; at the end of a command tells SQL that I am going to have a few different commands
#       INSERT INTO Album (title, artist_id) VALUES ("Who Made Who", 2)
# 			The foreign keys needs to be put in -- easy for the code to figure this out, harder for the human
# 	"Replication is OK as long as it is numbers"
# 		Over-riding objective is to not replicate text strings
# 		The less replication of strings, the faster the table will run
# 		Goal is to reduce the amount of data that needs to be scanned during operations
#       (plus, indices to speed things up even further)
#
# Lastly, the goal is to piece everything back together - reconstructing with JOIN
# 	The relational database can read through the web of information very quickly
# 		Often, when you want to retrieve/view some data, it comes from many tables linked by foreign keys
# 		Data tends to scale - make sure to plan for that in advance
# 	The JOIN operation says that we are connecting tables ON certain key(s)
# 		SELECT Album.title, Artist.name FROM Album JOIN Artist ON Album.Artist_id = Artist.id
# 			Generally, the ON and WHERE clauses will work the same on the JOIN operator
# 		If you skipped the ON clause, then you will get the full JOIN (all possible combinations of rows)
# 	Can have multiple JOIN all at the same time
# 		SELECT Track.title, Artist.name, Album.title, Genre.name FROM Track JOIN Genre JOIN Album JOIN Artist
#           ON Track.genre_id=Genre.id AND Track.Album_id=Album.id AND Album.artist_id = Artis.id
#
# There is a nice trick available when having set up a variable as UNIQUE in the SQL
#   INSERT OR IGNORE INTO  # Will INSERT if it does not exist or IGNORE if the INSERT would make a duplicate
#   INSERT OR REPLACE INTO  # Same idea, with the row either being created, or updated if it already exists
# In general, it is beneficial to write long single-line SQL queries when possible, rather than splitting them up
#
# Example assignment code
#


import xml.etree.ElementTree as ET
import sqlite3

conSQLFile = sqlite3.connect('_notuse_BP004v002.sqlite')
myCursor = conSQLFile.cursor()

# Note that executescript() is used to send multiple lines to SQL at the same time
myCursor.executescript('''

DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);

''')

fname = raw_input('Enter file name: ')
if (len(fname) < 1):
    fname = 'Library.xml'


def lookup(xmlString, searchTerm):
    found = False
    for child in xmlString:
        # Rather klugey - found gets set to True below, and then the VERY NEXT item is returned, ending the lookup
        if found:
            return child.text

        # Rather klugey - this line will find a "key" tag that matches to searchTerm but NOT return it
        if child.tag == 'key' and child.text == searchTerm:
            found = True

    # If nothing has been found, return None
    return None


# Now, read the XML that is in the passed file
xmlData = ET.parse(fname)
trackData = xmlData.findall('dict/dict/dict')
print 'Dict count:', len(trackData)   # Dict count: 404

# Now, take the relevant data and populate the key tables
for entry in trackData:

    if (lookup(entry, 'Track ID') is None):
        continue

    # Artist will require name, stored as "Artist"
    artistName = lookup(entry, 'Artist')

    # Genre will require name, stored as "Genre"
    genreName = lookup(entry, 'Genre')

    # Album will require title, stored as "Album"
    albumTitle = lookup(entry, 'Album')

    # Track requires title stored as "Name", len stored as "Total Time", rating stored as "Rating", and count stored as "Play Count"
    trackName = lookup(entry, 'Name')
    trackLen = lookup(entry, 'Total Time')
    trackRating = lookup(entry, 'Rating')
    trackCount = lookup(entry, 'Play Count')

    # Only include items that have full proper entries for the database
    if artistName is None or genreName is None or albumTitle is None or trackName is None:
        continue

    # print name, artist, album, count, rating, length

    # Update the Artist table, including fetching the artist_id
    myCursor.execute('''INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', (artistName,))
    myCursor.execute('SELECT id FROM Artist WHERE name = ? ', (artistName,))
    artist_id = myCursor.fetchone()[0]

    # Update the Genre table, including fetching the genre_id
    myCursor.execute('''INSERT OR IGNORE INTO Genre (name)
        VALUES ( ? )''', (genreName,))
    myCursor.execute('SELECT id FROM Genre WHERE name = ? ', (genreName,))
    genre_id = myCursor.fetchone()[0]

    # Update the Album table, including fetching the album_id
    myCursor.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
        VALUES ( ?, ? )''', (albumTitle, artist_id))
    myCursor.execute('SELECT id FROM Album WHERE title = ? ', (albumTitle,))
    album_id = myCursor.fetchone()[0]

    # Update the Track table
    myCursor.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count)
        VALUES ( ?, ?, ?, ?, ?, ? )''',
                     (trackName, album_id, genre_id, trackLen, trackRating, trackCount))

# Commit the database
conSQLFile.commit()

