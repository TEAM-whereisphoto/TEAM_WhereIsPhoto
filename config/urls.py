"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# 비번 초기화
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include, reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('map.urls')),
    path('brand/', include('brand.urls')),
    path('user/', include('user.urls')),
    path('LnF/', include('LnF.urls')),
    path('accounts/', include('allauth.urls')),

    path('', include('django.contrib.auth.urls')),
    
    #템플릿 추가중
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name='user/reset_password.html'),
        name='password_reset'
    ),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='user/reset_password_sent.html'), name='password_reset_done'),

    path(
        'password_reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='user/reset_password_form.html'),
        name='password_reset_confirm'
    ),

    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='user/reset_password_sucess.html'),
        name='password_reset_complete'
    )

]

# path(
#         'password_reset/',
#         auth_views.PasswordResetView.as_view(
#             template_name='accounts/reset_password.html'
#             success_url=reverse_lazy('accounts:password_reset_done')
#         ),
#         name='password_reset'
#     ),
#     path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_sent.html'), name='password_reset_done'),
#     path(
#         'password_reset/<uidb64>/<token>/',
#         auth_views.PasswordResetConfirmView.as_view(
#             template_name='accounts/reset_password_form.html'
#             success_url=reverse_lazy('accounts:password_reset_complete')
#         ),
#         name='password_reset_confirm'
#     ),
#     path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_sucess.html'), name='password_reset_complete'),
