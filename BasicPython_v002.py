# Summary of Chapters 6-10
#
# Chapter 6 - Strings
# Note that strings are immutable, so if fruit = "banana", cannot do fruit[0] = "D"
# Further note that indexing is bizarre in Python in general
# 0 is the first element, and len(fruit)-1 is the last element
# Further, requesting [m:n] means "give me back m through n-1
# And, [:n] means given me beginning through n-1, [m:] means given me m through end, and [:] means given me all
# Further [-m] means give me the last mth digit, so [-1] means last, [-2] means second last, etc.

fruit = "banana"  # example of a string
print fruit[0], fruit[3:], fruit[:3], fruit[:], fruit[0:6]
print fruit[-1], fruit[2:-1]  # Tres confusing!

# The for loop will move through a string in index order
for whatFound in fruit:
    print whatFound

# The in operator checks whether a given substring is in the main string
print "a" in fruit, "d" in fruit, "ana" in fruit  # True False True

# String comparisons - upper is always before lower
print "Pineapple" < fruit, "pineapple" < fruit, "apple" < fruit  # True False True

# Strings have many built in functions
# Each of these as a standalone does nothing to the original string
print fruit.capitalize(), fruit.upper(), fruit.lower()  # Banana BANANA banana
print fruit.find("a")  # Index of the first a (1)
print fruit.find("nn")  # -1 signalling non-existence
print fruit.find("na")  # Index of the first na (2)
print fruit.find("na", 3)  # Index of the first na at/after index 3 (4)

# The string can also be manipulated to remove leading/trailing whitespace
# Strings are similarly immutable on these functions
myProblem = "  Here is a sentence with some goofy formatting  \t \n"
print myProblem
print myProblem.strip()  # Remove trail/lead whitespace
print myProblem.lstrip()  # Remove lead whitespace
print myProblem.rstrip()  # Remove trail whitespace

# The startswith and endswith are handy shortcuts to avoid regular expressions; returns Boolean
print myProblem.strip().lower().startswith("h")  # True
print myProblem.strip().lower().startswith("H")  # False (has been converted to lower)
print myProblem.strip().lower().endswith("g")  # True

# There is also a rather handy formatting operator, with %d as integer, %g as float, %s as string
print "In %g years, I have spotted %d %s" % (3.5, 42, "camels")  ## In 3.5 years, I have spotted 42 camels"

# Some additional useful string functions
# str.replace(old, new, count=NULL) - replace old with new, maximum of count times
# str.rfind(sub, start=NULL, end=NULL) - finds highest index matching sub, uses start/end as : and returns -1 if none
# str.rindex(sub, start=NULL, end=NULL) - same as rfind but returns ValueError rather than -1 for no match
# str.rjust(width, fillchar=" ") - right justified string of length width, leading characters made fillchar
# str.center(width, fillchar=" ") and str.ljust(width, fillchar=" ") are substantially the same thing

print fruit.replace("a", "A"), fruit.replace("a", "A", 2)  # bAnAnA bAnAna
print fruit.rfind("a"), fruit.rfind("c")  # 5 -1
print fruit.rjust(8,"*"), fruit.center(8,"*"), fruit.ljust(8,"*")  # **banana *banana* banana**
print fruit.rjust(4,"*")  # banana (note that since the requested width is less than banana, it gives back banana


# Chapter 7 - Files
# Python in general has an open() which returns a handle
# The handle can either be passed to .read() or used as for lines in handle:
# Our file happens to be located in ..\UMWeek07\mbox-short.txt

fhandShort = open("..\UMWeek07\mbox-short.txt")

# Method 1 (pulls everything to memory)
inpShort = fhandShort.read()
print len(inpShort)
print inpShort[:100]

# Method 2 (line by line reading)
fhandShort = open("..\UMWeek07\mbox-short.txt")
for eachLine in fhandShort:
    if eachLine.startswith("From:"): print eachLine.strip()

# Files can be written out in a similar manner
# The "w" or "wb" is passed to the open() command
# Then, the .write() is used

fhandOut = open("dummyOut.txt", "w")
line1 = "This here's the wattle,\n"
line2 = "the emblem\t:\tof our land.\n"
fhandOut.write(line1)
fhandOut.write(line2)  # Default is append
fhandOut.close()

# The repr() will print out the tabs and newlines, which can be useful for debugging
print line1, line2
print repr(line1), repr(line2)

# Chapter 8 - Lists
# Lists are sequences of values (of any or even mixed types), denoted with []
# Lists have the same indexing as strings, and are mutable
# The range(n) operator creates an index from 0 to n-1, helpful for traversing lists

myList = ["spam", 2.0, 5, [10,20]]
print len(myList)
for ctr in range(len(myList)):
    print ctr, type(myList[ctr]), myList[ctr]
myList[1] = 2.0 * myList[2]
print myList

print 10 in myList, 10.0 in myList # True True

emptyList = []
for x in emptyList: print "Never got here!"
emptyList = list()
for x in emptyList: print "Still never got here!"
emptyList = [[]]
for x in emptyList: print "But I did get here!", x

# List concatenation is done with +, while * means repeat
listA = [1, 2]
listB = [3, 4]
print listA + listB, listA * 3  # [1, 2, 3, 4] [1, 2, 1, 2, 1, 2]
print (listA + listB)[1:3]  # [2, 3]

# There are multiple ways to delete an element from a list
#
saveList = myList[:]  # Avoids aliasing
tempList = myList  # Aliasing, dangerous!
print tempList, saveList  # ['spam', 10.0, 5, [10, 20]] ['spam', 10.0, 5, [10, 20]]
print tempList is myList, saveList is myList  # True False

