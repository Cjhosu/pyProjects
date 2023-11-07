import random
import sys, getopt

dice = 0
sides = 0

argv = sys.argv[1:]
opts, args = getopt.getopt(argv,"d:s:", ["--dice=", "--sides="] )

for opt, arg in opts:
    if opt in ("-d", "--dice"):
        dice = int(arg)
    elif opt in ("-s", "--sides"):
        sides = int(arg)

def diceroll(dice, sides):
    for x in range(0,dice):
        print(random.randint(1,sides))

diceroll(dice, sides)
