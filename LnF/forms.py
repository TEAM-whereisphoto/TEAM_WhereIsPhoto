from django import forms
from django.contrib.auth.models import User
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = LnF_Post
        fields = ('booth', 'title', '')