from django.shortcuts import render
from .models import *
# Create your views here.

def list(request):
    brands = Brand.objects.all()

    brand_list = []
    for brand in brands:
        if brand.retake == 1:
            retake =  "possible"
        else:
            retake = "impossible"
        
        if brand.remote == 1:
            remote = "possible"
        else:
            remote = "impossible"
        brand_detail = [brand.name, retake, remote, brand.time]

        etcs = brand.frame_set.all()
        etcList = []
        for etc in etcs:
            etcList.append([etc.price, etc.frame, etc.take])

        brand_detail.append(etcList)

        brand_list.append(brand_detail)

        # brand_list = [brand_name, retake, remote, time, [frame]]
        # frame = [price, 프레임 컷 수, 총 촬영 수]

    print(brand_list)
    ctx = {"brand_list": brand_list}
    return render(request, "brand/main.html", ctx)
