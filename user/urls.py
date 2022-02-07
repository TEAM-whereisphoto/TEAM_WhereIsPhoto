from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="log_out"),
    path("signup/", views.signup, name="signup"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"),
]