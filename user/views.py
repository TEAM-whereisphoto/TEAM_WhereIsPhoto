from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, SignupForm

# Create your views here.
def main(request):
    return render(request, "user/main.html")

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "user/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return render(request, "user/main.html") #성공대신 main

            return render(request, "user/login.html")

        ctx = {"form": form}
        return render(request, "user/login.html", ctx)


def log_out(request):
    logout(request)
    return redirect("user:main")

def signup(request):
    form = SignupForm()
    if request.method == "POST":
        if User.objects.filter(username = request.POST['username']).exists():
            help_text = '이미 존재하는 아이디입니다.'
        elif User.objects.filter(email = request.POST['email']).exists():
            help_text = '이미 존재하는 이메일입니다.'
        elif request.POST['password1'] != request.POST['password2']:
            help_text = '비밀번호가 일치하지 않습니다'
        else :
            user = User.objects.create_user(
                username = request.POST['username'],
                password = request.POST['password1'],
                email = request.POST['email'],
            )
            login(request, user) #바로 로그인
            return redirect ('user:main')
        ctx = {'help_text':help_text}
        return render(request, template_name='user/signup.html',context=ctx)
    else:
        form = SignupForm()
        ctx = {'form':form}
        return render(request, template_name='user/signup.html', context=ctx)
    