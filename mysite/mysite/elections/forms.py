from django import forms

class PersonForm(forms.Form):
    area=forms.CharField(label="area", max_length=10)
    region=forms.CharField(label="area", max_length=10)