from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from .models import *
from LnF.models import LnF_Post
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# Create your views here.
def mainpage(request):
    return render(request, 'base.html')

def mymap(request):
    booths = Booth.objects.all() 
    ctx = {'booths': booths} # 너무 많으면 여기서 booths[:10] 로 몇개만 뽑아도 됨!
    return render(request, 'map/mymap.html', context=ctx)

# 부스 평균 별점 계산 후 booth.rate_average 저장
def save_booth_rate_avg(booth): 
    reviews = Review.objects.filter(booth = booth.id)
    
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

def booth_detail(request,pk):
    booth = Booth.objects.get(id=pk)
    reviews = Review.objects.filter(booth = booth.pk).order_by('-time')
    lnfs = LnF_Post.objects.filter(booth= booth.pk).order_by('-time')
    lnf_num = len(lnfs)
    lnfs = lnfs[:3]

    if request.user.is_authenticated:
        try:
            liked = Liked.objects.get(user = request.user, booth= booth)
            currentLikeState = liked.dolike
        except Liked.DoesNotExist:
            currentLikeState = False
    else:
        currentLikeState = False

    tag_list = tag_count(pk)
    width = booth.rate_average * 20 
    

    ctx = {'booth': booth, 'lnfs' : lnfs, 'reviews': reviews, 'tag_list': tag_list, 'currentLikeState': currentLikeState, 'width':width}
    return render(request, template_name='map/booth_detail.html', context=locals())

def booth_review_list(request,pk):
    booth = Booth.objects.get(id=pk)
    reviews = Review.objects.filter(booth = booth.pk).order_by('-time')
    ctx = {'reviews': reviews,'pk': pk, 'booth':booth, 'boothname': booth.name, }
    return render(request, template_name='map/review_list.html', context=ctx)

@login_required
def booth_review_create(request, pk):
    booth = get_object_or_404(Booth, id=pk)
    boothname = booth.name
    id = pk
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        rate = request.POST.get('rating')

        if form.is_valid():
            post = form.save(commit=False)
            post.booth = booth
            post.user = request.user
            post.boothid = pk
            post.rate = rate
            booth.review_number += 1

            post.save()
            booth.save()
            save_booth_rate_avg(booth)
            return redirect('map:booth_review_list', post.boothid)
    else:
        form = ReviewForm()

    ctx = {'form': form, 'id': id, 'boothname':boothname}
    return render(request, template_name='map/review_create.html', context=ctx)
   
def review_update(request, pk):
    review = get_object_or_404(Review, id=pk)
    boothname = review.booth
    boothid = review.boothid

    if request.user == review.user:
        if request.method == 'POST': #post방식 요청
            rate = request.POST.get('rating')
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid(): #폼 유효하면
                review.rate = rate
                review = form.save(commit=False) #데이터 가져오기
                review.save() #저장
                save_booth_rate_avg(review.booth)
                return redirect('map:booth_review_list', boothid)

        else:
            ctx = {'review': review,'id':boothid, 'boothname' : boothname}
        return render(request, template_name='map/review_create.html', context=ctx)

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, id=pk)
    if request.user == review.user:
        booth_id = review.boothid
        booth = get_object_or_404(Booth, id=booth_id)  # id가 pk인 게시물 하나를 가져온다.
        booth.review_number -= 1
        booth.save()
        review.delete()

        save_booth_rate_avg(booth)

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
        like = Liked.objects.get(user = request.user, booth=booth)

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
    like = Liked.objects.get(user = request.user, booth = booth)
    
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