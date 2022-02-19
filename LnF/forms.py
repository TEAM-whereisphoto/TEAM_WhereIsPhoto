from django import forms
from django.contrib.auth.models import User
from .models import *


class PostForm(forms.ModelForm):
    tag = forms.ChoiceField(widget=forms.RadioSelect, choices=TAG_CHOICE)

    class Meta:
        model = LnF_Post
        fields = ('tag', 'content', 'img')

        widgets = {
          'content': forms.Textarea(attrs={
              'rows':10, 'cols':20
              }),
        }

        # labels = {
        #     'tag' : '',
        #     'content': '',
        #     'img' : '',
        # }