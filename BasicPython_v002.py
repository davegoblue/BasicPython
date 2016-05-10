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