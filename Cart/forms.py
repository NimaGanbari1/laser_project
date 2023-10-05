# Django
from django import forms


class EditCartForm(forms.Form):
    count = forms.IntegerField()
    code = forms.IntegerField()


class FinalAddresForm(forms.Form):
    Address = forms.CharField(widget=forms.Textarea)
