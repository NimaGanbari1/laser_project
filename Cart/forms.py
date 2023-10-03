from django import forms


class EditCartForm(forms.Form):
    count = forms.IntegerField()
    code = forms.IntegerField()