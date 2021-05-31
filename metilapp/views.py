from .forms import MetilForm
from .functions import delete_file, handle_uploaded_file, methyl_type_stadistics, read_file_gff
from django.shortcuts import render

# Create your views here.

def main_page(request):
    message=""
    if request.method=='POST':
        form = MetilForm(request.POST, request.FILES)
        if form.is_valid():
            f=request.FILES['file']
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
    return render(request,'metilapp/main_page.html', {'form': form,'message': message})