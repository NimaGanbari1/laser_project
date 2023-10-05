# ِDjango
from django import forms

# Third Party
from captcha.fields import CaptchaField

class RegisterFrom(forms.Form):
    phonemail = forms.CharField()
    
class createUserForm(forms.Form):
    phonemail = forms.CharField()
    code = forms.CharField()
    password = forms.CharField()
    captcha = CaptchaField()
    
class UserLoginForm(forms.Form):
    phonemail = forms.CharField()
    password = forms.CharField() 
    
class SetCodeForm(forms.Form):
    phonemail = forms.CharField()
    code = forms.CharField() 
    
    
class SetPassFrom(forms.Form):
    phonemail = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()  
  