import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
import django
django.setup()

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from map.models import Booth
from brand.models import Brand
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
            brand_list[name] = {
                    "location": location,
                    "operationHour": operationHour,
                    "brand": brand
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

        # next btn
        elif idx % 5 == 0:
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_dict)
            driver.find_element(By.ID, "info.search.page.next").click()
            idx += 1

        # 종료 조건 -> 다음 번호에 hidden이라는 class 있으면 종료
        elif "HIDDEN" in driver.find_element(By.ID, "info.search.page.no" + str(idx % 5 + 1)).get_attribute("class"):
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_dict)
            Flag = False

        else:
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_dict)
            driver.find_element(By.ID, "info.search.page.no" + str(idx % 5 + 1)).click()
            idx += 1

        time.sleep(1)

    return brand_dict


def main():

    brand_dict = {"인생네컷": "lifefourcut", "포토이즘": "photoism", "포토시그니처": "photosignature", "셀픽스": "selfix"}

    # brand_dict에 있는거 등록, 나머지는 임의 값
    for key in brand_dict:
        new = Brand(name=key, retake=0, time=0, remote=0, price=0, QR=0)
        new.save()

    logic_search = "search(brand)"
    logic_crawling = "globals()['{}_dict'.format(eng)] = crawling(brand)"

    for brand, eng in brand_dict.items():
        exec(logic_search)
        exec(logic_crawling)

# {eng_name} = {boothname: {location: , operation_hour: , brand: }}

    brand_dict_list = [lifefourcut_dict, photoism_dict, photosignature_dict, selfix_dict]
    for dict in brand_dict_list:
        for key, value in dict.items():
            brand = Brand.objects.get(name = value['brand'])  
            if value['operationHour'] != '':
                key = Booth(name = key, location = value['location'], operationHour = value['operationHour'], brand = brand)
                key.save()
            else:
                key = Booth(name = key, location = value['location'], brand = brand)
                key.save()



driver = set_chrome_driver()
driver.implicitly_wait(3)

main()
driver.close()









