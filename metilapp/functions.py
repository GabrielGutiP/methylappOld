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
        os.remove(f)
        os.remove(f+".fai")
    else:
        print(f+"does not exist")  

def read_file_gff(f_name):
    result = []
    with open(f_name, 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        for row in reader:
            if not row[0].startswith('#'):
                if row[2]!="modified_base":
                    aux = [row[0].split()[0], row[2], int(row[3]), row[6], row[8].split(";")[1].split("=")[1]]
                    result.append(aux)
    file.close()
    return result

def read_fasta(f_name, data_gff, complete_pat):
    fasta = Fasta(f_name)
    result = patterns_in_genome(fasta, complete_pat)
    result_met = met_pat_opt(data_gff, result)
    fasta.close()
    delete_fasta(f_name)
    return result, result_met

def methyl_type_stadistics(data):
    dic = dict()
    c = Counter([b[0] for b in data])
    for k in c.keys():
        aux = [x for x in data if x[0]==k]    # Filtrado de data por cromosoma
        dic[k]= Counter([b[1] for b in aux]).items()
    sol = Counter([b[1] for b in data]).items()
    return sol, dic.items()

def patterns_in_genome(data, complete_pat):
    index_complete = dict()
    i=0
    for c in data.keys():
        chrom = str(data[c][:].seq)
        for p in complete_pat.keys():
            aux_p = p.split("-")
            if len(aux_p)>1:
                seq_d = SeqUtils.nt_search(chrom, aux_p[0])
                seq_c = SeqUtils.nt_search(chrom, aux_p[1])
                index_complete[i] = [c , aux_p[0]+"-"+aux_p[1], seq_d[1:], len(seq_d)-1, complete_pat[p]]
                i = i+1
                index_complete[i] = [c , aux_p[1]+"-"+aux_p[0], seq_c[1:], len(seq_c)-1, complete_pat[p][::-1]] # Invertimos el orden de las posiciones de met para que encajen con el patrón
                i = i+1
            else:
                seq = SeqUtils.nt_search(chrom, aux_p[0])
                index_complete[i] = [c , aux_p[0], seq[1:], len(seq)-1, complete_pat[p][0]]
                i = i+1
    return index_complete

def met_pat_opt(gff, index_complete):
    result =  []
    met = dict()
    num_st = []
    for row in gff:
        met[row[2]]= row[1]
    for i in index_complete.values():
        c_MM = 0
        c_MN = 0
        c_NM = 0
        c_NN = 0
        for s in i[2]:
            aux_p = i[1].split("-")
            if len(aux_p)>1:
                pos_posit = s+int(i[4][0])
                pos_neg = s+1+len(aux_p[0])-int(i[4][1])
                if int(i[4][0])!=0 and pos_posit in met.keys():
                    t_met = met[pos_posit]                  # Tipo de metilación (m6A...)
                    aux = "M_"
                elif int(i[4][0])==0:
                    t_met = "None"
                    aux = "N_"
                    pos_posit = "NA"
                else:
                    t_met = "None"
                    aux = "N_"
                if int(i[4][1])!=0 and pos_neg in met.keys():
                    t_met = met[pos_neg]
                    aux = aux+"M"
                elif int(i[4][1])==0:
                    if t_met=="None":
                        t_met = "None"
                    aux = aux+"N"
                    pos_neg = "NA"
                else:
                    if t_met=="None":
                        t_met = "None"
                    aux = aux+"N"
            else:
                pos_posit = s+int(i[4])
                pos_neg = s+1+len(aux_p[0])-int(i[4])
                if pos_posit in met.keys():
                    t_met = met[pos_posit]
                    aux = "M_"
                else:
                    t_met = "None"
                    aux = "N_"
                if pos_neg in met.keys():
                    t_met = met[pos_neg]
                    aux = aux+"M"
                else:
                    t_met = "None"
                    aux = aux+"N"
            if aux=="M_M":
                c_MM = c_MM+1
            elif aux=="M_N":
                c_MN = c_MN+1
            elif aux=="N_M":
                c_NM = c_NM+1
            elif aux=="N_N":
                c_NN = c_NN+1
            result.append([i[0], i[1], s+1, pos_posit, pos_neg, aux, t_met])
        num_st.append([i[0], c_MM, c_MN, c_NM, c_NN, i[3], round(100*(int(c_MM)/int(i[3])), 2), round(100*(int(c_MN)/int(i[3])), 2), round(100*(int(c_NM)/int(i[3])), 2)
            , round(100*(int(c_NN)/int(i[3])), 2), i[1]])
    return result, num_st

def input_builder(form):
    complete_pat = dict()
    i = 1
    while i<=6:
        if form.data['patron'+str(i)] and form.data['compl_pat'+str(i)]:
            if form.data['patron'+str(i)] == form.data['compl_pat'+str(i)]:
                complete_pat[form.data['patron'+str(i)].strip()] = form.data['pos_pat'+str(i)]
            else:
                complete_pat[form.data['patron'+str(i)].strip()+"-"+form.data['compl_pat'+str(i)].strip()] = [form.data['pos_pat'+str(i)], form.data['pos_compl_pat'+str(i)]]
        i=i+1
    return complete_pat