from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, SignupForm

# 탈퇴시 랜덤숫자를 위해
from random import randint

# 리뷰 가져오기
from LnF.models import *

def main(request):
    users = request.user
    print(users)
    # posts = LnF_Post.objects.all()
    posts = LnF_Post.objects.filter(user = users)
    # posts = LnF_Post.objects.filter(user__contains = users).order_by('-time')

    try:
        exist = LnF_Post.objects.get(user = users)
    except LnF_Post.DoesNotExist:
        exist = 0
    except LnF_Post.MultipleObjectsReturned:
        exist = 1
    print(exist)

    ctx = {'posts': posts, 'exist': exist}
    return render(request, 'user/main.html', context=ctx)
    # return render(request, "user/main.html")

class LoginView(View):
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
                return render(request, "user/main.html")

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
        messages.error(request, 'Password not same')
    else:
      messages.error(request, 'Password not correct')
    return render(request, 'user/change_password.html')
  else:
    return render(request, 'user/change_password.html')

def member_modify(request):
    if request.method == "POST":
        #id = request.user.id
        #user = User.objects.get(pk=id)
        user = request.user
        user.username = request.POST["username"]
        user.save()
        return redirect('user:main')
    return render(request, 'user/member_modify.html')

def member_del(request):
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
    return render(request, 'user/member_del.html')

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
    posts = LnF_Post.objects.filter(user=request.user)
    comments =  Comment.objects.none()
    for post in posts:
        comments = comments | post.comment_set.filter(read=0)
    print(comments)
    # print(type(comments))
    ctx={'posts':posts, 'comments':comments, 'len':len(comments)}

    # for comment in comments:
    #     comment.read = 1
    #     comment.save()

    return render(request, template_name='user/notice.html', context=ctx)

def read_notice(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.read = 1
    comment.save()

    return redirect('LnF:detail', comment.post.booth_id)