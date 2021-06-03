from .validators import validate_comp_if_pattern, validate_pos_in_compl_pat, validate_pos_in_pattern
from .forms import MetilForm
from .functions import delete_fasta, delete_file, handle_uploaded_file, input_builder, methyl_type_stadistics, patterns_in_genome, read_fasta, read_file_gff
from django.shortcuts import render

def main_page(request):
    validation=""
    message=""

    if request.method=='POST':
        form = MetilForm(request.POST, request.FILES)
        validation=validate_pos_in_pattern(form) + validate_pos_in_compl_pat(form) + validate_comp_if_pattern(form)
        if form.is_valid() and validation=="":
            f=request.FILES['m_out']
            g=request.FILES['genome']

            jobID = f.name
            if form.data['job_ID']:
                jobID = form.data['job_ID']

            patterns = input_builder(form)
            
            handle_uploaded_file(f)
            handle_uploaded_file(g)

            data_gff = read_file_gff('metilapp/'+f.name)
            base_sts = methyl_type_stadistics(data_gff)

            data_fasta = read_fasta('metilapp/'+g.name, patterns[0], patterns[1])

            delete_file(f)

            return render(request,'metilapp/result.html', {'message': message, 'met_name': f.name, 'fasta_name': g.name, 'jobID': jobID, 'total_m': base_sts[0], 'chrom_m': base_sts[1], 
                    'index_pat': data_fasta[0], 'index_compl_pat': data_fasta[1]})
        else:
            message = form.errors
    form = MetilForm()
    return render(request,'metilapp/main_page.html', {'form': form,'message': message, 'val': validation})