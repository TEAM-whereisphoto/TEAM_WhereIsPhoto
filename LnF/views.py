from django.http import JsonResponse
from django.shortcuts import render
from pytz import timezone
from .models import *
from map.models import Booth
from brand.models import Brand



def list(request):
    brands = Brand.objects.all()
    query = request.GET.get('query', '')
    tag= request.GET.get('tag', '')

    if query:
        booths = Booth.objects.filter(name__icontains = query)
        posts = LnF_Post.objects.filter(booth__in = booths).order_by('-time')
        if tag:
            posts = posts.filter(tag=tag)
    
    else:
        posts=LnF_Post.objects.all().order_by('-time')
        if tag:
            posts = posts.filter(tag=tag)
    ctx = {'posts': posts, 'brands':brands}
    return render(request, 'LnF/list.html', context=ctx)

