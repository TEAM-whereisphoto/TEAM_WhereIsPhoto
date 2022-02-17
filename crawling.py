import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
import django
django.setup()
import requests

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from map.models import Booth
from brand.models import Brand, Frame

# 드라이버 세팅
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# brand 검색
def search(brand):
    input_selector = "search\.keyword\.query"
    search_btn_selector = "search.keyword.submit"

    driver.get(url="https://map.kakao.com/")
    driver.find_element(By.ID, input_selector).send_keys(brand)
    if (brand == "인생네컷"):
        driver.find_element(By.ID, "dimmedLayer").click()
    driver.find_element(By.ID, search_btn_selector).click() 


# list에 정보 저장
def store_booth(booths_list, brand, brand_list):
    for booth in booths_list:
        if brand in booth.find_element(By.CSS_SELECTOR, "div.head_item.clickArea > strong > a.link_name").text:
            name = booth.find_element(By.CSS_SELECTOR, "div.head_item.clickArea > strong > a.link_name").text
            location = booth.find_element(By.CSS_SELECTOR, "div.info_item > div.addr > p:nth-child(1)").text
            operationHour= booth.find_element(By.CSS_SELECTOR, "div.info_item > div.openhour > p > a").text
            x, y= getXY(location)

            brand_list[name] = {
                    "location": location,
                    "operationHour": operationHour,
                    "brand": brand,
                    "x": x,
                    "y": y
                }


# crawling
def crawling(brand):
    brand_dict = {}
    Flag = True
    idx = 1
    while Flag:
        # 더보기 클릭
        if idx == 1:
            if "HIDDEN" in driver.find_element(By.ID, "info.search.place.more").get_attribute("class"):
                booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
                store_booth(booths_list, brand, brand_dict)
                Flag = False
            else:
                booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
                store_booth(booths_list, brand, brand_dict)
                driver.find_element(By.ID, "info.search.place.more").click()
                idx += 1

        # 종료 조건 -> 다음 번호에 hidden이라는 class 있으면 종료
        elif "HIDDEN" in driver.find_element(By.ID, "info.search.page.no" + str(idx % 5 + 1)).get_attribute("class"):
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_dict)
            Flag = False

        # next btn
        elif idx % 5 == 0:
            if "disabled" in driver.find_element(By.ID, "info.search.page.next").get_attribute("class"):
                booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
                store_booth(booths_list, brand, brand_dict)
                Flag = False
            else:
                booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
                store_booth(booths_list, brand, brand_dict)
                driver.find_element(By.ID, "info.search.page.next").click()
                idx += 1

        else:
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_dict)
            driver.find_element(By.ID, "info.search.page.no" + str(idx % 5 + 1)).click()
            idx += 1

        time.sleep(1)
    return brand_dict


def main():
    brand_dict = {"인생네컷": "lifefourcut", "포토이즘박스": "photoism", "포토시그니처": "photosignature", "셀픽스": "selfix", "하루필름": "harufilm"}
    
    logic_search = "search(brand)"
    logic_crawling = "globals()['{}_dict'.format(eng)] = crawling(brand)"

    for brand, eng in brand_dict.items():
        exec(logic_search)
        exec(logic_crawling)

    # {eng_name} = {boothname: {location: , operation_hour: , brand: }}

    brand_dict_list = [lifefourcut_dict, photoism_dict, photosignature_dict, selfix_dict, harufilm_dict]
    for dict in brand_dict_list:
        for key, value in dict.items():
            brand = Brand.objects.get(name = value['brand'])  
            if value['operationHour'] != '':
                key = Booth(name = key, location = value['location'], operationHour = value['operationHour'], brand = brand, x = value['x'], y = value['y'])
                key.save()
            else:
                key = Booth(name = key, location = value['location'], brand = brand, x = value['x'], y = value['y'])
                key.save()


# brand 등록W
def brand():
    brand_dict = {
        "인생네컷": {
            "retake": "YES",
            "remote": "YES",
            "QR": "YES",
            "time": 10,
            "img": "/media/brand/인생네컷.png"
        },
        "셀픽스":{
            "retake": "YES",
            "remote": "YES",
            "QR": "YES",
            "time": 20,
            "img": "/media/brand/셀픽스.png"
        },
        "포토시그니처": {
            "retake": "YES",
            "remote": "YES",
            "QR": "YES",
            "time": 10,
            "img": "/media/brand/포토시그니쳐.png"
        },
        "하루필름": {
            "retake": "NO",
            "remote": "YES",
            "QR": "YES",
            "time": 15,
            "img": "/media/brand/하루필름.png"
        },
        "포토이즘박스": {
            "retake": "NO",
            "remote": "YES",
            "QR": "YES",
            "time": 10,
            "img": "/media/brand/포토이즘.png"
        },
    }

    for key in brand_dict.keys():
        name = brand_dict[key]
        new = Brand(name = key, retake = name["retake"], remote = name["remote"], QR = name["QR"], time = name["time"], img = name["img"])
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


# 주소 -> 좌표
def getXY(address):
    result = ""
    if address == "인천 미추홀구 숙골로87번길 5 5블럭 1층 40호":
        address = "인천 미추홀구 숙골로87번길 5"

    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    API_KEY = '970791aa193813b80b02a98d2a78907d'
    header = {'Authorization': 'KakaoAK ' + API_KEY}
    req = requests.get(url, headers = header)

    if req.status_code == 200:
        result_address = req.json()["documents"][0]["address"]

        result = result_address["y"], result_address["x"]
    else:
        result = "ERROR[" + str(req.status_code) + "]"
    
    return result

driver = set_chrome_driver()
driver.implicitly_wait(5)

brand()
frame()
main()

driver.close()









