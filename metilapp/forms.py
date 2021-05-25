# -*- encoding: utf-8 -*-
from django import forms
from metilapp.validators import validate_file_extension

class MetilForm(forms.Form):
     file = forms.FileField(validators=[validate_file_extension])