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

import operator

# Create your views here.
def mainpage(request):
    return render(request, 'base.html')
def mymap(request):
    booths = Booth.objects.all() 
    ctx = {'booths': booths} # 너무 많으면 여기서 booths[:10] 로 몇개만 뽑아도 됨!
    return render(request, 'map/mymap.html', context=ctx)

def avg(request, pk): # 평균 별점 계산 함수
    booth = Booth.objects.get(id=pk)
    reviews = Review.objects.filter(booth = booth.pk)

    n=0
    sum =0
    try:
        for review in reviews:
            n += 1
            sum += review.rate
            rate = round(sum/n, 1)
            k = int(rate)
            if (rate-k) < 0.5:
                booth.ranting = k
            else:
                booth.rating = k + 0.5
    except:
        print("등록된 리뷰가 없습니다.")
    booth.review_number = n
    booth.save()


def tag_count(pk):
    booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
    reviews = Review.objects.filter(booth = booth.pk)
    tag_dic = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]

    for review in reviews:
        tags = []
        tags = review.title
        for tag in tags:
            if tag == '시설이 깨끗해요':
                tag_dic[0][1] += 1
            elif tag == '소품이 다양해요':
                tag_dic[1][1] += 1
            elif tag == '부스가 많아요':
                tag_dic[2][1] += 1
            elif tag == '고데기가 있어요':
                tag_dic[3][1] += 1
            elif tag == '로드점이에요':
                tag_dic[4][1] += 1
    print(tag_dic)
    return tag_dic

def booth_brand(request, pk):
    booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
    like = Liked.objects.all()
    avg(request, pk)  # 왜 새로고침해야 뜨는거지
    brandname = booth.brand
    brand = Brand.objects.get(name=brandname)
    brand_list = []
    if brand.retake == 1:
        retake = "possible"
    else:
        retake = "impossible"
    if brand.remote == 1:
        remote = "possible"
    else:
        remote = "impossible"
    brand_detail = [brand.name, retake, remote, brand.time]
    etcs = brand.frame_set.all()
    etcList = []
    for etc in etcs:
        etcList.append([etc.price, etc.frame, etc.take])
    brand_detail.append(etcList)
    brand_list.append(brand_detail)

    return brand_list


def booth_detail(request,pk):
    booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
    reviews = Review.objects.filter(booth = booth.pk)
    lnfs = LnF_Post.objects.filter(booth= booth.pk)
    
    brand = Brand.objects.all()
    brand_list = []
    brand_list = booth_brand(request, pk)
    tag_dic = tag_count(pk)
    tag_dic = sorted(tag_dic, key= lambda x: (x[0],-x[1]), reverse = True)

    ctx = {'booth': booth, 'lnfs' : lnfs, 'reviews': reviews, 'brand_list': brand_list, 'pk': pk}
    return render(request, template_name='map/booth_detail.html', context=ctx)

def booth_review_list(request,pk):
    booth = Booth.objects.get(id=pk)
    reviews = Review.objects.filter(booth = booth.pk)
    ctx = {'reviews': reviews,'pk':pk}
    return render(request, template_name='map/review_list.html', context=ctx)

def booth_review_create(request, pk):
    user = request.user
    booth = Booth.objects.get(id=pk)
    if user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.booth = booth
                post.user = user
                post.boothid = pk
                avg(request, pk)  # 왜 새로고침해야 뜨는거지
                post.save()
                return redirect('map:booth_review_list', pk)
        else:
            form = ReviewForm()
        ctx = {'form': form}
        return render(request, template_name='map/review_create.html', context=ctx)
    else:
        return redirect('user:login')

def review_detail(request, pk):  # request도 받고 몇번 인덱스인지 = pk를 받는다. 게시물 상세조
    review = Review.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다
    tags = []
    tags = review.title

    ctx = {'review': review, 'pk':pk, 'tags':tags}  # template로 보내기 위해선 context를 만들어야한다.
    return render(request, template_name='map/review_detail.html', context=ctx)


def review_update(request, pk):
    review = get_object_or_404(Review, id=pk)
    boothid = review.boothid
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            return redirect('map:booth_review_list', boothid)
    else:
        form = ReviewForm(instance=review)
        ctx = {'form': form,'pk':pk}

        return render(request, template_name='map/review_create.html', context=ctx)

def review_delete(request, pk):
    review = get_object_or_404(Review, id=pk)
    booth_id = review.boothid
    review.delete()
    return redirect('map:booth_review_list', booth_id)

def search(request):
    search = request.GET.get('search','')
    boothlist = Booth.objects.filter(name__contains=search)
    ctx = {'booths': boothlist}
    return render(request, 'map/mymap.html', context=ctx)


@csrf_exempt
def like_ajax(request):
    req = json.loads(request.body)
    pk = req['id']
    booth = Booth.objects.get(id=pk)
    user = request.user
    liked = Liked.objects.get(booth=booth.pk, user=user)


    if liked.dolike == True:
        liked.dolike = False
        status = liked.dolike
        k = 1
    else:
        liked.dolike = True
        status = liked.dolike
        k = 0
    liked.save()

    return JsonResponse({'id': pk, 'k': k, 'status': status})

def search(request):
    search = request.GET.get('search','')
    boothlist = Booth.objects.filter(name__contains=search)
    ctx = {'booths':boothlist}
    return render(request, 'map/mymap.html', context=ctx)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def filter(request):
#     req = json.loads(request.body)
#     showbrands = req['brands']
#     print("before")
#     boothlist = list(Booth.objects.filter(brand__in=showbrands).values())
#     # 이게 지금 foriegn키라 접근이 뭔가 어렵나봄..
#     # boothlist = list(Booth.objects.all().values())
#     print(boothlist)


#     return JsonResponse({'booths':boothlist})

# from django.core import serializers
# @csrf_exempt
# def dbtojs(request):
#     boothobjs = Booth.objects.all()
#     boothjsons = serializers.serialize("json", boothobjs)

