from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import requests
import re

a_res = []
n_res = []
t_res = []


def titl_filter(h_list):
    ko_1 = re.compile('[^ ㄱ-ㅣ가-힣\(\)\[\]\<\>]+')
    result = ko_1.sub('', h_list)
    t_res.append(result)


def inst_filter(o_list):
    ko_1 = re.compile('[^ ㄱ-ㅣ가-힣\(\)\[\]\<\>]+')
    result = ko_1.sub('', o_list)
    a_res.append(result)


def date_filter(n_list):
    ko_1 = re.compile('[^ 0-9\(\)\[\]\<\>\-]+')
    result = ko_1.sub('', n_list)
    n_res.append(result)



def crawler_1365():
    # BoardList 추출 시작
    board_list = soup.select("#content > div.content_view > div > div.board_list.data_middle > ul > li > a > dl > dt")

    # 리스트에서 공고문 제목 한글만 추출 시작

    for board in board_list:
        titl_filter(board.text)

    print(t_res)
    # 리스트에서 공고문 제목 한글만 추출 끝

    # BoardList에 각 해당하는 모집기관 주소 추출 시작
    area_list = soup.select(
        "#content > div.content_view > div > div.board_list.data_middle > ul > li > a > dl > dd.board_data > dl:nth-child(1) > dd")

    for area in area_list:
        inst_filter(area.text)

    print(a_res)
    # BoardList에 각 해당하는 모집기관 주소 추출 끝

    # 기간 추출
    num_list = soup.select(
        "#content > div.content_view > div > div.board_list.data_middle > ul > li > a > dl > dd.board_data > dl:nth-child(3) > dd")

    for num in num_list:
        date_filter(num.text)

    print(n_res)


driver=webdriver.Chrome('C:/Users/yui/OneDrive/PycharmProjects/untitled1/chromedriver.exe')
driver.get('https://1365.go.kr/vols/P9210/partcptn/timeCptn.do')
driver.find_element_by_xpath("//*[@id='searchHopeArea1']").send_keys("부산광역시")
time.sleep(0.3)
driver.find_element_by_xpath("//*[@id='searchHopeArea2']").send_keys("사하구")
time.sleep(0.3)
driver.find_element_by_css_selector("#btnSearch").click()
time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

crawler_1365()

num = soup.find("# content > div.content_view > div > div.board_header > div > p > em")
print(num)
int(num)
pagenum = (num // 10) + 1

driver.execute_script("fnPage(" + "2" + ");return false;")


# try:
#     element = WebDriverWait(driver, 10).until(
#         # By.ID 는 ID로 검색, By.CSS_SELECTOR 는 CSS Selector 로 검색
#         EC.presence_of_element_located((By.CSS_SELECTOR, "#searchHopeArea2 > option:nth-child(2)"))
#     )
# except TimeoutException:
#     print("타임아웃")
# finally:
#     driver.quit()
