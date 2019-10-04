import re

with open('sample.csv') as file:
    keylist = ()
    datalist = ()
    for line in file:
        if re.match(".*table.*",line):
            key, value = line.split(":")
            print('INSERT INTO' +value , end="")
        elif re.match (".*columns.*",line):
            pairs = dict(item.split(":") for item in line.split(","))
            vallist = list(pairs.values())
            keylist = list(pairs.keys())
            columns = ", ".join(keylist[1:])
            print('('+ columns +')  VALUES')
        else:
            line = line.strip()
            dlist = line.split(",")
            data = (','.join("'" + item + "'" for item in dlist))
            print (data)
