from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="log_out"),
    path("signup/", views.signup, name="signup"),
    path("change_password/", views.change_password, name='change_password'),
    path('member_modify/', views.member_modify, name='member_modify'),
]