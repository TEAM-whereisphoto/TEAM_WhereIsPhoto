from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, SignupForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# 탈퇴시 랜덤숫자를 위해
from random import randint

# 리뷰 가져오기
from LnF.models import *

#Liked 구현 
from map.models import *

from django.contrib.auth.decorators import login_required
# AnonymousUser 예외처리
@login_required
def main(request):
    users = request.user

    # dolike가 true인 booth-brand pair 관련 list 만들기
    liked_booth_brand = []
    my_likes = Liked.objects.filter(user = users)
    for my_like in my_likes:
        if my_like.dolike:
            liked_booth_brand.append([my_like.booth, my_like.booth.brand])

    user_liked_num = len(liked_booth_brand)
    comments = getNew(users)
    
    ctx = {'len': len(comments), 'liked_booth_brand':liked_booth_brand, 'user_liked_num': user_liked_num}
    return render(request, 'user/main.html', context=ctx)
    
def my_review(request):
    users = request.user

    #리뷰
    reviews_posts = Review.objects.filter(user = users)

    try:
        my_review_exist = Review.objects.get(user = users)
    except Review.DoesNotExist:
        my_review_exist = 0
    except Review.MultipleObjectsReturned:
        my_review_exist = 1
    
    ctx = {'reviews_posts': reviews_posts,'my_review_exist': my_review_exist}
    return render(request, 'user/my_review.html', context=ctx)

# http://127.0.0.1:8000/find/review/3/
def read_my_review(request, pk):
    my_review = Review.objects.get(pk=pk)

    return redirect('map:review_detail', my_review.id)

def my_lnf(request):
    users = request.user

    #분실물
    lnf_posts = LnF_Post.objects.filter(user = users)

    try:
        my_lnf_exist = LnF_Post.objects.get(user = users)
    except LnF_Post.DoesNotExist:
        my_lnf_exist = 0
    except LnF_Post.MultipleObjectsReturned:
        my_lnf_exist = 1

    ctx = {'lnf_posts': lnf_posts, 'my_lnf_exist': my_lnf_exist}
    return render(request, 'user/my_lnf.html', context=ctx)

def read_my_lnf(request, pk):
    my_lnf = LnF_Post.objects.get(pk=pk)

    return redirect('LnF:post_detail', my_lnf.id)

class LoginView(View):
    @method_decorator(csrf_exempt)
    def get(self, request):
        form = LoginForm()
        return render(request, "user/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password, email=email)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend') #아래와 동일. 
                return redirect("user:main")

            return render(request, "user/login.html")

        ctx = {"form": form}
        return render(request, "user/login.html", ctx)

def log_out(request):
    logout(request)
    return redirect("/")

def signup(request):
    form = SignupForm()
    if request.method == "POST":
        if User.objects.filter(username = request.POST['username']).exists():
            help_text = '이미 존재하는 아이디입니다.'
        elif request.POST['password1'] != request.POST['password2']:
            help_text = '비밀번호가 일치하지 않습니다'
        elif User.objects.filter(email = request.POST['email']).exists():
            help_text = '이미 존재하는 이메일입니다.'
        else :
            user = User.objects.create_user(
                username = request.POST['username'],
                password = request.POST['password1'],
                email = request.POST['email'],
            )
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            #login(request, user) #바로 로그인 -> 소셜 로그인 구현으로 인한 백엔드 오류 방지
            return redirect ('user:main')
        ctx = {'help_text':help_text}
        return render(request, template_name='user/signup.html',context=ctx)
    else:
        form = SignupForm()
        ctx = {'form':form}
        return render(request, template_name='user/signup.html', context=ctx)

# 패스워드 변경
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth

def change_password(request):
  if request.method == "POST":
    user = request.user
    # 아이디 변경
    edit_username = request.GET.get('edit_username', user.username)
    # edit_username = request.POST["username"]
    print(edit_username)
    # 패스워드 조건 설정
    origin_password = request.POST["origin_password"]

    if check_password(origin_password, user.password):
      new_password = request.POST["new_password"]
      confirm_password = request.POST["confirm_password"]
      if new_password == confirm_password:
        user.set_password(new_password)
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('user:main')
      else:
        messages.error(request, '비밀번호가 일치하지 않습니다.')
    else:
      messages.error(request, '현재 비밀번호가 일치하지 않습니다.')
    return render(request, 'user/change_password.html')
  else:
    return render(request, 'user/change_password.html')

def modify(request):
    if request.method == "POST":
        #id = request.user.id
        #user = User.objects.get(pk=id)
        user = request.user
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.save()
        return redirect('user:main')
    return render(request, 'user/modify.html')

def delete(request):
    if request.method == "POST":
        user = request.user
        pw_del = request.POST["pw_del"]
        if check_password(pw_del, user.password):
            random_number = randint(1000, 10000)
            user.username = "탈퇴한 사용자"+str(random_number)
            user.password = randint(1000000000, 10000000000)
            user.save()
            logout(request)
            # user.delete()
            return redirect('/')
        else:
            messages.error(request, '현재 비밀번호가 일치하지 않습니다.')
    return render(request, 'user/delete.html')

# 장고 기본 로그인(조건 까다로움)
# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('index')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'user/change_password.html', {
#         'form': form
#     })

def notice(request):
    comments = getNew(request.user)
    ctx={'comments':comments, 'len':len(comments)}

    return render(request, template_name='user/notice.html', context=ctx)

def getNew(userss):
    posts = LnF_Post.objects.filter(user=userss)
    comments =  Comment.objects.none()
    for post in posts:
        comments = comments | post.comment_set.filter(read=0)
    return comments

def read_notice(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.read = 1
    comment.save()

    return redirect('LnF:post_detail', comment.post.id)


def nav_notice(request):
    if request.user.is_authenticated:
        comments = getNew(request.user)
        if len(comments) > 0:
            notice = True
        else:
            notice = False
    else:
        notice =False

    ctx={'notice': notice}
    return JsonResponse(ctx)