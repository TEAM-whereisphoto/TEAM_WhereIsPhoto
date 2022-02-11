from django.urls import path
from map import views

app_name = "map"

urlpatterns = [
    path('review/list/', view=views.review_list, name='review_list'),  # 리뷰 리스트 페이지
    path('review/<int:pk>/', view=views.review_detail, name='review_detail'),  # 리뷰 디테일 페이지
    path('review/create/', view=views.review_create, name='review_create'),  # 리뷰 작성/수정 페이지
    path('<int:pk>/update', view=views.review_update, name='review_update'),
    path('<int:pk>/delete', view=views.review_delete, name='review_delete'),

    path('booth/detail/<int:pk>', view=views.booth_detail, name='booth_detail'),
    path('booth/detail/<int:pk>/review', view=views.booth_review_list, name='booth_review_list'), 

    # path('', view.mainpage) # 메인페이지 view
    path('map/', views.mymap, name="mymap"),
    path('search/', views.search, name="search"),
    path('', view=views.review_list, name='list'),  # 리뷰 리스트 페이지

    path('filter/', views.filter, name="filter")
]