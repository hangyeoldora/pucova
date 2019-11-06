from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time
import os
import googlemaps

gmaps_key = 'AIzaSyD5sRAJgDzlXZrYVgvDC4TYVEnEpEe-Abg'
gmaps = googlemaps.Client(key=gmaps_key)

seouls = [
    '종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구',
    '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구',
    '강남구', '송파구', '강동구',
]
busans = [
    '사하구', '사상구', '중구', '서구', '동구', '영도구', '부산진구', '동래구', '남구', '북구', '해운대구', '금정구',
    '강서구', '연제구', '수영구', '기장군',
]
daegus = ['중구', '동구', '서구', '남구', '북구', '수성구', '달서구', '달성군']
incheons = ['중구', '동구', '미추홀구', '연수구', '남동구', '부평구', '계양구', '서구', '강화군', '옹진군']
gwangjus = ['동구', '서구', '남구', '북구', '광산구']
daejeons = ['동구', '중구', '서구', '유성구', '대덕구']
ulsans = ['중구', '남구', '동구', '북구', '울주군']
sejongs = ['세종시']
gyeonggis = [
    '수원시', '성남시', '고양시', '용인시', '부천시', '안산시', '안양시', '남양주시', '화성시', '평택시', '의정부시',
    '시흥시', '파주시', '광명시', '김포시', '군포시', '광주시', '이천시', '양주시', '오산시', '구리시', '안성시',
    '포천시', '의왕시', '하남시', '여주시', '양평군', '동두천시', '과천시', '가평군', '연천군',
]
gangwons = [
    '춘천시', '원주시', '강릉시', '동해시', '태백시', '속초시', '삼척시', '홍천군', '횡성군', '영월군', '평창군',
    '정선군', '철원군', '화천군', '양구군', '인제군', '고성군', '양양군',
]
chungbuks = [
    '청주시', '충주시', '제천시', '보은군', '옥천군', '영동군', '증평군', '진천군', '괴산군', '음성군', '단양군',
]
chungnams = [
    '천안시', '공주시', '보령시', '아산시', '서산시', '논산시', '계룡시', '당진시', '금산군', '부여군', '서천군',
    '청양군', '홍성군', '예산군', '태안군',
]
jeonbuks = [
    '전주시', '군산시', '익산시', '정읍시', '남원시', '김제시', '완주군', '진안군', '무주군', '장수군', '임실군',
    '순창군', '고창군', '부안군',
]
jeonnams = [
    '목포시', '여수시', '순천시', '나주시', '광양시', '담양군', '곡성군', '구례군', '고흥군', '보성군', '화순군',
    '장흥군', '강진군', '해남군', '영암군', '무안군', '함평군', '영광군', '장성군', '완도군', '진도군', '신안군',
]
gyeongbuks = [
    '포항시', '경주시', '김천시', '안동시', '구미시', '영주시', '영천시', '상주시', '문경시', '경산시', '군위군',
    '의성군', '청송군', '영양군', '영덕군', '청도군', '고령군', '성주군', '칠곡군', '예천군', '봉화군', '울진군',
    '울릉군',
]
gyeongnams = [
    '창원시', '진주시', '통영시', '사천시', '김해시', '밀양시', '거제시', '양산시', '의령군', '함안군', '창녕군',
    '고성군', '남해군', '하동군', '산청군', '함양군', '거창군', '합천군',
]
jejus = ['제주시', '서귀포시']

cities = [
    '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '세종특별자치시',
    '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'
]

regions = {
    '서울특별시': seouls, '부산광역시': busans, '대구광역시': daegus, '인천광역시': incheons, '광주광역시': gwangjus,
    '대전광역시': daejeons, '울산광역시': ulsans, '세종특별자치시': sejongs, '경기도': gyeonggis, '강원도': gangwons,
    '충청북도': chungbuks, '충청남도': chungnams, '전라북도': jeonbuks, '전라남도': jeonnams, '경상북도': gyeongbuks,
    '경상남도': gyeongnams, '제주특별자치도': jejus,
}

