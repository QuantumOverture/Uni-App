from django import forms
from MainApp.models import UniComment


class RedirectToUni(forms.Form):
    UniName = forms.CharField(label="Enter University/College Name: ",required=True)

CHOICES = [(1,'1 Star'),
           (2,'2 Star'),
           (3,'3 Star'),
           (4,'4 Star'),
           (5,'5 Star'),]
class UserReview(forms.ModelForm):
    StarRating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = UniComment
        fields = ['Comment','StarRating']
