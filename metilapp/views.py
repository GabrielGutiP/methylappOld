from .forms import MetilForm
from .functions import delete_file, handle_uploaded_file, read_file_gff
from django.shortcuts import render

# Create your views here.

def main_page(request):
    message=""
    if request.method=='POST':
        form = MetilForm(request.POST, request.FILES)
        if form.is_valid():
            f=request.FILES['file']
            handle_uploaded_file(f)
            data_gff = read_file_gff('metilapp/upload/'+f.name)
            delete_file(f)
            message = "Everything worked as intended"
            return render(request,'metilapp/result.html', {'message': message, 'data': data_gff[5]})
        else:
            message = form.errors
    form = MetilForm()
    return render(request,'metilapp/main_page.html', {'form': form,'message': message})