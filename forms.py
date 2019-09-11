from django import forms



class RedirectToUni(forms.Form):
    UniName = forms.CharField(label="Enter University/College Name: ",required=True)
