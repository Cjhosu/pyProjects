import re

with open('sample.csv') as file:
    typelist = ()
    for line in file:
        if re.match(".*table.*",line):
            key, value = line.split(":")
            print('INSERT INTO' +value , end="")
        elif re.match (".*columns.*",line):
            pairs = dict(item.split(":") for item in line.split(","))
            typelist = list(pairs.values())
            collist = list(pairs.keys())
            columns = ", ".join(collist[1:])
            print('('+ columns +')  VALUES')
        else:
            line = line.strip()
            dlist = line.split(",")
            zipped = zip(typelist[1:],dlist)
            data = dict(zipped)
            mylist = []
            if not line == "":
                print("(",end="")
                for k,v in data.items():
                    if k.strip() == "int" or k.strip() == "boolean":
                        mylist.append(v)
                    else:
                        mylist.append("'" +v + "'")
                print(",".join(mylist)+ "),")
            else:
                print('\n' , end="")
