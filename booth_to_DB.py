# 호옥시 crawling.py가 안될때 임시로 등록해서 사용하세요!

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
import django
django.setup()

import pandas as pd
from map.models import Booth
from brand.models import Brand


# 사용법 (초기 db에 아무 것도 없다 가정(brand랑 booth에))
# 0. pip install pandas 해주기 !!
# 1. python manage.py makemigrations
# 2. python manage.py migrate
# 3. python booth_to_DB.py (현재 파일) 실행
# 4. 제대로 등록됐는지 확인



# 25-30 line은 규리꺼 pull&merge하기 전까지 임시로 사용 -------------------------------------------

# 1) 브랜드 종류 등록하기 
brand_dict = {"인생네컷": "lifefourcut", "포토이즘": "photoism", "포토시그니처": "photosignature", "셀픽스": "selfix"}

# brand_dict에 있는거 등록, 나머지는 임의 값
for key in brand_dict:
    new = Brand(name = key, retake = 0, time = 0, remote = 0, price = 0, QR = 0)
    new.save()

print("brand model 등록 완료!\n")
# ------------------------------------------------------------------------------


# 2) 크롤링해놓은 csv 파일 받아오기
brand_df_list = []
for key, value in brand_dict.items():
    path = 'booth_data/'+ str(value) + '.csv'
    globals()['{}'.format(value)] = pd.read_csv(path)
    brand_df_list.append(globals()['{}'.format(value)])
print("크롤링 csv를 받아왔습니다.")


# 3) booth들 등록하기
# brand_df_list에 있는 브랜드별 dataframe 등록
for brand_df in brand_df_list:
    for index, value in brand_df.iterrows():
        brand = Brand.objects.get(name = value['brand'])  
        if value['operationHour'] != '':
            key = Booth(name = value['name'], location = value['location'], operationHour = value['operationHour'], brand = brand)
            key.save()
        else:
            key = Booth(name = value['name'], location = value['location'], brand = brand)
print("booth 등록 완료!")