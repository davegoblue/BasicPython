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

#
# Week 04 - Many to Many in SQL
# There can be many students per course AND ALSO many course per student
# The techniques from the previous week need to be modified to properly handle this
# The previous track to album is a one-to-many relationship (there are many tracks per album; only one album per track)
# 	Often, a "crows foot" is used in the data modeling to suggest the "many" component of the relationship
# 	For example, with biological mother to child, you would link by having a "crows foot" on the children,
#   since each mother can have many children
# Suppose that there is a many-to-many relationship using books and authors;
# an author may write several books, and a book may have several authors
# 	One common solution is to add a "connection table" (has other names, e.g., "junction table" or "member table")
#   with two foreign keys
#	Books is unique by book
#	Authors is unique by author
#	Connection table is unique by book-author ("there is usually no separate primary key;
#   the combination of the book/author could be considered the primary key")
#		Books is one-to-many to authors in Connection
#		Authors is one-to-many to books in Connection
#	Relationship has become two versions of the many-to-one
#		Connection table has two foreign keys, and no primary key
# Gives an example of the implementation
#	User: ID*, Name, email
#	Course: ID*, Title
#	Member: User ID, Course ID, Role (teacher, student, etc.) . . .
#           Final line syntax is "PRIMARY KEY (user_id, course_id)"
# ORDER BY var1, var2 DESC, var3
#	This would be the equivalent in R of A[order(A$var1, -A$var2, A$var3)]
# Overwhelmingly, the reasons for doing all of this is speed
# 	Once your data becomes large enough, this becomes a necessity!
#
# Many to Many Roster Demonstration
#	Back to the decomposition of a many-to-many in to two separate many-to-one relationships
#	INSERT OR IGNORE
#		The "OR IGNORE" means "do not do this if it would cause an error;
#       since we required uniqueness, the error would be a duplicate"
#		In essence, this means it will create a primary key and INSERT the first time it sees something,
#       and will ignore it otherwise
#

# This assignment is to manage the many-to-many relationship
# There should be two unique primary-key tables, and a junction table including role
# Each primary-key table should be one-to-many to the junction table
# Code adapted from the Dr. Chuck starting point (roster.py)

import json
import sqlite3

mySQLConn = sqlite3.connect('_notuse_BP004v003.sqlite')
myCursor = mySQLConn.cursor()

# Create the appropriate tables (delete them if they already exist)
myCursor.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# Default to using roster_data.json, but allow flexibility as and when needed
fname = raw_input('Enter file name: ')
if (len(fname) < 1):
    fname = 'roster_data.json'

# File is formatted as a JSON list
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

userData = open(fname).read()
json_data = json.loads(userData)

# Read through each line of JSON, extracting user name, course title, and user role
for entry in json_data:
    userName = entry[0]
    courseTitle = entry[1]
    userRole = entry[2]

    # print userName, courseTitle, userRole

    # Put userName in to table User (if not yet there), and extract the associated primary key
    myCursor.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', (userName,))
    myCursor.execute('SELECT id FROM User WHERE name = ? ', (userName,))
    user_id = myCursor.fetchone()[0]

    # Put courseTitle in to table Course (if not yet there), and extract the associated primary key
    myCursor.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', (courseTitle,))
    myCursor.execute('SELECT id FROM Course WHERE title = ? ', (courseTitle,))
    course_id = myCursor.fetchone()[0]

    # Put user_id, course_id, and userRole in to table Member
    myCursor.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
                     (user_id, course_id, userRole))

# Commit (write everything to disk)
mySQLConn.commit()

