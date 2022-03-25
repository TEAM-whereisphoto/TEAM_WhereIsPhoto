from django.urls import path
from . import views
app_name = "brand"

urlpatterns = [
    path("", view = views.list, name="list")
]