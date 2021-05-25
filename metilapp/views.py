from django.shortcuts import render
from metilapp.forms import MetilForm
from metilapp.functions import handle_uploaded_file

# Create your views here.

def main_page(request):
    message=""
    if request.method=='POST':
        form = MetilForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file']) 
            message = "Everything worked as intended"
            return render(request,'metilapp/result.html', {'message': message})
        else:
            message = form.errors
    form = MetilForm()
    return render(request,'metilapp/main_page.html', {'form': form,'message': message})