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

def read_gene_gff(f_name, prom):
    result = []
    with open(f_name, 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        for row in reader:
            if not row[0].startswith('#'):
                if row[2] in ["CDS","rRNA","tRNA"]:
                    aux_r = []
                    for r in row[8].split(";"):
                        if r.startswith('ID'):
                            aux_r.append(r.split("=")[1].split("-")[1])
                        elif r.startswith('Parent'):
                            aux_r.append(r.replace("Parent=gene-", ""))
                        elif r.startswith('product'):
                            aux_r.append(r.split("=")[1])
                    if row[6]=="+":
                        aux = [row[0], row[2], [int(row[3]), int(row[4])], [int(row[3])-1-int(prom), int(row[3])-1], row[6], aux_r]  # Cromosoma, gen, rango gen, rango promotor, cadena y descripcion
                    else:
                        aux = [row[0], row[2], [int(row[3]), int(row[4])], [int(row[4])+1, int(row[4])+1+int(prom)], row[6], aux_r]
                    result.append(aux)
    file.close()
    return result

def read_fasta(f_name, data_gff, complete_pat, met_gen, met_prom):
    fasta = Fasta(f_name)
    result = patterns_in_genome(fasta, complete_pat)
    result_met = met_pat_opt(data_gff, result)
    patt_gen = patterns_in_genes(met_gen, met_prom, result_met[0])
    fasta.close()
    delete_fasta(f_name)
    return result, result_met , patt_gen[0], patt_gen[1]

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
            result.append([i[0], i[1], s+1, pos_posit, pos_neg, aux, t_met])    # Cromosoma|Patron completo|Inicio de patrón|Posible + met|Posible - met|Estado|Tipo met
        num_st.append([i[0], c_MM, c_MN, c_NM, c_NN, i[3], round(100*(int(c_MM)/int(i[3])), 2), round(100*(int(c_MN)/int(i[3])), 2), round(100*(int(c_NM)/int(i[3])), 2), 
            round(100*(int(c_NN)/int(i[3])), 2), i[1]])
    return result, num_st

def met_in_genes(gff, gene):
    # Mostrar Cromosoma|Accession number|Parent|Product|Tipo gen|Coor. inicio|Coor. final|Cadena|Tipos de metilaciones(m4C, m6A...)|Total
    met_gen = []
    metGen = dict() #Cromosoma|Tipo met|Coor met|Tipo gen|Parent|Description|Coor. inicio|Coor. final|Cadena gen|Cadena met
    met_prom = []
    prom = dict()
    for g in gene:
        met = dict()
        metP = dict()
        for row in gff:
            if row[0]==g[0]:
                if int(g[2][0]) <= int(row[2]) <= int(g[2][1]):
                    met[row[2]] = row[1]
                    if not row[0]+"-"+str(row[2]) in metGen.keys() or metGen[row[0]+"-"+str(row[2])][3] == "NA":
                        metGen[row[0]+"-"+str(row[2])] = [row[0], row[1], row[2], g[1], g[5][1], g[5][2], g[2][0], g[2][1], g[4], row[3], g[5][0]]
                else:
                    if not row[0]+"-"+str(row[2]) in metGen.keys():
                        metGen[row[0]+"-"+str(row[2])] = [row[0], row[1], row[2], "NA", "NA", "NA", "NA", "NA", "NA", row[3], g[5][0]]
                if int(g[3][0]) <= int(row[2]) <= int(g[3][1]):
                    metP[row[2]] = row[1]
                    if not row[0]+"-"+str(row[2]) in prom.keys() or prom[row[0]+"-"+str(row[2])][3] == "NA":
                        prom[row[0]+"-"+str(row[2])] = [row[0], row[1], row[2], g[1], g[5][1], g[5][2], g[3][0], g[3][1], g[4], row[3], g[5][0]]
                else:
                    if not row[0]+"-"+str(row[2]) in prom.keys():
                        prom[row[0]+"-"+str(row[2])] = [row[0], row[1], row[2], "NA", "NA", "NA", "NA", "NA", "NA", row[3], g[5][0]]
        aux = Counter(met.values())
        aux_p = Counter(metP.values())
        met_gen.append([g[0], g[5][0], g[5][1], g[5][2], g[1], g[2][0], g[2][1], g[4], aux["m4C"], aux["m6A"], aux["m5C"], len(met.keys())])
        met_prom.append([g[0], g[5][0], g[5][1], g[5][2], g[1], g[3][0], g[3][1], g[4], aux_p["m4C"], aux_p["m6A"], aux_p["m5C"], len(metP.keys())])
    return met_gen, met_prom, metGen, prom

def patterns_in_genes(met_gen, met_prom, patt):
    # patt : Cromosoma|Patron completo|Inicio de patrón|Posible + met|Posible - met|Estado|Tipo met
    # met_gen/met_prom : Cromosoma|Accession number|Parent|Product|Tipo gen|Coor. inicio|Coor. final|Cadena|Tipos de metilaciones(m4C, m6A...)|Total
    pat_gen = []    # Cromosoma|Tipo gen|Accession number|Parent|Description|Coor. init|Coor. fin|Cadena|Patron|MM|MN|NM|NN|... 
    pat_prom = []
    for g in met_gen:
        dicc = dict()
        stat = dict()
        total = 0
        for met in patt:
            if met[0]==g[0]:
                if not met[1] in dicc.keys():
                    stat[met[1]+'M_M'] = 0
                    stat[met[1]+'M_N'] = 0
                    stat[met[1]+'N_M'] = 0
                    stat[met[1]+'N_N'] = 0
                    dicc[met[1]] = [stat[met[1]+'M_M'],stat[met[1]+'M_N'],stat[met[1]+'N_M'],stat[met[1]+'N_N']]
                m = met[3]
                m1 = met[4]
                if m=="NA":
                    m = -1
                if m1=="NA":
                    m1 = -1
                if int(g[5])<=int(m)<=int(g[6]) or int(g[5])<=int(m1)<=int(g[6]):
                    total = total+1
                    if met[5] == 'M_M':
                        stat[met[1]+'M_M'] = stat[met[1]+'M_M']+1
                    elif met[5] == 'M_N':
                        stat[met[1]+'M_N'] = stat[met[1]+'M_N']+1
                    elif met[5] == 'N_M':
                        stat[met[1]+'N_M'] = stat[met[1]+'N_M']+1
                    elif met[5] == 'N_N':
                        stat[met[1]+'N_N'] = stat[met[1]+'N_N']+1
                    dicc[met[1]] = [stat[met[1]+'M_M'],stat[met[1]+'M_N'],stat[met[1]+'N_M'],stat[met[1]+'N_N']]
        pat_gen.append([g[0], g[4], g[1], g[2], g[3], g[5], g[6], g[7], total, Counter(dicc).items()])
    
    for g in met_prom:
        dicc = dict()
        stat = dict()
        total = 0
        for met in patt:
            if met[0]==g[0]:
                if not met[1] in dicc.keys():
                    stat[met[1]+'M_M'] = 0
                    stat[met[1]+'M_N'] = 0
                    stat[met[1]+'N_M'] = 0
                    stat[met[1]+'N_N'] = 0
                    dicc[met[1]] = [stat[met[1]+'M_M'],stat[met[1]+'M_N'],stat[met[1]+'N_M'],stat[met[1]+'N_N']]
                m = met[3]
                m1 = met[4]
                if m=="NA":
                    m = -1
                if m1=="NA":
                    m1 = -1
                if int(g[5])<=int(m)<=int(g[6]) or int(g[5])<=int(m1)<=int(g[6]):
                    total = total+1
                    if met[5] == 'M_M':
                        stat[met[1]+'M_M'] = stat[met[1]+'M_M']+1
                    elif met[5] == 'M_N':
                        stat[met[1]+'M_N'] = stat[met[1]+'M_N']+1
                    elif met[5] == 'N_M':
                        stat[met[1]+'N_M'] = stat[met[1]+'N_M']+1
                    elif met[5] == 'N_N':
                        stat[met[1]+'N_N'] = stat[met[1]+'N_N']+1
                    dicc[met[1]] = [stat[met[1]+'M_M'],stat[met[1]+'M_N'],stat[met[1]+'N_M'],stat[met[1]+'N_N']]
        pat_prom.append([g[0], g[4], g[1], g[2], g[3], g[5], g[6], g[7], total, Counter(dicc).items()])
    return pat_gen, pat_prom

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