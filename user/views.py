from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, SignupForm

# 새로 추가하는 메소드
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str


# Create your views here.
def main(request):
    return render(request, "user/main.html")

#모든 account user로 변경(토큰 제외)
def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request) 
            # localhost:8000
            message = render_to_string('templates/user/user_activate_email.html',                         {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = "[SOT] 회원가입 인증 메일입니다."
            user_email = user.username
            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()
            return HttpResponse(
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
                '</div>'
            )
            return redirect('user:home')
    return render(request, 'user/signup.html')

def activate(request, uid64, token):

    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('account:home')
    else:
        return HttpResponse('비정상적인 접근입니다.')
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

# def signup(request):
#     form = SignupForm()
#     if request.method == "POST":
#         if User.objects.filter(username = request.POST['username']).exists():
#             help_text = '이미 존재하는 아이디입니다.'
#         elif request.POST['password1'] != request.POST['password2']:
#             help_text = '비밀번호가 일치하지 않습니다'
#         elif User.objects.filter(email = request.POST['email']).exists():
#             help_text = '이미 존재하는 이메일입니다.'
#         else :
#             user = User.objects.create_user(
#                 username = request.POST['username'],
#                 password = request.POST['password1'],
#                 email = request.POST['email'],
#             )
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             #login(request, user) #바로 로그인 -> 소셜 로그인 구현으로 인한 백엔드 오류 방지
#             return redirect ('user:main')
#         ctx = {'help_text':help_text}
#         return render(request, template_name='user/signup.html',context=ctx)
#     else:
#         form = SignupForm()
#         ctx = {'form':form}
#         return render(request, template_name='user/signup.html', context=ctx)
    
