# -*- encoding: utf-8 -*-
from django import forms
from .validators import validate_file_extension

class MetilForm(forms.Form):
     file = forms.FileField(label="SMRT Methylation Output (.gff)", validators=[validate_file_extension])
     job_ID = forms.CharField(label="Job ID" , required=False)