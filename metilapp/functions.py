import os

def handle_uploaded_file(f):  
    with open('metilapp/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def delete_file(f):
    if os.path.exists('metilapp/upload/'+f.name):
        os.remove('metilapp/upload/'+f.name)
    else:
        print(f+"does not exist")  