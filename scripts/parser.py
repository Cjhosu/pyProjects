import re

class Parser:

    def tables(self,line):
        key, value = line.split(":")
        print('INSERT INTO' +value , end="")

    def columns(self, line):
        pairs = dict(item.split(":") for item in line.split(","))
        self.typelist = list(pairs.values())
        collist = list(pairs.keys())
        columns = ", ".join(collist[1:])
        print('('+ columns +')  VALUES')

    def values(self, line):
        line = line.strip()
        dlist = line.split(",")
        zipped = zip(self.typelist[1:],dlist)
        data = dict(zipped)
        mylist = []
        if line != "":
            print("(",end="")
            for k,v in data.items():
                if k.strip() == "int" or k.strip() == "boolean":
                    mylist.append(v.strip(';'))
                else:
                    mylist.append("'" +v.strip(';') + "'")
            if not re.match(".*;.*", line):
                print(",".join(mylist)+ "),")
            else:
                print(",".join(mylist)+ ")")
        else:
            print('\n' , end="")


with open('sample.csv') as file:
    p = Parser()
    for line in file:
        if re.match(".*table.*",line):
            p.tables(line)
        elif re.match (".*columns.*",line):
            p.columns(line)
        else:
            p.values(line)
