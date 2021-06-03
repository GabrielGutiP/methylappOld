import os
import csv
from collections import Counter
from pyfaidx import Fasta
from Bio import SeqUtils


def handle_uploaded_file(f):  
    with open('./metilapp/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def delete_file(f):
    if os.path.exists('./metilapp/'+f.name):
        os.remove('./metilapp/'+f.name)
    else:
        print(f+"does not exist")  

def delete_fasta(f):
    if os.path.exists(f):
        #f.close()
        os.remove(f+".fai")
        os.remove(f)
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

def read_fasta(f_name, patterns, compl_pats):
    fasta = Fasta(f_name)
    result = patterns_in_genome(fasta, patterns, compl_pats)
    fasta.close()
    delete_fasta(f_name)
    return result

def methyl_type_stadistics(data):
    dic = dict()
    c = Counter([b[0] for b in data])
    for k in c.keys():
        aux = [x for x in data if x[0]==k]    # Filtrado de data por cromosoma
        dic[k]= Counter([b[1] for b in aux]).items()
    sol = Counter([b[1] for b in data]).items()
    return sol, dic.items()

def patterns_in_genome(data, patterns, compl_pats):
    count_pat = dict()
    count_compl_pat = dict()
    index_pat = dict()
    index_compl_pat = dict()

    for c in data.keys():                                   # Busqueda de patrones en cada cromosoma
        dic_aux = dict()
        for p in patterns:
            chrom = str(data[c][:].seq)
            seq = SeqUtils.nt_search(chrom, p[0])           # Repetición del patrón con IUPAC en el cromosoma  
            dic_aux[p] = seq[1:]
            count_pat[c]= [p[0],len(seq)-1]                 # Conteo de repeticiones del patrón con el cromosoma
        index_pat[c]=dic_aux.items()
    
    for c in data.keys():                                   # Busqueda de patrones complementarios
        dic_aux = dict()
        for p in compl_pats:
            chrom = data[c][:].seq
            seq = SeqUtils.nt_search(chrom, p[0])           # Repetición del patrón con IUPAC en el cromosoma  
            dic_aux[p] = seq[1:]
            count_compl_pat[c]= [p[0],len(seq)-1]
        index_compl_pat[c]=dic_aux.items()
    return count_pat.items(), count_pat.items(), count_compl_pat.items(), count_compl_pat.items()

def input_builder(form):
    pat = dict()
    compl_pat = dict()
    i = 1
    while i<=6:
        if form.data['patron'+str(i)]:
            pat[form.data['patron'+str(i)]] = form.data['pos_pat'+str(i)]
        
        if form.data['compl_pat'+str(i)]:
            compl_pat[form.data['compl_pat'+str(i)]] = form.data['pos_compl_pat'+str(i)]
        i=i+1
    return pat.items(), compl_pat.items()