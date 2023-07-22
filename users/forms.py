from django import forms

class RegisterFrom(forms.Form):
    phonemail = forms.CharField()

class createUserForm(forms.Form):
    phonemail = forms.CharField()
    code = forms.CharField()
    password = forms.CharField()
    
class UserLoginForm(forms.Form):
    phonemail = forms.CharField()
    password = forms.CharField() 