import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


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
            brand_list.append(
                {
                    "name": booth.find_element(By.CSS_SELECTOR, "div.head_item.clickArea > strong > a.link_name").text,
                    "location": booth.find_element(By.CSS_SELECTOR, "div.info_item > div.addr > p:nth-child(1)").text,
                    "operationHour": booth.find_element(By.CSS_SELECTOR, "div.info_item > div.openhour > p > a").text,
                    "brand": brand
                }
            )


# crawling
def crawling(brand, brand_list):
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

        # next btn
        elif idx % 5 == 0:
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_list)
            driver.find_element(By.ID, "info.search.page.next").click()
            idx += 1

        # 종료 조건 -> 다음 번호에 hidden이라는 class 있으면 종료
        elif "HIDDEN" in driver.find_element(By.ID, "info.search.page.no" + str(idx % 5 + 1)).get_attribute("class"):
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_list)
            Flag = False

        else:
            booths_list = driver.find_elements(By.CLASS_NAME, "PlaceItem")
            store_booth(booths_list, brand, brand_list)
            driver.find_element(By.ID, "info.search.page.no" + str(idx % 5 + 1)).click()
            idx += 1

        time.sleep(1)

    return brand_list


def main():
    # 인생네컷
    lifefourcut_list = []
    search("인생네컷")
    lifefourcut_list = crawling("인생네컷", lifefourcut_list)
    df = pd.DataFrame(lifefourcut_list)
    df.to_csv("booth_data\lifefourcut.csv")

    # 포토이즘
    photoism_list = []
    search("포토이즘")
    photoism_list = crawling("포토이즘", photoism_list)
    df = pd.DataFrame(photoism_list)
    df.to_csv("booth_data\photoism.csv")

    # 포토시그니처
    photosignature_list = []
    search("포토시그니처")
    photosignature_list = crawling("포토시그니처", photosignature_list)
    df = pd.DataFrame(photosignature_list)
    df.to_csv("booth_data\photosignature.csv")

    # 셀픽스
    selfix_list = []
    search("셀픽스")
    selfix_list = crawling("셀픽스", selfix_list)
    df = pd.DataFrame(selfix_list)
    df.to_csv("booth_data\selfix.csv")

    # # 폴라스튜디오
    # polarstudio_list = []
    # search("폴라스튜디오")
    # polarstudio_list = crawling("폴라스튜디오", polarstudio_list)
    # df = pd.DataFrame(polarstudio_list)
    # df.to_csv("booth_data\polarstudio.csv")


driver = set_chrome_driver()
driver.implicitly_wait(3)

main()










