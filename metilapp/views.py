from .validators import validate_comp_if_pattern, validate_pos_in_compl_pat, validate_pos_in_pattern
from .forms import MetilForm
from .functions import delete_file, handle_uploaded_file, methyl_type_stadistics, read_file_gff
from django.shortcuts import render

# Create your views here.

def main_page(request):
    validation=""
    message=""

    if request.method=='POST':
        form = MetilForm(request.POST, request.FILES)
        validation=validate_pos_in_pattern(form) + validate_pos_in_compl_pat(form) + validate_comp_if_pattern(form)
        if form.is_valid() and validation=="":
            f=request.FILES['m_out']
            jobID = f.name
            if form.data['job_ID']:
                jobID = form.data['job_ID']
            handle_uploaded_file(f)
            data_gff = read_file_gff('metilapp/'+f.name)
            base_sts = methyl_type_stadistics(data_gff)
            delete_file(f)
            return render(request,'metilapp/result.html', {'message': message, 'total_m': base_sts[0], 'chrom_m': base_sts[1], 'jobID': jobID})
        else:
            message = form.errors
    form = MetilForm()
    return render(request,'metilapp/main_page.html', {'form': form,'message': message, 'val': validation})