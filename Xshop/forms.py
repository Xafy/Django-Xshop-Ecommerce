from django import forms
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    fullname  = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', 'placeholder':'full name',}))
    email     = forms.EmailField(widget=forms.EmailInput(attrs= {'class':'form-control', 'placeholder':'your email',}))
    content   = forms.CharField(widget=forms.Textarea(attrs= {'class':'form-control', 'placeholder':'your content',}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("email has to be gmail")
        return email
    
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) < 5 :
            raise forms.ValidationError("content must be greater than 5 letters")
        return content


