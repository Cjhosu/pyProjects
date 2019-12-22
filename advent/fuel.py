import math

mod_list = []

with open('modules') as file:
    for linez in file:
        mod=int(linez)
        modbythree= mod/3
        val= (math.floor(modbythree)) - 2
        mod_list.append(val)

tot=0
for item in mod_list:
    tot += item
    print(item)
    print(tot)
