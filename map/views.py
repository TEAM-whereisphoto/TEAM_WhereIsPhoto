from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static
from .models import *


# Create your views here.
def mymap(request):
    booths = Booth.objects.all()
    src = static('icon/pin_yellow.png')
    ctx = {'booths':booths, 'src':src}
    return render(request, 'map/mymap.html', context=ctx)