
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import urls
# 비번 초기화
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include, reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('brand.urls')),
    path('find/', include('map.urls')),
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
#set image urls
urlpatterns += static(settings.MEDIA_URL, document_root=config.settings.base.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=config.settings.base.STATIC_ROOT)
