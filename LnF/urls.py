from django.urls import path
from LnF import views

app_name = "LnF"

urlpatterns = [
    path("", view=views.list, name='list'),
    path("new/", view=views.new, name='new'),
]