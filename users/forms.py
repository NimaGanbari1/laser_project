from django import forms
from products.models import Product
class RegisterFrom(forms.Form):
    phonemail = forms.CharField()

class createUserForm(forms.Form):
    phonemail = forms.CharField()
    code = forms.CharField()
    password = forms.CharField()
    
class UserLoginForm(forms.Form):
    phonemail = forms.CharField()
    password = forms.CharField() 
    
class EditCartForm(forms.Form):
    count = forms.IntegerField()
    code = forms.IntegerField()
    
class FinalAddresForm(forms.Form):
    Address = forms.CharField()