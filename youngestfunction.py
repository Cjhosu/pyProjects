bears = { "caleb":33, "lauren":31, "jessi":36, "alastair":1, "ryan":32, }

def findyoungest(age_dict):
    youngest = None
    for x in age_dict:
        if youngest == None:
            youngest = x
        elif age_dict[x] < age_dict[youngest]:
            youngest = x
        else:
            continue
    print(youngest)

findyoungest(bears)
