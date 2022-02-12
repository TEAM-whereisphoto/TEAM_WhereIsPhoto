from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from .models import *

from LnF.models import LnF_Post
from brand.models import Brand
from brand.models import Frame
from user.models import User

from django.templatetags.static import static
from django.db.models import Q
# from pytz import timezone
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def mymap(request):
    booths = Booth.objects.all() 
    ctx = {'booths': booths} # 너무 많으면 여기서 booths[:10] 로 몇개만 뽑아도 됨!
    return render(request, 'map/mymap.html', context=ctx)

def avg(pk): # 평균 별점 계산 함수
    booth = Booth.objects.get(id=pk)
    reviews = Review.objects.filter(booth = booth.pk)

    n=0
    sum =0
    for review in reviews:
        n += 1
        sum += review.rate
    booth.rating = float(sum/n) #소수점 출력이 안나옴
    booth.review_number = n
    booth.save()

def booth_detail(request,pk):
    booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
    reviews = Review.objects.filter(booth = booth.pk)
    lnfs = LnF_Post.objects.filter(booth= booth.pk)
    # avg(pk) # 왜 새로고침해야 뜨는거지

    brand = Brand.objects.all()
    brand_list = []
    for br in brand:
        if(br == booth.brand):
            if br.retake == 1:
                retake = "possible"
            else:
                retake = "impossible"
            if br.remote == 1:
                remote = "possible"
            else:
                remote = "impossible"
            brand_detail = [br.name, retake, remote, br.time]

            etcs = br.frame_set.all()
            etcList = []
            for etc in etcs:
                etcList.append([etc.price, etc.frame, etc.take])

        brand_detail.append(etcList)
        brand_list.append(brand_detail)

    ctx = {'booth': booth, 'lnfs' : lnfs, 'reviews': reviews, 'brand_list': brand_list}
    return render(request, template_name='map/booth_detail.html', context=ctx)

def booth_review_list(request,pk):
    booth = Booth.objects.get(id=pk)
    reviews = Review.objects.filter(booth = booth.pk)
    ctx = {'reviews': reviews}
    return render(request, template_name='map/review_list.html', context=ctx)


def booth_review_create(request):
    booth = Booth.objects.get(id=pk)
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.booth = booth
            post.user = user
            avg(pk)  # 왜 새로고침해야 뜨는거지
            post.save()
            return redirect('map:review_list')
    else:
        form = ReviewForm()
    ctx = {'form': form}
    return render(request, template_name='map/review_create.html', context=ctx)


def review_list(request):
    reviews = Review.objects.all()
    ctx = {'reviews': reviews}
    return render(request, template_name='map/review_list.html', context=ctx)

def review_detail(request, pk):  # request도 받고 몇번 인덱스인지 = pk를 받는다. 게시물 상세조
    review = Review.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다
    ctx = {'review': review}  # template로 보내기 위해선 context를 만들어야한다.
    return render(request, template_name='map/review_detail.html', context=ctx)

def review_create(request):
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            return redirect('map:review_list')
    else:
        form = ReviewForm()
    ctx = {'form': form}
    return render(request, template_name='map/review_create.html', context=ctx)

def review_update(request, pk):
    review = get_object_or_404(Review, id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            return redirect('reviews:review_detail', pk)
    else:
        form = ReviewForm(instance=review)
        ctx = {'form': form}

        return render(request, template_name='map/review_create.html', context=ctx)

def review_delete(request, pk):
    review = get_object_or_404(Review, id=pk)
    review.delete()
    return redirect('reviews:review_list')



'''
@csrf_exempt
def like_ajax(request):
    req = json.loads(request.body)
    booth_id = req['id']
    booth = Booth.objects.get(id =booth_id)

    if booth.dolike == True:
        post.dolike = False
        status = post.dolike
        k=1
    else:
        post.dolike = True
        status = post.dolike
        k=0
    post.save()

    return JsonResponse({'id': post_id, 'k': k, 'status':status})
    
'''

def search(request):
    search = request.GET.get('search','')
    boothlist = Booth.objects.filter(name__contains=search)
    ctx = {'booths':boothlist}
    return render(request, 'map/mymap.html', context=ctx)

@csrf_exempt
def load(request):
    booths = Booth.objects.all()
    boothList = []
    for booth in booths:
        boothDict = {}
        boothDict = {"id": booth.id, "name": booth.name, "location": booth.location, "x": booth.x, "y": booth.y, "rating":booth.rating, 
        "likenum": booth.likenum, "operationHour": booth.operationHour, "review_num": len(booth.review_set.all()), "brand": booth.brand.name}
        boothList.append(boothDict)

    return JsonResponse({'boothList': boothList})


    # [{id, name, location, x, y, rating, likenum, operationHour, brand}, {}]