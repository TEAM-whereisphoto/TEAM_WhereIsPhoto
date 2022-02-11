from calendar import c
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from .models import *

from LnF.models import LnF_Post
from brand.models import Brand
from brand.models import Frame
from user.models import User

from django.templatetags.static import static
from django.db.models import Q
from pytz import timezone
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

def booth_statistic(request, pk):
    booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
    reviews = Review.objects.filter(booth = booth.pk)
    iron_yes = 0
    iron_no = 0

    street = 0
    road = 0

    deco_glass = 0
    deco_band = 0
    deco_hat = 0

    boxnum_one = 0
    boxnum_two = 0
    boxnum_thr = 0
    boxnum_fou = 0
    boxnum_fim = 0
    boxnum_max = 0
    boxnum_index=0

    for review in reviews:
        if review.iron == 'YES':
            iron_yes += 1
        else:
            iron_no += 1

        if review.street == 'STORE':
            street += 1
        else:
            road += 1

        if review.deco == 'GLASS':
            deco_glass += 1
        elif review.deco == 'BAND':
            deco_band += 1
        else:
            dceo_hat += 1

        if review.boxnum == 'one':
            boxnum_one += 1
            if boxnum_one > boxnum_max:
                boxnum_max = boxnum_one
                boxnum_index = 1
        elif review.boxnum == 'two':
            boxnum_two += 1
            if boxnum_two > boxnum_max:
                boxnum_max = boxnum_two
                boxnum_index = 2
        elif review.boxnum == 'three':
            boxnum_thr += 1
            if boxnum_thr > boxnum_max:
                boxnum_max = boxnum_thr
                boxnum_index = 3
        elif review.boxnum == 'four':
            boxnum_fou += 1
            if boxnum_fou > boxnum_max:
                boxnum_max = boxnum_fou
                boxnum_index = 4
        else:
            boxnum_fim += 1
            if boxnum_fim > boxnum_max:
                boxnum_max = boxnum_fim
                boxnum_index = 5

        booth.boxnum = boxnum_index
        if(iron_yes > iron_no):
            booth.iron = 1
        if(street > road):
            booth.street = 1
        if(deco_glass >= 2):
            booth.deco = 'GLASS'
        if(deco_band >= 2):
            booth.deco = 'BAND'
        if(deco_hat >= 2):
            booth.deco = 'HAT'
        booth.save()


def booth_detail(request,pk):
    booth = Booth.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다.
    reviews = Review.objects.filter(booth = booth.pk)
    lnfs = LnF_Post.objects.filter(booth= booth.pk)
    avg(pk) # 왜 새로고침해야 뜨는거지

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

    booth_statistic(request, pk)

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
