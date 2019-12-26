pinlist =[]
donelist = []
def check_order(strlist):
    idx = 0
    for x in range (0,5):
        idx = x
        if strlist[idx] > strlist[idx+1]:
            return
    new =''.join(strlist)
    donelist.append(new)
    #print(donelist)

def serialize(strlist):
    idx = 0
    for x in range (0,5):
        idx = x
        if strlist[idx] == strlist[idx+1]:
            #print(strlist)
            check_order(strlist)
            return

for num in range(254032,789860):
    pinlist.append(num)

for num in pinlist:
    strlist= list(str(num))
    serialize(strlist)

print(len(donelist))
#print(donelist)
