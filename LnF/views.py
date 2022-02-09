from django.shortcuts import render
from .models import *
from map.models import Booth
# Create your views here.


def list(request):
    posts=LnF_Post.objects.all()
    query = request.GET.get('query', '')
    if query:
        booths = Booth.objects.filter(name__icontains = query)
        posts = LnF_Post.objects.filter(booth__in = booths)
            
    ctx = {'posts': posts}
    return render(request, 'LnF/list.html', context=ctx)