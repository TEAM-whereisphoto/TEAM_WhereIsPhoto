from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm


def review_list(request):
    reviews = Review.objects.all()
    ctx = {'posts': reviews}
    return render(request, template_name='map/review_list.html', context=ctx)  # context를 딕셔너리 형태로 만들어서 보낸다.

def review_detail(request, pk):  # request도 받고 몇번 인덱스인지 = pk를 받는다. 게시물 상세조
    review = Review.objects.get(id=pk)  # id가 pk인 게시물 하나를 가져온다
    ctx = {'post': review}  # template로 보내기 위해선 context를 만들어야한다.

    return render(request, template_name='map/review_detail.html', context=ctx)

def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('reviews:list')
    else:
        form = ReviewForm()
        ctx = {'form': form}

        return render(request, template_name='map/review_form.html', context=ctx)

def review_update(request, pk):
    review = get_object_or_404(Review, id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            return redirect('reviews:detail', pk)
    else:
        form = ReviewForm(instance=review)
        ctx = {'form': form}

        return render(request, template_name='map/review_form.html', context=ctx)

def review_delete(request, pk):
    review = get_object_or_404(Review, id=pk)
    review.delete()
    return redirect('reviews:list')