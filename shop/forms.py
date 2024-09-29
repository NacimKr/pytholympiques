from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Product


# class UserForm(forms.Form):
#     subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
#     message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
#     sender = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
#     cc_myself = forms.BooleanField(required=False)
    
class UserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class' : 'form-control'}))
    password1 = forms.EmailField(widget=forms.PasswordInput(
        attrs={'class' : 'form-control'}))
    password2 = forms.EmailField(widget=forms.PasswordInput(
        attrs={'class' : 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )

    
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title","price","description","image","quantity"]
        
    # title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    # price = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    # image = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    # quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))