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