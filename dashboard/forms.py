from django import forms

class PhotoForm(forms.Form):
    photoData = forms.CharField(widget=forms.HiddenInput())
