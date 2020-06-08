import yaml
import re

regex = re.compile('cmm_pgsql::dblist.*')

def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

if __name__ == "__main__":
    filepath = "../../../repos/control/hieradata/app_env/production.yaml"
    data = yaml_loader(filepath)
    outerhash = data
    for cluster in outerhash.items():
        cluster_name = cluster[0]
        if re.match(regex, cluster_name):
            print(cluster_name)
            dbs = data.get(cluster_name)
            try:
                for db_name in dbs.items():
                    print('    '+db_name[0])
            except:
                print('NONE')
