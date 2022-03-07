import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
import django
django.setup()
import requests

import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from django.conf import settings
from map.models import Booth
from brand.models import Brand, Frame

# 드라이버 세팅
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# brand 검색
def search(brand):
    input_selector = "search.keyword.query"
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
            brand_list.append({
                "name": name,
                "location": location,
                "operationHour": operationHour,
                "brand": brand,
                "x": x,
                "y": y
                })
            print(name)



# crawling
def crawling(brand):
    brand_list = []
    Flag = True
    idx = 1
    while Flag:
        # 더보기 클릭
        if idx == 1:
            if "HIDDEN" in driver.find_element(By.ID, "info.search.place.more").get_attribute("class"):
                booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
                store_booth(booths_list, brand, brand_list)
                Flag = False
            else:
                booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
                store_booth(booths_list, brand, brand_list)
                driver.find_element(By.ID, "info.search.place.more").click()
                idx += 1

        # 종료 조건 -> 다음 번호에 hidden이라는 class 있으면 종료
        elif "HIDDEN" in driver.find_element(By.ID, "info.search.page.no" + str(idx % 5 + 1)).get_attribute("class"):
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_list)
            Flag = False

        # next btn
        elif idx % 5 == 0:
            if "disabled" in driver.find_element(By.ID, "info.search.page.next").get_attribute("class"):
                booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
                store_booth(booths_list, brand, brand_list)
                Flag = False
            else:
                booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
                store_booth(booths_list, brand, brand_list)
                driver.find_element(By.ID, "info.search.page.next").click()
                idx += 1

        else:
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_list)
            driver.find_element(By.ID, "info.search.page.no" + str(idx % 5 + 1)).click()
            idx += 1

        time.sleep(1)
    return brand_list


def main():
    brand_dict = {"인생네컷": "lifefourcut", "포토이즘박스": "photoism", "포토시그니처": "photosignature", "셀픽스": "selfix", "하루필름": "harufilm"}
    
    for brand, eng in brand_dict.items():
        search(brand)
        df = pd.DataFrame(crawling(brand))
        df.to_csv(f"booth_data\{eng}.csv")

# 주소 -> 좌표
def getXY(address):
    result = ""
    if address == "인천 미추홀구 숙골로87번길 5 5블럭 1층 40호":
        address = "인천 미추홀구 숙골로87번길 5"

    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    API_KEY = settings.KAKAO_SECRET_KEY
    header = {'Authorization': 'KakaoAK ' + API_KEY}
    req = requests.get(url, headers = header)
    if req.status_code == 200:
        result_address = req.json()["documents"][0]["address"]
        result = result_address["x"], result_address["y"]
    else:
        result = "ERROR[" + str(req.status_code) + "]", "ERROR[" + str(req.status_code) + "]"

    return result

driver = set_chrome_driver()
driver.implicitly_wait(3)


main()

driver.close()