#
# Visualization - Geocoding
# Geocoding - multiple steps process
# 	Data Source -> Gather to Raw DB -> Clean/Process (perhaps to Clean DB) -> Visualize / Analyze
# 		Goal is to let the Gather to Raw DB run independently (it can be slow, buggy, etc.)
# 		Once the data is in the Raw DB, the process is generally much smoother
# 	There are many data mining technologies
# 		Hadoop (Apache)
# 		Spark (Apache)
#		Redshift (Amazon)
# 		Pentaho
# 	This lecture is just about a very limited subset of data mining - "personal data mining"
# 		The goal is to become a better programmer, not a data mining expert
# 	Goal will be to talk with Google's geocoding API
# 		Google Maps from user data
# 		Uses the Google Geodata API
# 		Caches data in a database to avoid rate limiting and allow restarting
#		Visualized in a browser using Google Maps API
#		Dr Chuck plans to give his own API for this, to avoid having people hit Google API endlessly
# 	Two primary programs
#		geoload.py - takes the Google API and the locations data and creates geodata.sqlite
#		geodump.py - manipulates geodata.sqlite data to create the where.js (JSON file) for mapping
#
#
# Page Rank and Web Searching - simulate the Google page rank algorithm
# 	The page rank algorithm values links, and especially incoming links from more valuable pages
# 		Step 1: Web Crawling - Write a simple web crawler
# 		Step 2: Index Building - Compute a simple version of the page rank algorithm
# 		Step 3: Searching (we will instead visualize the resulting network for this example)
# 	Web Crawler goes to a page, finds all of its links, goes to those pages, etc.
# 		BeautifulSoup (or other programs) may be used to help fix/read "broken" html
# 		Further, might put the pages we have found in to a database
# 	For serious web-crawling, some business rules exist
# 		Selection policy (which pages to download)
# 		Re-visit policy (when to check for changes to the pages)
# 		Politeness policy (avoid overloading websites)
#		Parallelization policy (distributed web crawlers)
# 	There is often a robots.txt file for communication with web crawlers
# 		Informal and voluntary standards
# 		Sometimes people make "spider traps" to catch "bad" spiders
# 	Indexing is the collecting, parsing, and storing in a manner that enables very fast results
# 		Looking for the useful meaning inside the data
# 	The queue actually exists inside the database
# 		Web <-> spider.py <-> spider.sqlite
# 			Goes to the first page, stores all of its links in DB,
#           uses DB ordering as the queue for the next page to search
# 			At the beginning, this code would grow the DB very, very quickly at the beginning!
# 		The sprank.py program reads the pages and updates the page ranks
# 			sprank.py <-> spider.sqlite
# 		The spreset.py process returns everything to defaults so that you can start over
# 		The spdump.py prints out the current page list and associated ranks
# 			spider.sqlite -> spdump.py
# 		The spjson.py dumps out some JSON for visualizing the linkages
#       (visualization is done by JaveScript which is the .js)
# 			spider.sqlite -> spjson.py -> force.js -> visualization
#
# Gmane - Mailing Lists example (gmane.org archives web mailing lists)
# 	General process
# 		Step 1: Crawl the archive of a mailing list
# 		Step 2: Do some analysis/cleanup
# 		Step 3: Visualize data as word cloud and lines
# 	WARNING: This can be a ton of data!
# 		Do not just point at gmane.org and let it run (>1 GB)
# 		There is no rate limiting; do not choke your bandwidth or ruin access for everyone else
# 		Dr Chuck has a non-rate-limited version available
# 	This is a complicated work-flow
# 		gmane.org -> gmane.py -> content.sqlite -> gmodel.py -> content.sqlite
# 			"This raw data is a little messier than what we have been using;
#           goal of the second table is to put things in third normal form"
#           (this is what gmodel.py will do)
#
#           Cleaning is not done during gmane.py to 1) keep gmane.py simple, and
#           2) ensure we really get a raw copy of the data
#
# 		content.sqlite -> gline.py -> gline.js -> line graphs
# 		content.sqlite -> gword.py -> gword.pj -> word cloud
# 		content.sqlite -> gbasic.py -> dump of top participants
#	Three different examples of data-mining
#
# Back to the geocoding example from above
# 	The command buffer(address) will revert address to plain text (what we want) rather than unicode (what we do not)
# 	The command pass means (more or less) continue along, used inside the except: as the sole statement
# 	Generally a good idea to print the data and then quit if something goes wrong in one of the functions
#
#


import urllib
import sqlite3
import json
import time
import codecs


serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"
scontext = None

conn = sqlite3.connect('_notuse_BP004v004.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

fh = open("where.data")
count = 0
for line in fh:
    if count > 200 : break
    address = line.strip()
    print ''
    cur.execute("SELECT geodata FROM Locations WHERE address= ?", (buffer(address), ))

    try:
        data = cur.fetchone()[0]
        print "Found in database ",address
        continue
    except:
        pass

    print 'Resolving', address
    url = serviceurl + urllib.urlencode({"sensor":"false", "address": address})
    print 'Retrieving', url
    uh = urllib.urlopen(url, context=scontext)
    data = uh.read()
    print 'Retrieved',len(data),'characters',data[:20].replace('\n',' ')
    count = count + 1
    try:
        js = json.loads(str(data))
        # print js  # We print in case unicode causes an error
    except:
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print '==== Failure To Retrieve ===='
        print data
        break

    cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', ( buffer(address),buffer(data) ) )
    conn.commit()
    time.sleep(1)

fh.close()
cur.close()
conn.close()


# Next we will pretty the data for viewing


conn = sqlite3.connect('_notuse_BP004v004.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('where.js','w', "utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur :
    time.sleep(0.25)  # Have a sleep before each step (for screenshot)
    data = str(row[1])
    try: js = json.loads(str(data))
    except: continue

    if not('status' in js and js['status'] == 'OK') : continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'","")
    try :
        print where, lat, lng

        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print count, "records written to where.js"
print "Open where.html to view the data in a browser"


