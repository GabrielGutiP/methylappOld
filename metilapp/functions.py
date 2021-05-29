import os
import csv

def handle_uploaded_file(f):  
    with open('./metilapp/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def delete_file(f):
    if os.path.exists('./metilapp/upload/'+f.name):
        os.remove('metilapp/upload/'+f.name)
    else:
        print(f+"does not exist")  

def read_file_gff(f_name):
    result = []
    with open(f_name, 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        for row in reader:
            if not row[0].startswith('#'):
                aux = [row[0].split()[0], row[2], row[3], row[6], row[8].split(";")[1].split("=")[1]]
                result.append(aux)
    file.close()
    return result