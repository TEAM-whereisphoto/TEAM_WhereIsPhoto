from django.urls import path
from LnF import views

app_name = "LnF"

urlpatterns = [
    path("", view=views.list, name='list'),
    path("new/", view=views.new, name='new'),
    path("<int:pk>/detail/", view=views.detail, name='detail'),
    path("<int:pk>/detail/add_comment/", view= views.add_comment, name="add_comment"),
    path("<int:pk>/detail/del_comment/", view= views.del_comment, name="del_comment"),
]