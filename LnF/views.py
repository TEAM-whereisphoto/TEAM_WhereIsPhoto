from django.http import  JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from map.models import Booth
from brand.models import Brand
from user.models import User
import json

@csrf_exempt
def list(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        if query:
            booths = Booth.objects.filter(name__icontains = query)
            posts = LnF_Post.objects.filter(booth__in = booths).order_by('-time')
        else:
            posts=LnF_Post.objects.all().order_by('-time')
        ctx = {'posts': posts, 'query': query}
        
        return render(request, 'LnF/list.html', context=ctx)


def new(request):
    user = request.user
    booths = Booth.objects.all()

    if request.method == "POST":
        booth_name = request.POST.get('booth')
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = user
            new_post.booth = get_object_or_404(Booth, name=booth_name)
            new_post.save()
            return redirect('LnF:list')
    
    else:
        form = PostForm()
    
    ctx = {'form': form, 'booths': booths }
    return render(request, 'LnF/new.html', ctx)

def new_one(request, pk):
    user = request.user
    booth = get_object_or_404(Booth, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = user
            new_post.booth = booth
            new_post.save()
            return redirect('LnF:list')
    
    else:
        form = PostForm()
    
    ctx = {'form': form, 'booth': booth }
    return render(request, 'LnF/new_one.html', ctx)

def tag(request):
    req = json.loads(request.body)


# pk: booth pk
def booth_detail(request, pk):
    booth = get_object_or_404(Booth, id=pk)
    posts = LnF_Post.objects.filter(booth = booth)
    ctx = {'posts': posts, 'booth': booth}
    return render(request, 'LnF/booth_detail.html', context=ctx)

def post_detail(request,pk):
    post = get_object_or_404(LnF_Post, id=pk)
    booth = post.booth
    ctx = {'post': post, 'booth': booth}
    return render(request, 'LnF/post_detail.html', context=ctx)

@login_required
def post_update(request, pk):
    post = get_object_or_404(LnF_Post, id=pk)
    booths = Booth.objects.all()

    if request.user == post.user:
        if request.method == 'POST':
            booth_name = request.POST.get('booth')
            form = PostForm(request.POST, request.FILES, instance=post)

            if form.is_valid():
                post.booth = get_object_or_404(Booth, name=booth_name)
                post = form.save(commit=False)
                post.save()
            return redirect('LnF:post_detail', pk)

        else:
            booth = post.booth
            print(booth)
            form = PostForm(instance=post)
            ctx = {'form': form, 'booths':booths, 'booth':booth}
            return render(request, 'LnF/new.html', context=ctx)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(LnF_Post, id=pk)
    if request.user == post.user:
        post.delete()
        return redirect('LnF:list')



# ajax
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
    print(request.user.username)
    return JsonResponse({'id': id, 'type': type, 'content': content, 'comment-id': comment_id, 'user': request.user.username })

@csrf_exempt
def del_comment(request, pk):
    req = json.loads(request.body)
    comment_id = req['id']
    
    comment = get_object_or_404(Comment, id = comment_id)
    comment.delete()
    return JsonResponse({'id': comment_id})

@csrf_exempt
def tag(request):
    req = json.loads(request.body)
    query = req['query']
    postList = []

    if query:
        booths = Booth.objects.filter(name__icontains = query)
        posts = LnF_Post.objects.filter(booth__in = booths).order_by('-time')
    else:
        posts=LnF_Post.objects.all().order_by('-time')

    if req["분실"] == True:
        lostTag = posts.filter(tag = '분실')
        postList += lostTag
    if req["보관"] == True:
        keepTag = posts.filter(tag = "보관")
        postList += keepTag

    resList = []
    for post in postList:
        if post.img:
            img = post.img.url
        else:
            img = ""

        resList.append({'booth_name': post.booth.name, 'booth_id': post.booth.id ,'user': post.user.username, 'timeString': post.timeString, 'time': post.time.strftime('%m월 %d일'), 'content': post.content, 'img': img, 'tag': post.tag})
    return JsonResponse({'resList': resList})

 