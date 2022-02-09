from django.shortcuts import render
from .models import *
# Create your views here.


def list(request):
    posts=LnF_Post.objects.all()
    ctx = {'posts': posts}
    return render(request, 'LnF/list.html', context=ctx)