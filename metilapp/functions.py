import os
import csv
from collections import Counter

def handle_uploaded_file(f):  
    with open('./metilapp/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def delete_file(f):
    if os.path.exists('./metilapp/'+f.name):
        os.remove('./metilapp/'+f.name)
    else:
        print(f+"does not exist")  

def read_file_gff(f_name):
    result = []
    with open(f_name, 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        for row in reader:
            if not row[0].startswith('#'):
                if row[2]!="modified_base":
                    aux = [row[0].split()[0], row[2], row[3], row[6], row[8].split(";")[1].split("=")[1]]
                    result.append(aux)
    file.close()
    return result

def methyl_type_stadistics(data):
    dic = dict()
    c = Counter([b[0] for b in data])
    for k in c.keys():
        aux = [x for x in data if x[0]==k]    # Filtrado de data por cromosoma
        dic[k]= Counter([b[1] for b in aux]).items()
    sol = Counter([b[1] for b in data]).items()
    return sol, dic.items()