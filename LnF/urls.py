from django.urls import path
from LnF import views

app_name = "LnF"

urlpatterns = [
    path("", view=views.list, name='list'),
    path("new/", view=views.new, name='new'),
    path("tag/", view=views.tag, name='tag'),
    path("<int:pk>/booth_detail/", view=views.booth_detail, name='booth_detail'),
    path("<int:pk>/post_detail/", view=views.post_detail, name='post_detail'),
    path("<int:pk>/update/", view=views.post_update, name='post_update'),
    path("<int:pk>/delete/", view=views.post_delete, name='post_delete'),
    path("<int:pk>/post_detail/add_comment/", view= views.add_comment, name="add_comment"),
    path("<int:pk>/post_detail/del_comment/", view= views.del_comment, name="del_comment"),
]