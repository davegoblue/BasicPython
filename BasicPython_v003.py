# This document is to summarize a series of web services exercises from UM Python Cousera
#
# Chapter 11 - Regular Expressions
# Need to start by importing the re library
# Typical commands are re.search() and re.findall()

import re
myText = "Hello there: this is fun is it not?"
a = re.search("hello", myText)  # returns a matchObject
b = re.search("there", myText)  # returns a matchObject
c = re.search("is ", myText)  # returns a matchObject

# The matchObject is always None if nothing matched (note that hello is a mismatch due to case)
print a is not None, b is not None, c is not None  # False True True
if a is not None: print "a:", a.group(0)  # <no line printed>
if b is not None: print "b:", b.group(0)  # b: there
if c is not None: print "c:", c.group(0)  # c: is <note that even though two is, just one print item

# The ^ means starts with
a = re.search("^Hello", myText)
b = re.search("^there", myText)
print a is not None, b is not None  # True False

# The period can stand for any character
a = re.search("i..i", myText)  # will match anything with i having two things between it
if a is not None: print "a (i..i):", a.group(0)  # a (i..i): is i

# The ? means one or more while the * means 0 or more
# Note that \S means non-whitespace while \s means whitespace
a = re.search(":.+i", myText)  # should pick up greedily : this is fun is i
b = re.search(":.*d", myText)  # should be none, cannot find
print a is not None, b is not None  # True False

# The findall() is a touch easier to use!
fhand = open("../UMWeek07/mbox-short.txt")
for eachLine in fhand:
    eachLine = eachLine.strip()
    lineList = re.findall("\S+@\S+", eachLine)  # find 1+ non-whitespace, then @, then 1+ non-whitespace
    if len(lineList) > 0: print lineList

# Then, to keep out all the weird excess characters
fhand = open("../UMWeek07/mbox-short.txt")
for eachLine in fhand:
    eachLine = eachLine.strip()
    lineList = re.findall("[a-zA-Z0-9]\S*@\S*[a-zA-Z0-9]", eachLine)  # using * now; first character alphanumeric
    if len(lineList) > 0: print lineList

# Note that since re.search() is declared to be True if found (a touch confusing . . . )
fhand = open("../UMWeek07/mbox-short.txt")
for eachLine in fhand:
    eachLine = eachLine.strip()
    if re.search("^X-\S*: [0-9.]+", eachLine): print eachLine

# Note that () mean just give me back this specific item
fhand = open("../UMWeek07/mbox-short.txt")
for eachLine in fhand:
    eachLine = eachLine.strip()
    myNum = re.findall("^X-\S*: ([0-9.]+)", eachLine)
    if len(myNum) > 0: print myNum

# Another example
fhand = open("../UMWeek07/mbox-short.txt")
for eachLine in fhand:
    eachLine = eachLine.strip()
    myNum = re.findall("^From .* ([0-9][0-9]):", eachLine)  # Line starts with From-space, then space-##: (pull ##)
    if len(myNum) > 0: print myNum

# The escape character is the backslash, meaning treat it as-is
# So \$ means pull out $ whereas $ would typically mean ends-with
myText = "We just realized with 20-20 hindsight that there is still $10.95 for the cookie fund"
print re.findall("\$[0-9.]+", myText)  # $10.95 -- command requires $ then series of nothing but 0-9.

# Some additional handy expressions
# ^ starts-with
# $ ends-with
# . wildcard (any character)
# \s whitespace character
# \S non-whitespace character
# * match 0+ of the immediately preceeding character
# *? match 0+ of the immediately preceeding character in "non-greedy" mode
# + match 1+ of the immediately preceeding character
# +? match 1+ of the immediately preceeding character in "non-greedy" mode
# [aeiou] match anything inside the brackets (these are EXACT, with no need for escape characters)
# () ignored for matching purposes, but only what is inside the () is returned
# \d is equivalent to [0-9]
# \D is equivalent to [^0-9]


# Chapter 12 - Networked programs
# HTTP is HyperText Transfer Protocol
# Python has a socket library, allowing the end user to be a basic browser
import socket


# Read in a text file with header
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(("www.py4inf.com", 80))
mysock.send("GET http://www.py4inf.com/code/romeo.txt HTTP/1.0\n\n")

while True:
    data = mysock.recv(512)
    if len(data) < 1: break
    print data

mysock.close()

import socket
import time


# Read in an image file with header
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(("www.py4inf.com", 80))
mysock.send("GET http://www.py4inf.com/cover.jpg HTTP/1.0\n\n")
count = 0
picture=""

while True:
    data=mysock.recv(5120)
    if len(data) < 1: break
    time.sleep(0.1)  # Keep the lines all at 5120
    count = count + len(data)
    print len(data), count
    picture = picture + data

mysock.close()

# Grab the header (ends with two straight CRLF)
pos = picture.find("\r\n\r\n")
print "Header length", pos
print picture[:pos]

# Ditch the header and save the picture
picture = picture[pos+4:]
fhand = open("stuff.jpg", "wb")
fhand.write(picture)
fhand.close()


# Alternately, this can all be done much easier with urllib
import urllib

# Use the urllib library to manage this
fhand = urllib.urlopen("http://www.py4inf.com/code/romeo.txt")  # consumes headers, returns only data
for line in fhand: print line.rstrip()

# Alternately, use urllib to get word counts
counts = dict()
fhand = urllib.urlopen("http://www.py4inf.com/code/romeo.txt")  # consumes headers, returns only data
for line in fhand:
    words = line.split()
    for word in words: counts[word] = counts.get(word, 0) + 1

print counts


# The BeautifulSoup library can also be used to help repair "broken" HTML
# import urllib
# from BeautifulSoup import *
#
# Use BeautifulSoup to extract the links
# url = raw_input("\nEnter - ")
# html = urllib.urlopen(url).read()
# soup = BeautifulSoup(html)
# tags = soup("a") # Retrieve anchor tags
#
# Print the tag, then extract in more detail
# for tag in tags:
#     print "TAG:", tag
#     print "URL:", tag.get("href", None)
#     print "Content:", tag.contents[0]
#    print "Attrs:", tag.attrs

# Can also use regular expressions to scarpe the web - this is essentially what Google does
import urllib
import re

# Use regular expressions to scrape for web links
url = raw_input("\nEnter - ")
html = urllib.urlopen(url).read()
links = re.findall('href="(http.*?://.*?)"', html)
for link in links: print link
