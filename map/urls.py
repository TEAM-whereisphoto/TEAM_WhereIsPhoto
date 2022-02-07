from django.urls import path
from map import views

app_name = "map"

urlpatterns = [
    # path('', view.mainpage) # 메인페이지 view
    path('map/', views.mymap, name="mymap"),
    
]