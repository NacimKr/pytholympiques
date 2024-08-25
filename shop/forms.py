from django import forms

class UserForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    
    
class ProductForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    image = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))