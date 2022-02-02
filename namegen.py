import sys, random

print("Welcome to the name generator.\n")
print("here are some names\n")

first = ('Baby-Oil', 'Ched', 'Chewy', 'Fancypants', 'Huggy', 'Lunch Money')
last = ('Appleyard', 'Bloominshine', 'Endicott', 'Guster', 'Oxhandler', 'Walkingstick')

while True:
    firstName = random.choice(first)
    lastName = random.choice(last)

    print("\n\n")

    print("{} {}".format(firstName, lastName), file=sys.stderr)
    print("\n\n")

    try_again = input("\n\nTry again? (Press Enter else n to quit)\n")
    if try_again.lower() == "n":
        break

input("\nPress Enter to exit.")