driver = webdriver.Chrome('C:/Users/LHG/PycharmProjects/untitled1/chromedriver.exe')
r_num = 0
max_page = 1

def ti_inst_filter(ti_list):
    ti_res = []
    for tinst in ti_list:
        tinst = re.sub('<.+?>', '', tinst.text, 0).strip()
        ti_res.append(tinst)
    return ti_res


def add_filter(a_list):
    ad_res = []
    for addr in a_list:
        addr = re.sub('<.+?>', '', addr.text, 0).strip()
        addr = re.sub(':', '', addr).strip()
        ad_res.append(addr)
    return ad_res


def num_puri(r_su):
    r_su = r_su.text[:-1]
    r_su = re.sub(',', '', r_su)
    r_su = int(r_su)
    return r_su


def page_cal(r_su):
    r_su = r_su // 10
    r_su = r_su + 1
    return r_su

def crawler_1365_ad():
    # 기관명 추출 시작
    # #content > div.content_view > div > div.board_list.non_sub > ul > li:nth-child(2) > a > dl > dt
    kikwan_list=soup.select("#content > div.content_view > div > div.board_list.non_sub > ul > li > a > dl > dt")
    kikwan_list = ti_inst_filter(kikwan_list)

    # 주소 추출
    # #content > div.content_view > div > div.board_list.non_sub > ul > li:nth-child(2) > a > dl > dd > dl.none.locaton > dd
    addres_list = soup.select(
        "#content > div.content_view > div > div.board_list.non_sub > ul > li > a > dl > dd > dl.none.locaton > dd")
    addres_list = add_filter(addres_list)

    result = {'기관': kikwan_list, '주소': addres_list}
    print(str(len(result['기관'])) + ", " + str(len(result['주소'])))
    print(result)
    df = pd.DataFrame(result, columns=['기관', '주소'])
    print(df)
    return df

for reg, cities in regions.items():
    print('--- crawling ' + reg + '\'s 기관 list ---')

    for city in cities:
        print(city)
        gu_df = pd.DataFrame(columns=['기관', '주소'])

        driver.get('https://1365.go.kr/vols/P9140/srvcinfo/volsDnttInfo.do')
        driver.find_element_by_xpath("//*[@id='srchSido']").send_keys(reg)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='srchSigu']").send_keys(city)
        time.sleep(0.5)
        # #searchFm > div > div > div > button
        driver.find_element_by_css_selector("#btnSearch").click()
        time.sleep(1.5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        r_num = driver.find_element_by_css_selector("#content > div.content_view > div > div.board_header > div > p > em")
        r_num = num_puri(r_num)

        max_page = page_cal(r_num)
        now_page = 1
        while now_page <= max_page:
            print("@@@@@@@@@@@@ now on page " + str(now_page))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            pg_df = crawler_1365_ad()
            gu_df = pd.concat([gu_df, pg_df])
            print("crawled " + str(now_page) + "/" + str(max_page))

            if now_page == max_page:
                now_page += 1
                continue
            else:
                driver.execute_script("fnPage(" + str(now_page + 1) + ");return false;")
                # time.sleep(2)
                time.sleep(1.5)
                now_page += 1
        print('gu_df 프린트')
        print(gu_df)

        gu_df['지역'] = reg
        gu_df['시군구'] = city
        gu_align = pd.DataFrame(gu_df, columns=['지역', '시군구', '기관', '주소'])
        try:
            path = "C:/Users/LHG/PycharmProjects/untitled1/DB/addressDB/1365/" + reg + "/"
            access_rights = 0o707
            os.mkdir(path, access_rights)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)
        # os.mkdir("C:/Users/yui/OneDrive/PycharmProjects/untitled1/venv/Scripts/" + cities[i] + "/")
        print(path)
        gu_align.to_csv(path + city + ".csv")
