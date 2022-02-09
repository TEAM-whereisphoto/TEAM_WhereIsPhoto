from django.urls import path
from LnF import views

app_name = "LnF"

urlpatterns = [
    path("", view=views.list, name='list'),
    # path("filter/", view=views.filter, name="filter"),
]