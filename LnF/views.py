from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *

from map.models import Booth
from brand.models import Brand
from user.models import User


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

def new(request):
    user = request.user
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = user
            new_post.save()
            return redirect('LnF:list')
    
    else:
        form = PostForm()
    
    ctx = {'form': form}
    return render(request, 'LnF/new.html', ctx)
