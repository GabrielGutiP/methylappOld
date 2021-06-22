# -*- encoding: utf-8 -*-
from django import forms
from django.forms.fields import IntegerField
from .validators import validate_smrt_extension, validate_gene_extension, validate_genome_extension, validate_pat_IUPAC, validate_pos_compl, validate_pos_pat

class MetilForm(forms.Form):
     m_out = forms.FileField(label="SMRT Methylation Output (.gff)", validators=[validate_smrt_extension])
     genome = forms.FileField(label="Genome file Fasta Format (.fasta)", validators=[validate_genome_extension])
     gene = forms.FileField(label="Genome annotation file (.gff)", validators=[validate_gene_extension])
     job_ID = forms.CharField(label="Job ID" , required=False)

     prom = forms.IntegerField(label="Promoter region", validators=[validate_pos_compl])

     patron1 = forms.CharField(label="Pattern 1", required=False, validators=[validate_pat_IUPAC])
     pos_pat1 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_pat])
     compl_pat1 = forms.CharField(label="Complementary of Pattern 1", required=False, validators=[validate_pat_IUPAC])
     pos_compl_pat1 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_compl])

     patron2 = forms.CharField(label="Pattern 2", required=False, validators=[validate_pat_IUPAC])
     pos_pat2 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_pat])
     compl_pat2 = forms.CharField(label="Complementary of Pattern 2", required=False, validators=[validate_pat_IUPAC])
     pos_compl_pat2 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_compl])

     patron3 = forms.CharField(label="Pattern 3", required=False, validators=[validate_pat_IUPAC])
     pos_pat3 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_pat])
     compl_pat3 = forms.CharField(label="Complementary of Pattern 3", required=False, validators=[validate_pat_IUPAC])
     pos_compl_pat3 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_compl])

     patron4 = forms.CharField(label="Pattern 4", required=False, validators=[validate_pat_IUPAC])
     pos_pat4 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_pat])
     compl_pat4 = forms.CharField(label="Complementary of Pattern 4", required=False, validators=[validate_pat_IUPAC])
     pos_compl_pat4 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_compl])

     patron5 = forms.CharField(label="Pattern 5", required=False, validators=[validate_pat_IUPAC])
     pos_pat5 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_pat])
     compl_pat5 = forms.CharField(label="Complementary of Pattern 5", required=False, validators=[validate_pat_IUPAC])
     pos_compl_pat5 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_compl])

     patron6 = forms.CharField(label="Pattern 6", required=False, validators=[validate_pat_IUPAC])
     pos_pat6 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_pat])
     compl_pat6 = forms.CharField(label="Complementary of Pattern 6", required=False, validators=[validate_pat_IUPAC])
     pos_compl_pat6 = forms.IntegerField(label="Methylate base position", required=False, validators=[validate_pos_compl])