# .pop(n) will delete item n and return it to the console
x = tempList.pop(2)
print x, tempList
print myList  # Oopsies!

myList = saveList[:]
print myList
x = saveList.pop(2)
print x, saveList
print myList  # Much better

# del list(n) will delete item n from the list, without popping
saveList = myList[:]  # Avoids aliasing
del saveList[1]
print saveList, myList

# .remove(value) will remove the first item that matches value
saveList = myList[:]  # Avoids aliasing
saveList.remove(5)  # Will only remove the first 5 in the list
print saveList, myList

# Lists use len, max, min, sum
print len(myList), max(myList), min(myList), sum(myList[1:3])  # 4 spam 5 15.0

# Lists can be used to convert character strings
myString = "Bananas are sometimes tasty"
print list(myString)
print myString.split(" ")  # ["Bananas", "are", "sometimes", "tasty"]
x = "_"
print x.join(myString.split(" "))  # "Bananas_are_sometimes_tasty"

# Can use .strip() to get rid of whitespace, .startswith() to grep key lines, and .split() to make a list
fhand = open("..\UMWeek07\mbox-short.txt")
for eachLine in fhand:
    eachLine = eachLine.strip()
    if not eachLine.startswith("From "): continue
    myWords = eachLine.split()
    if len(myWords) > 2: print myWords[2]

# Reminder on aliasing
print "***\t***\n\n"
a = "bananas"
b = "bananas"
print a is b  # True (sort of OK since these are immutable)
a = a + " are sometimes tasty"
print a, b, a is b  # Works out OK

a = [1, 2, 3]
b = [1, 2, 3]
print a is b  # False (lists do not alias even if like this
a = b
print a is b, a, b  # True (this could cause problems
a = b[:]
print a is b, a, b  # False

# The textbook is rather understated in calling this behavior "highly error prone"


# Note that most list operations return None
t1 = [1, 2]
t2 = t1.append(3)
print t1, t2  # [1, 2, 3] None

t1 = [1, 2]
t2 = t1 + [3]
print t1, t2  # [1, 2] [1, 2, 3]


# Similar behavior in functions
def tail(t): return t[1:]
letters = ["a", "b", "c"]
tail(letters)
print letters  # ["a", "b", "c"]
rest = tail(letters)
print rest, letters  # ["a", "b"] ["a", "b", "c"]
letters = tail(letters)
print letters  # ["b", "c"]


# Use of the range() command - all arguments must be integers
print range(5)  # [0, 1, 2, 3, 4]
print range(1, 5)   # [1, 2, 3, 4]
print range(1, 5, 2)  # [1, 3]


# Chapter 9 - Dictionaries
# A dictionary is a type of associative array - mapping of key-value pairs (items)
# Items can be created on the fly, which can be quite helpful
# The dictionary can either be called with dict() or set using {"key1":"value1", "key2":"value2"}
# There is no real meaning to the order of the items in the dictionary - do not count on predictable/logical order
eng2sp=dict()
print eng2sp  # {}
eng2sp["one"] = "uno"
eng2sp["two"] = "dos"
eng2sp["three"] = "tres"
print eng2sp  #  {'three': 'tres', 'two': 'dos', 'one': 'uno'}
print eng2sp["two"], len(eng2sp), type(eng2sp)  # "dos" 3 <type 'dict'>

# The in operator lets you check the keys, while .values() gives a list of the values
print "one" in eng2sp, "four" in eng2sp, "tres" in eng2sp  # True False False
print "one" in eng2sp.values(), "tres" in eng2sp.values()  # False True

# The .get() is a pretty nice way to simplify coding for dictionaries
myWord = "Brontosaurus"

# Typical method using if/else
d1 = dict()
for eachChar in myWord.lower():
    if eachChar not in d1:
        d1[eachChar] = 1
    else:
        d1[eachChar] = d1[eachChar] + 1
print d1

# Refined method using .get()
d2 = dict()
for eachChar in myWord.lower():
    d2[eachChar] = d2.get(eachChar, 0) + 1  # The second argument to .get() is what comes back for a no-match
print d2

print d1==d2, d1 is d2  # True False

# For loops iterate through dictionary *keys*
for eachItem in d1:
    print eachItem, d1[eachItem]

# Or, if you want to sort by eachItem
d1List = d1.keys()
d1List.sort()
for eachItem in d1List:
    print eachItem, d1[eachItem]

# Stripping puctuation can be helpful - can use .translate(None, deleteList)
import string
print string.punctuation  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
myLine = "**This, I must say, eh?  Punctuation, overdone, is unpleasant! :-)"
print myLine.split()
# ['**This,', 'I', 'must', 'say,', 'eh?', 'Punctuation,', 'overdone,', 'is', 'unpleasant!', ':-)']
print myLine.translate(None, string.punctuation).split()
# ['This', 'I', 'must', 'say', 'eh', 'Punctuation', 'overdone', 'is', 'unpleasant']

# Example assignment code
fileName = "..\UMWeek07\mbox-short.txt"
handle = open(fileName)
nameCount = dict()

for eachLine in handle:
    if not eachLine.strip().startswith("From "):
        continue
    msgSender = eachLine.strip().split()[1]
    nameCount[msgSender] = nameCount.get(msgSender,0) + 1

maxSender = ""
maxCount = 0

for msgSender, ctSender in nameCount.items():
    if ctSender > maxCount:
        maxCount = ctSender
        maxSender = msgSender

print maxSender, maxCount
