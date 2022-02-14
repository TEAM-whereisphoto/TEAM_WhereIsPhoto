from ctypes.wintypes import tagPOINT
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from map.models import Booth
from brand.models import Brand
from user.models import User
from django.db.models import Q

import json

@csrf_exempt
def list(request):
    posts = LnF_Post.objects.all()
    if request.method == "POST":
        req = json.loads(request.body)
        postList = []

        if req["분실"] == True:
            lostTag = LnF_Post.objects.filter(tag = '분실')
            postList += lostTag
        if req["보관"] == True:
            keepTag = LnF_Post.objects.filter(tag = "보관")
            postList += keepTag

        posts= LnF_Post.objects.filter(title__in = postList)

        return JsonResponse({"posts": posts})

    else:
        query = request.GET.get('query', '')

        if query:
            booths = Booth.objects.filter(name__icontains = query)
            posts = LnF_Post.objects.filter(booth__in = booths).order_by('-time')

        else:
            posts=LnF_Post.objects.all().order_by('-time')

    ctx = {'posts': posts}
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

def tag(request):
    req = json.loads(request.body)


# pk: booth pk
def detail(request, pk):
    booth = get_object_or_404(Booth, id=pk)
    posts = LnF_Post.objects.filter(booth = booth)
    ctx = {'posts': posts, 'booth': booth}
    return render(request, 'LnF/detail.html', context=ctx)


@csrf_exempt
def add_comment(request, pk):
    req = json.loads(request.body)
    id = req['id']
    type = req['type']
    content = req['content']
    
    comment = Comment()
    comment.post = LnF_Post.objects.get(id = id)
    comment.content = content
    comment.user = request.user
    comment.time = timezone.now()
    comment_id = comment.id
    comment.save()
    return JsonResponse({'id': id, 'type': type, 'content': content, 'comment-id': comment_id})

@csrf_exempt
def del_comment(request, pk):
    req = json.loads(request.body)
    comment_id = req['id']
    
    comment = get_object_or_404(Comment, id = comment_id)
    comment.delete()
    return JsonResponse({'id': comment_id})


