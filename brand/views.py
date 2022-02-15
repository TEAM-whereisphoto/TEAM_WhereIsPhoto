from django.shortcuts import render
from .models import *
# Create your views here.

def list(request):
    brands = Brand.objects.all()

    brand_list = []
    for brand in brands:
        brand_detail = [brand.name, brand.retake, brand.remote, brand.time, brand.img]

        etcs = brand.frame_set.all()
        etcList = []
        for etc in etcs:
            etcList.append([etc.price, etc.frame, etc.take])

        brand_detail.append(etcList)

        brand_list.append(brand_detail)

        # brand_list = [brand_name, retake, remote, time, [frame]]
        # frame = [price, 프레임 컷 수, 총 촬영 수]

    ctx = {"brand_list": brand_list}
    return render(request, "brand/main.html", ctx)
