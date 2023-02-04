from .validators import validate_comp_if_pattern, validate_one_patt, validate_pos_in_compl_pat, validate_pos_in_pattern, validate_one_patt
from .forms import MetilForm
from .functions import delete_file, handle_uploaded_file, input_builder, methyl_type_stadistics, read_fasta, read_file_gff, read_gene_gff, met_in_genes
from django.shortcuts import render
import io
import xlsxwriter
from django.http import FileResponse

def main_page(request):
    validation=""
    message=""

    if request.method=='POST':
        form = MetilForm(request.POST, request.FILES)
        validation = validate_pos_in_pattern(form) + validate_pos_in_compl_pat(form) + validate_comp_if_pattern(form) + validate_one_patt(form)
        if form.is_valid() and validation=="":
            f=request.FILES['m_out']
            g=request.FILES['genome']
            gene=request.FILES['gene']

            jobID = f.name
            if form.data['job_ID']:
                jobID = form.data['job_ID']

            patterns = input_builder(form)
            
            handle_uploaded_file(f)
            handle_uploaded_file(g)
            handle_uploaded_file(gene)

            data_gff = read_file_gff('metilapp/'+f.name)
            base_sts = methyl_type_stadistics(data_gff)

            gene_gff = read_gene_gff('metilapp/'+gene.name, form.data['prom'])
            data_metGen = met_in_genes(data_gff, gene_gff)

            data_fasta = read_fasta('metilapp/'+g.name, data_gff, patterns, data_metGen[0], data_metGen[1])

            validation = delete_file(f) + delete_file(gene)

            if "web" in request.POST:    
                if validation != "":
                    form = MetilForm()
                    return render(request,'metilapp/main_page.html', {'form': form,'message': message, 'val': validation})
                else:
                    return render(request,'metilapp/result.html', {'message': message, 'patterns': patterns.items(), 'met_name': f.name, 'fasta_name': g.name, 'gene_name': gene.name,
                    'prom': form.data['prom'], 'jobID': jobID, 'total_m': base_sts[0], 'chrom_m': base_sts[1], 'index_pat': data_fasta[0].items(), 'pat_status': data_fasta[1][0], 
                    'num_st': data_fasta[1][1], 'metGen': data_metGen[0], 'metProm': data_metGen[1], 'genMets': data_metGen[2].items(), 'promMets': data_metGen[3].items(),
                    'pattGen': data_fasta[2], 'pattProm': data_fasta[3]})
            elif "excel" in request.POST:
                if validation != "":
                    form = MetilForm()
                    return render(request,'metilapp/main_page.html', {'form': form,'message': message, 'val': validation})
                else:
                    buffer = io.BytesIO()
                    workbook = xlsxwriter.Workbook(buffer)

                    # General summary
                    worksheet = workbook.add_worksheet('General summary')
                    f_ID = workbook.add_format({'bold': True, 'font_size': 20})
                    worksheet.write('A1', jobID, f_ID)
                    
                    f_titulos = workbook.add_format({'bold': True, 'right':True})
                    worksheet.write('A2', 'SMRT Methylation Output (.gff)', f_titulos)
                    worksheet.write('B2', f.name)
                    worksheet.write('A3', 'Genome file (.fasta)', f_titulos)
                    worksheet.write('B3', g.name)
                    worksheet.write('A4', 'Genome anotation file (.gff)', f_titulos)
                    worksheet.write('B4', gene.name)
                    
                    i=6
                    table = ''
                    for chrom, value in base_sts[1]:
                        v=list(value)
                        table = 'A'+str(i)+':'+'B'+str(i+len(v))
                        worksheet.add_table(table, {'data': v,
                                'columns': [{'header': chrom},
                                            {'header': 'Count'},
                                            ]})
                        i=i+4

                    table = 'A'+str(i)+':'+'B'+str(i+len(base_sts[0]))
                    worksheet.add_table(table, {'data': list(base_sts[0]),
                                'columns': [{'header': 'Methylation'},
                                {'header': 'Total'},
                                ]})
                    worksheet.autofit()

                    # Genome pattern distribution
                    sheet2 = workbook.add_worksheet('Genome pattern distribution')
                    i=1
                    table = 'A'+str(i)+':A'+str(i+len(patterns.items()))
                    v=list(patterns.items())
                    pat=[]
                    poss = []
                    for pattern in v:
                        pat.append(pattern)
                        poss.append(pattern[1])

                    sheet2.add_table(table, {'data': pat,
                                'columns': [{'header': 'Patterns-Complementary'},
                                            ]})
                    table = 'B'+str(i)+':C'+str(i+len(patterns.items()))
                    sheet2.add_table(table, {'data': poss,
                                'columns': [{'header': 'Position'},
                                            {'header': 'Complementary position'},
                                            ]})

                    i=i+len(patterns.items())+2
                    table = 'A'+str(i)+':'+'K'+str(i+len(data_fasta[1][1]))
                    met_count = list()
                    for aux in data_fasta[1][1]:
                        order = [0,10,5,1,6,2,7,3,8,4,9]
                        v=[aux[j] for j in order]
                        met_count.append(v)
                    sheet2.add_table(table, {'data': met_count,
                                'columns': [{'header': 'Chromosome'},
                                            {'header': 'Pattern'},
                                            {'header': 'Total matches'},
                                            {'header': 'M_M'},
                                            {'header': '% MM'},
                                            {'header': 'M_N'},
                                            {'header': '% MN'},
                                            {'header': 'N_M'},
                                            {'header': '% NM'},
                                            {'header': 'N_N'},
                                            {'header': '% NN'},
                                            ]})
                    sheet2.autofit()
                    
                    # Methylation status
                    sheet3 = workbook.add_worksheet('Methylation status')
                    i=1
                    table = 'A'+str(i)+':'+'U'+str(i+len(data_fasta[1][0]))
                    met_count = list()
                    for aux in data_fasta[1][0]:
                        order = [0,1,6,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
                        v=[aux[j] for j in order]
                        met_count.append(v)
                    
                    sheet3.add_table(table, {'data': met_count,
                                'columns': [{'header': 'Chromosome'},
                                            {'header': 'Pattern'},
                                            {'header': 'Methylation'},
                                            {'header': 'Starting coordenate'},
                                            {'header': 'Putative coor. in W'},
                                            {'header': 'Putative coor. in C'},
                                            {'header': 'Status'},
                                            {'header': 'Score coor. W'},
                                            {'header': 'Coverage W'},
                                            {'header': 'IPDRatio W'},
                                            {'header': 'Frac. W'},
                                            {'header': 'Frac. low W'},
                                            {'header': 'Frac. up W'},
                                            {'header': 'IdentificationQv W'},
                                            {'header': 'Score coor. C'},
                                            {'header': 'Coverage C'},
                                            {'header': 'IPDRatio C'},
                                            {'header': 'Frac. C'},
                                            {'header': 'Frac. low C'},
                                            {'header': 'Frac. up C'},
                                            {'header': 'IdentificationQv C'},
                                            ]})
                    sheet3.autofit()

                    # Methylation in genes
                    sheet4 = workbook.add_worksheet('Methylations in genes')
                    i=1
                    table = 'A'+str(i)+':'+'L'+str(i+len(data_metGen[0]))
                    sheet4.add_table(table, {'data': data_metGen[0],
                                'columns': [{'header': 'Chromosome'},
                                            {'header': 'Accession number'},
                                            {'header': 'Gene'},
                                            {'header': 'Description'},
                                            {'header': 'Feature'},
                                            {'header': 'Start'},
                                            {'header': 'End'},
                                            {'header': 'Strand'},
                                            {'header': 'm4C'},
                                            {'header': 'm6A'},
                                            {'header': 'm5C'},
                                            {'header': 'Total'},
                                            ]})
                    sheet4.autofit()

                    # Methylations in promoters
                    sheet5 = workbook.add_worksheet('Methylations in promoters')
                    i=1
                    table = 'A'+str(i)+':'+'L'+str(i+len(data_metGen[1]))
                    sheet5.add_table(table, {'data': data_metGen[1],
                                'columns': [{'header': 'Chromosome'},
                                            {'header': 'Accession number'},
                                            {'header': 'Gene'},
                                            {'header': 'Description'},
                                            {'header': 'Feature'},
                                            {'header': 'Start'},
                                            {'header': 'End'},
                                            {'header': 'Strand'},
                                            {'header': 'm4C'},
                                            {'header': 'm6A'},
                                            {'header': 'm5C'},
                                            {'header': 'Total'},
                                            ]})
                    sheet5.autofit()

                    # Methylations gene distribution
                    sheet6 = workbook.add_worksheet('Methylations gene distribution')
                    v=list()
                    for j, k in data_metGen[2].items():
                        v.append(k)
                    i=1
                    table = 'A'+str(i)+':'+'R'+str(i+len(v))
                    sheet6.add_table(table, {'data': v,
                                'columns': [{'header': 'Chromosome'},
                                            {'header': 'Met. type'},
                                            {'header': 'Coor. met.'},
                                            {'header': 'Feature'},
                                            {'header': 'Gene'},
                                            {'header': 'Description'},
                                            {'header': 'Start'},
                                            {'header': 'End'},
                                            {'header': 'Gene strand'},
                                            {'header': 'Met. strand'},
                                            {'header': 'Accession number'},
                                            {'header': 'Score'},
                                            {'header': 'Coverage'},
                                            {'header': 'IPDRatio'},
                                            {'header': 'Frac.'},
                                            {'header': 'Frac. low'},
                                            {'header': 'Frac. up'},
                                            {'header': 'IdentificationQv'},
                                            ]})
                    sheet6.autofit()

                    # Methylations promoter distribution
                    sheet7 = workbook.add_worksheet('Methyl. promoter distribution')
                    v=list()
                    for j, k in data_metGen[3].items():
                        v.append(k)
                    i=1
                    table = 'A'+str(i)+':'+'R'+str(i+len(v))
                    sheet7.add_table(table, {'data': v,
                                'columns': [{'header': 'Chromosome'},
                                            {'header': 'Met. type'},
                                            {'header': 'Coor. met.'},
                                            {'header': 'Feature'},
                                            {'header': 'Gene'},
                                            {'header': 'Description'},
                                            {'header': 'Start'},
                                            {'header': 'End'},
                                            {'header': 'Gene strand'},
                                            {'header': 'Met. strand'},
                                            {'header': 'Accession number'},
                                            {'header': 'Score'},
                                            {'header': 'Coverage'},
                                            {'header': 'IPDRatio'},
                                            {'header': 'Frac.'},
                                            {'header': 'Frac. low'},
                                            {'header': 'Frac. up'},
                                            {'header': 'IdentificationQv'},
                                            ]})
                    sheet7.autofit()

                    # Patterns in genes
                    sheet8 = workbook.add_worksheet('Patterns in genes')
                    v=list()
                    w = list()
                    for j, k in data_fasta[2][0][9]:
                        v.append(j)
                    for j in data_fasta[2]:
                        w.append(list(j[9]))
                    # Crear número de lista en base a patrones, encapsular todas del mismo tipo juntos.
                    tab_mt=dict()
                    for aux in v:
                        tab_mt[aux] = list()
                    for aux in w:
                        for h in aux:
                            aux2 = list()
                            aux2.append(h[0])
                            for jj in h[1]:
                                aux2.append(jj)
                            if tab_mt.get(h[0]) == None:
                                tab_mt[h[0]] = aux2
                            else:    
                                tab_mt[h[0]].append(aux2)
                        
                    i=1
                    table = 'A'+str(i)+':'+'I'+str(i+len(data_fasta[2]))
                    sheet8.add_table(table, {'data': data_fasta[2],
                                'columns': [{'header': 'Chromosome'},
                                            {'header': 'Feature'},
                                            {'header': 'Accession number'},
                                            {'header': 'Gene'},
                                            {'header': 'Description'},
                                            {'header': 'Start'},
                                            {'header': 'End'},
                                            {'header': 'Strand'},
                                            {'header': 'Total'},
                                            ]})
                    i=9
                    for j in v:
                        sheet8.add_table(0,i,len(data_fasta[2]),i+4, {'data': tab_mt[j], 'first_column': True,
                                'columns': [{'header': j},
                                            {'header': 'M_M'},
                                            {'header': 'M_N'},
                                            {'header': 'N_M'},
                                            {'header': 'N_N'},
                                            ]})
                        i=i+5
                    sheet8.autofit()

                    # Patterns in promoters
                    sheet9 = workbook.add_worksheet('Patterns in promoters')
                    v=list()
                    w = list()
                    for j, k in data_fasta[3][0][9]:
                        v.append(j)
                    for j in data_fasta[3]:
                        w.append(list(j[9]))
                    # Crear número de lista en base a patrones, encapsular todas del mismo tipo juntos.
                    tab_mt=dict()
                    for aux in v:
                        tab_mt[aux] = list()
                    for aux in w:
                        for h in aux:
                            aux2 = list()
                            aux2.append(h[0])
                            for jj in h[1]:
                                aux2.append(jj)
                            if tab_mt.get(h[0]) == None:
                                tab_mt[h[0]] = aux2
                            else:    
                                tab_mt[h[0]].append(aux2)
                        
                    i=1
                    table = 'A'+str(i)+':'+'I'+str(i+len(data_fasta[3]))
                    sheet9.add_table(table, {'data': data_fasta[3],
                                'columns': [{'header': 'Chromosome'},
                                            {'header': 'Feature'},
                                            {'header': 'Accession number'},
                                            {'header': 'Gene'},
                                            {'header': 'Description'},
                                            {'header': 'Start'},
                                            {'header': 'End'},
                                            {'header': 'Strand'},
                                            {'header': 'Total'},
                                            ]})
                    i=9
                    for j in v:
                        sheet9.add_table(0,i,len(data_fasta[3]),i+4, {'data': tab_mt[j], 'first_column': True,
                                'columns': [{'header': j},
                                            {'header': 'M_M'},
                                            {'header': 'M_N'},
                                            {'header': 'N_M'},
                                            {'header': 'N_N'},
                                            ]})
                        i=i+5
                    sheet9.autofit()
                    
                    workbook.close()
                    buffer.seek(0)

                    return FileResponse(buffer, as_attachment=True, filename='methylappRes.xlsx')
        else:
            message = form.errors
    form = MetilForm()
    return render(request,'metilapp/main_page.html', {'form': form,'message': message, 'val': validation})