from django import forms
from .models import Comment


class CreateCartForm(forms.Form):
    uniqeCode = forms.IntegerField()
    count = forms.IntegerField()
    user = forms.CharField()
    
class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["Product", "text"]
    