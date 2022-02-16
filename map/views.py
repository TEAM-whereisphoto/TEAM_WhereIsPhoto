from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from .models import *

from LnF.models import LnF_Post
from brand.models import Brand
from brand.models import Frame
from user.models import User

from django.templatetags.static import static
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import operator


# Create your views here.
def mainpage(request):
    return render(request, 'base.html')

def mymap(request):
    booths = Booth.objects.all() 
    ctx = {'booths': booths} # 너무 많으면 여기서 booths[:10] 로 몇개만 뽑아도 됨!
    return render(request, 'map/mymap.html', context=ctx)

# 부스 평균 별점 계산 후 booth.rate_average 저장
def save_booth_rate_avg(pk): 
    booth = Booth.objects.get(id=pk)
    reviews = Review.objects.filter(booth = booth.pk)
    
    review_num=len(reviews)
    rate_sum =0
    if review_num == 0:
        booth.rate_average = 0
    else:
        for review in reviews:
            rate_sum += review.rate
        booth.rate_average = round(rate_sum/review_num, 1)
    booth.save()

def tag_count(pk):
    booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
    reviews = Review.objects.filter(booth = booth.pk)
    tag_list = [['clean', 0], ['prop', 0], ['booth', 0], ['iron', 0], ['street', 0]]

    for review in reviews:
        tags = []
        tags = review.tag
        for tag in tags:
            if tag == '시설이 깨끗해요':
                tag_list[0][1] += 1
            elif tag == '소품이 다양해요':
                tag_list[1][1] += 1
            elif tag == '부스가 많아요':
                tag_list[2][1] += 1
            elif tag == '고데기가 있어요':
                tag_list[3][1] += 1
            elif tag == '로드점이에요':
                tag_list[4][1] += 1
    tag_list = sorted(tag_list, key= lambda x: -x[1])
    return tag_list

# def booth_brand(request, pk):

#     booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
#     like = Liked.objects.all()
#     avg(pk)  # 왜 새로고침해야 뜨는거지
#     brandname = booth.brand
#     brand = Brand.objects.get(name=brandname)
#     brand_list = []
#     if brand.retake == 1:
#         retake = "possible"
#     else:
#         retake = "impossible"
#     if brand.remote == 1:
#         remote = "possible"
#     else:
#         remote = "impossible"
#     brand_detail = [brand.name, retake, remote, brand.time]
#     etcs = brand.frame_set.all()
#     etcList = []
#     for etc in etcs:
#         etcList.append([etc.price, etc.frame, etc.take])
#     brand_detail.append(etcList)
#     brand_list.append(brand_detail)

#     return brand_list


def booth_detail(request,pk):
    booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
    reviews = Review.objects.filter(booth = booth.pk)
    lnfs = LnF_Post.objects.filter(booth= booth.pk)
    if request.user.is_authenticated:
        try:
            liked = Liked.objects.get(user = request.user)
            currentLikeState = liked.dolike
        except Liked.DoesNotExist:
            currentLikeState = False
    else:
        currentLikeState = False

    tag_dic = tag_count(pk)
    tag_dic = sorted(tag_dic, key= lambda x: (x[0],-x[1]), reverse = True)

    ctx = {'booth': booth, 'lnfs' : lnfs, 'reviews': reviews, 'tag_dic': tag_dic, 'currentLikeState': currentLikeState}
    return render(request, template_name='map/booth_detail.html', context=ctx)

def booth_review_list(request,pk):
    booth = Booth.objects.get(id=pk)
    reviews = Review.objects.filter(booth = booth.pk)
    ctx = {'reviews': reviews,'pk':pk, 'boothname':booth.name}
    return render(request, template_name='map/review_list.html', context=ctx)

def booth_review_create(request, pk):
    booth = get_object_or_404(Booth, id=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.booth = booth
            post.user = request.user
            post.boothid = pk

            booth.review_number += 1
            post.save()
            booth.save()
            save_booth_rate_avg(pk)
            return redirect('map:booth_review_list', pk)
    else:
        form = ReviewForm()

    ctx = {'form': form}
    return render(request, template_name='map/review_create.html', context=ctx)
   

def review_detail(request, pk):  # request도 받고 몇번 인덱스인지 = pk를 받는다. 게시물 상세조
    review = Review.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다
    tags = []
    tags = review.tag
    colors = review.color

    ctx = {'review': review, 'pk':pk, 'tags':tags, 'colors': colors }  # template로 보내기 위해선 context를 만들어야한다.
    return render(request, template_name='map/review_detail.html', context=ctx)


def review_update(request, pk):
    review = get_object_or_404(Review, id=pk)
    boothid = review.boothid
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            save_booth_rate_avg(pk)
            return redirect('map:booth_review_list', boothid)
    else:
        form = ReviewForm(instance=review)
        ctx = {'form': form,'pk':pk}

        return render(request, template_name='map/review_create.html', context=ctx)

def review_delete(request, pk):
    review = get_object_or_404(Review, id=pk)
    booth = get_object_or_404(Booth, id=booth_id)  # id가 pk인 게시물 하나를 가져온다.

    booth_id = review.boothid
    booth.review_number -= 1
    booth.save()
    review.delete()

    save_booth_rate_avg(pk)

    return redirect('map:booth_review_list', booth_id)

def search(request):
    search = request.GET.get('search','')
    boothlist = Booth.objects.filter(name__contains=search)
    ctx = {'booths': boothlist}
    return render(request, 'map/mymap.html', context=ctx)


@csrf_exempt
# login o , currentLikeState: False -> True
def like_ajax(request, pk):
    booth = get_object_or_404(Booth, id=pk)
    user = request.user
    try:
        like = Liked.objects.get(user = request.user)

    except Liked.DoesNotExist:
        like = Liked.objects.create(booth = booth, user = user)
    
    like.dolike = True
    booth.likenum += 1
    like.save()
    booth.save()
    return JsonResponse({'booth_id': booth.id })

# login o, currentLikeState: True -> False
def dislike_ajax(request, pk):
    booth = get_object_or_404(Booth, id=pk)
    user = request.user
    like = Liked.objects.get(user = request.user)
    
    like.dolike = False
    booth.likenum -= 1
    like.save()
    booth.save()

    return JsonResponse({'booth_id': booth.id })


def search(request):
    search = request.GET.get('search','')
    boothlist = Booth.objects.filter(name__contains=search)
    ctx = {'booths':boothlist}
    return render(request, 'map/mymap.html', context=ctx)


@csrf_exempt
def load(request):
    booths = list(Booth.objects.values("pk", "name", "location", "x", "y", "rate_average", "likenum", "operationHour", "brand__name", "review_number"))
    return JsonResponse({'boothList': booths})

    # [{id, name, location, x, y, rating, likenum, operationHour, brand}, {}]