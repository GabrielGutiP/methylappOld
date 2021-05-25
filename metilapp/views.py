from django.shortcuts import render
from metilapp.forms import MetilForm
from metilapp.functions import delete_file, handle_uploaded_file

# Create your views here.

def main_page(request):
    message=""
    if request.method=='POST':
        form = MetilForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            handle_uploaded_file(f) 
            delete_file(f)
            message = "Everything worked as intended"
            return render(request,'metilapp/result.html', {'message': message})
        else:
            message = form.errors
    form = MetilForm()
    return render(request,'metilapp/main_page.html', {'form': form,'message': message})