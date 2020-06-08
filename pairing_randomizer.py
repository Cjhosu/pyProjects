import random

DBAS = ['caleb', 'jp', 'victoria', 'anna', 'brad', 'kalpesh', 'david', 'ryan']
dontpair = []
count = 1

with open('donotpair.txt', 'r') as filelist:
    for line in filelist:
        currentline = line[:-1]
        appenditem = tuple(eval(currentline))
        dontpair.append(appenditem)

class Pairing:

    def getdbas(self):
        global count
        while DBAS != []:
            firstdba = (random.choice(DBAS))
            DBAS.remove(firstdba)
            self.setpair(self,firstdba)
        with open('donotpair.txt', 'w') as wfilelist:
            for listitem in dontpair:
                wfilelist.writelines('%s\n' % str(listitem))

    def setpair(self, firstdba):
            global count
            try:
                seconddba = random.choice(DBAS)
            except:
                print('Acceptable pairs are running low. randomize again')
                return
            pair = (firstdba, seconddba)
            reflect = (seconddba, firstdba)
            print ('attempting to pair '+ str(pair))
            if count > 10:
                return
            elif pair in list(dontpair) or reflect in list(dontpair):
                print('Should not pair'+ str(pair))
                count += 1
                self.setpair(self, firstdba)
            else:
                DBAS.remove(seconddba)
                print('successfully paired ' + str(pair))
                dontpair.append(pair)

if __name__ ==   '__main__':
    Pairing.getdbas(Pairing)


