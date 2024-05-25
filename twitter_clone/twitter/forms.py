from django import forms
from .models import Twitter


class TwitterForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   'placeholder': 'Enter Your Twitter',
                                   'class': 'form-control',
                               }
                           ),
                           label='',
                           )

    class Meta:
        model = Twitter
        exclude = ('user',)