from django.urls import path
from .import views

app_name = "map"

urlpatterns = [
    path('', view=views.review_list, name='list'),  # 리뷰 리스트 페이지
    path('<int:pk>/', view=views.review_detail, name='detail'),  # 리뷰 디테일 페이지
    path('review/', view=views.review_create, name='create'),  # 리뷰 작성/수정 페이지
    path('<int:pk>/update', view=views.review_update, name='update'),
    path('<int:pk>/delete', view=views.review_delete, name='delete'),
]