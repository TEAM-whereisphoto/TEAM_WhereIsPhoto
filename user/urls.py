from django.urls import path
from . import views

# 비번 초기화
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = "user"

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="log_out"),
    path("signup/", views.signup, name="signup"),
    path("change_password/", views.change_password, name='change_password'),
    path('member_modify/', views.member_modify, name='member_modify'),

    # 보류
    # path(
    #     'password_reset/',
    #     auth_views.PasswordResetView.as_view(
    #         template_name='user/reset_password.html',
    #         success_url=reverse_lazy('user:password_reset_done')
    #     ),
    #     name='password_reset'
    # ),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='user/reset_password_sent.html'), name='password_reset_done'),
    # path(
    #     'password_reset_confirm/<uidb64>/<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(
    #         template_name='user/reset_password_form.html',
    #         success_url=reverse_lazy('user:password_reset_complete')
    #     ),
    #     name='password_reset_confirm'
    # ),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/reset_password_sucess.html'), name='password_reset_complete'),
]