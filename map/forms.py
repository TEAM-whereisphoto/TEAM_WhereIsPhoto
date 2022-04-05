from django import forms
from .models import Review
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        
        fields = ('tag', 'color', 'content', 'img')

    def checkstar(self, request):
        if (request.get('rating')==None):
            self.errors["Rate"]= "\n필수 항목입니다."
