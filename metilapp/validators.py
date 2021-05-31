import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.gff']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def validate_pos_pat(value):
    if value <= 0:
        raise ValidationError('Incorrect position.')

def validate_pos_compl(value):
    if value < 0:
        raise ValidationError('Incorrect value for position.')

def validate_pat_IUPAC(value):
    aux = "ACGTURYSWKMBDHVN"
    for i in value:
        if not i in aux:
            raise ValidationError('No IUPAC values in pattern.')

def validate_pos_in_pattern(form):
    i = 1
    while i <= 6:
        aux = 'pos_pat'+str(i)
        pat = 'patron'+str(i)
        if form.data[aux]:
            if len(form.data[pat])<int(form.data[aux]):
                message= message+'\nIncorrect position for pattern '+str(i)+'.'
        i=i+1
    return message

def validate_pos_in_compl_pat(form):
    message=""
    i = 1
    while i <= 6:
        aux = 'pos_compl_pat'+str(i)
        pat = 'compl_pat'+str(i)
        if form.data[aux]:
            if len(form.data[pat])<int(form.data[aux]):
                message= message+'\nIncorrect position for complementary pattern '+str(i)+'.'
        i=i+1
    return message

def validate_comp_if_pattern(form):
    message=""
    i = 1
    while i <= 6:
        aux = 'compl_pat'+str(i)
        pat = 'patron'+str(i)
        if form.data[aux] and not form.data[pat]: 
            message= message+'\nInvalid lone complementary pattern '+str(i)+'.'
        i=i+1
    return message