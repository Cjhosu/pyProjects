people_ages = {  'Caleb': 34, 'Ryan': 33, 'Lauren': 31 ,'Jessi': 36 }

def findyoungest(age_dict):
    youngest = None
    for person in age_dict:
        if youngest == None:
            youngest = person
        elif age_dict[person] < age_dict[youngest]:
            youngest = person
        else: 
            continue
    print(youngest)

findyoungest(people_ages)
