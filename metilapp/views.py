from .validators import validate_comp_if_pattern, validate_pos_in_compl_pat, validate_pos_in_pattern
from .forms import MetilForm
from .functions import delete_file, handle_uploaded_file, input_builder, methyl_type_stadistics, read_fasta, read_file_gff, read_gene_gff, met_in_genes
from django.shortcuts import render

def main_page(request):
    validation=""
    message=""

    if request.method=='POST':
        form = MetilForm(request.POST, request.FILES)
        validation = validate_pos_in_pattern(form) + validate_pos_in_compl_pat(form) + validate_comp_if_pattern(form)
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

            data_fasta = read_fasta('metilapp/'+g.name, data_gff, patterns)

            delete_file(f)
            delete_file(gene)

            return render(request,'metilapp/result.html', {'message': message, 'patterns': patterns.items(), 'met_name': f.name, 'fasta_name': g.name, 'gene_name': gene.name,
             'prom': form.data['prom'], 'jobID': jobID, 'total_m': base_sts[0], 'chrom_m': base_sts[1], 'index_pat': data_fasta[0].items(), 'pat_status': data_fasta[1][0], 
                'num_st': data_fasta[1][1], 'metGen': data_metGen[0], 'metProm': data_metGen[1], 'genMets': data_metGen[2], 'promMets': data_metGen[3]})
        else:
            message = form.errors
    form = MetilForm()
    return render(request,'metilapp/main_page.html', {'form': form,'message': message, 'val': validation})