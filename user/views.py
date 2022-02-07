from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, SignupForm

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

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
    return redirect("user:main")

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
            user.is_active = False # 유저 비활성화
            user.save()
            current_site = get_current_site(request) 
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "계정 활성화 확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            #login(request, user) #바로 로그인 -> 소셜 로그인 구현으로 인한 백엔드 오류 방지
            return redirect ('user:main')
        ctx = {'help_text':help_text}
        return render(request, template_name='user/signup.html',context=ctx)
    else:
        form = SignupForm()
        ctx = {'form':form}
        return render(request, template_name='user/signup.html', context=ctx)

    
def login(request):
    # 포스트 방식으로 들어오면
    if request.method == 'POST':
        # 정보 가져와서 
        username = request.POST['username']
        password = request.POST['password']
        # 로그인
        user = auth.authenticate(request, username=username, password=password)
        # 성공
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        # 실패
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')

# 계정 활성화 함수(토큰을 통해 인증)
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("home")
    else:
        return render(request, 'home.html', {'error' : '계정 활성화 오류'})
    return 