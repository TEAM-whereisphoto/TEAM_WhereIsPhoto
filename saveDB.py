import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
import django
django.setup()


from brand.models import Brand, Frame
from map.models import Booth
import pandas as pd

def brand():
    brand_dict = {
        "인생네컷": {
            "retake": "YES",
            "remote": "YES",
            "QR": "YES",
            "time": 10,
            "img": "/static/icons/brand/인생네컷.png",
            "liked_img": "/static/icons/liked/life_four_liked.png",
        },
        "셀픽스":{
            "retake": "YES",
            "remote": "YES",
            "QR": "YES",
            "time": 20,
            "img": "/static/icons/brand/셀픽스.png",
            "liked_img": "/static/icons/liked/selpix_liked.png",
        },
        "포토시그니처": {
            "retake": "YES",
            "remote": "YES",
            "QR": "YES",
            "time": 10,
            "img": "/static/icons/brand/포토시그니쳐.png",
            "liked_img": "/static/icons/liked/signature_liked.png",
        },
        "하루필름": {
            "retake": "NO",
            "remote": "YES",
            "QR": "YES",
            "time": 15,
            "img": "/static/icons/brand/하루필름.png",
            "liked_img": "/static/icons/liked/haru_liked.png",
        },
        "포토이즘박스": {
            "retake": "NO",
            "remote": "YES",
            "QR": "YES",
            "time": 10,
            "img": "/static/icons/brand/포토이즘.png",
            "liked_img": "/static/icons/liked/photoism_liked.png",
        },
    }

    for key in brand_dict.keys():
        name = brand_dict[key]
        new = Brand(name = key, retake = name["retake"], remote = name["remote"], QR = name["QR"], time = name["time"], img = name["img"], liked_img = name["liked_img"])
        new.save()

# frame 등록
def frame():
    frame_dict = {
        "frame1" : {
            "frame": 4,
            "take": 4,
            "price": 4000,
            "etc": "",
            "brand": ["인생네컷", "포토시그니처"]
        },
        "frame2": {
            "frame": 4,
            "take": 6,
            "price": 4000,
            "etc": "",
            "brand": ["하루필름", "셀픽스"]
        },
        "frame3": {
            "frame": 4,
            "take": 8,
            "price": 4000,
            "etc": "",
            "brand": ["포토이즘박스"]
        },
        "frame4": {
            "frame": 4,
            "take": 4,
            "price": 5000,
            "etc": "디즈니(인생네컷), 특수프레임(포토시그니처)",
            "brand": ["인생네컷", "포토시그니처"]
        },
        "frame5": {
            "frame": 6,
            "take": 10,
            "price": 4000,
            "etc": "",
            "brand": ["포토시그니처"]
        },
        "frame6": {
            "frame": 6,
            "take": 10,
            "price": 5000,
            "etc": "특수프레임(포토시그니처)",
            "brand": ["포토이즘박스", "하루필름", "포토시그니처"]
        },
        "frame7": {
            "frame": 4,
            "take": 10,
            "price": 5000,
            "etc": "4cut profile(하루필름)",
            "brand": ["하루필름"]

        },
        "frame8": {
            "frame": 8,
            "take": 6,
            "price": 6000,
            "etc": "증명사진(하루필름)",
            "brand": ["하루필름"]
        },
        "frame9": {
            "frame": 6,
            "take": 6,
            "price": 4000,
            "etc": "6장 중 3장 선택(셀픽스)",
            "brand": ["셀픽스"]
        },
        "frame10": {
            "frame": 1,
            "take": 6,
            "price": 5000,
            "etc": "전신",
            "brand": ["셀픽스"]
        },
        "frame11": {
            "frame": 4,
            "take": 6,
            "price": 5000,
            "etc": "전신",
            "brand": ["셀픽스"]
        },
    }

    for key in frame_dict.keys():
        name = frame_dict[key]
        
        for brandName in name["brand"]:
            brand = Brand.objects.get(name = brandName)  
            new = Frame(name = key, frame = name["frame"], take = name["take"], price = name["price"], etc = name["etc"], brand = brand)
            new.save()


def setBooth():
    brand_dict = {"인생네컷": "lifefourcut", "포토이즘박스": "photoism", "포토시그니처": "photosignature", "셀픽스": "selfix", "하루필름": "harufilm"}
    for key, value in brand_dict.items():
        path = 'booth_data/'+ str(value) + '.csv'
        df = pd.read_csv(path, index_col=0, sep=",")

        booth_list = df.to_dict('records')
        for booth_detail in booth_list:
            brand = Brand.objects.get(name = booth_detail['brand'])
    
            if type(booth_detail['operationHour']) != float:
                new_booth = Booth(name = booth_detail['name'], location = booth_detail['location'], operationHour = booth_detail['operationHour'], brand = brand, x = booth_detail['y'], y = booth_detail['x'])
                new_booth.save()
            else:
                new_booth = Booth(name = booth_detail['name'], location = booth_detail['location'], brand = brand, x = booth_detail['y'], y = booth_detail['x'])
                new_booth.save()
    print("DB 세팅 완료")


brand()
frame()
setBooth()