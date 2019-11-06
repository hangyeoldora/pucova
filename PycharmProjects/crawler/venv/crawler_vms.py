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

cities = [
    '서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남',
    '경북', '경남', '제주'
]

seouls = [
    '서울특별시 종로구', '서울특별시 중구', '서울특별시 용산구', '서울특별시 성동구', '서울특별시 광진구',
    '서울특별시 동대문구', '서울특별시 중랑구', '서울특별시 성북구', '서울특별시 강북구', '서울특별시 도봉구',
    '서울특별시 노원구', '서울특별시 은평구', '서울특별시 서대문구', '서울특별시 마포구', '서울특별시 양천구',
    '서울특별시 강서구', '서울특별시 구로구', '서울특별시 금천구', '서울특별시 영등포구', '서울특별시 동작구',
    '서울특별시 관악구', '서울특별시 서초구', '서울특별시 강남구', '서울특별시 송파구', '서울특별시 강동구',
]
busans = [
    '부산광역시 중구', '부산광역시 서구', '부산광역시 동구', '부산광역시 영도구', '부산광역시 부산진구',
    '부산광역시 동래구', '부산광역시 남구', '부산광역시 북구', '부산광역시 해운대구', '부산광역시 사하구',
    '부산광역시 금정구', '부산광역시 강서구', '부산광역시 연제구', '부산광역시 수영구', '부산광역시 사상구',
    '부산광역시 기장군'
]
daegus = [
    '대구광역시 중구', '대구광역시 동구', '대구광역시 서구', '대구광역시 남구', '대구광역시 북구', '대구광역시 수성구',
    '대구광역시 달서구', '대구광역시 달성군',
]
incheons = [
    '인천광역시 중구', '인천광역시 동구', '인천광역시 미추홀구', '인천광역시 연수구', '인천광역시 남동구',
    '인천광역시 부평구', '인천광역시 계양구', '인천광역시 서구', '인천광역시 강화군', '인천광역시 옹진군',
]
gwangjus = ['광주광역시 동구', '광주광역시 서구', '광주광역시 남구', '광주광역시 북구', '광주광역시 광산구']
daejeons = ['대전광역시 동구', '대전광역시 중구', '대전광역시 서구', '대전광역시 유성구', '대전광역시 대덕구']
ulsans = ['울산광역시 중구', '울산광역시 남구', '울산광역시 동구', '울산광역시 북구', '울산광역시 울주군']
sejongs = [
    '세종특별자치시 연기면', '세종특별자치시 연동면', '세종특별자치시 부강면', '세종특별자치시 금남면',
    '세종특별자치시 장군면', '세종특별자치시 연서면', '세종특별자치시 전의면', '세종특별자치시 전동면',
    '세종특별자치시 소정면',
]
gyeonggis = [
    '경기도 수원시', '경기도 수원시 장안구', '경기도 수원시 권선구', '경기도 수원시 팔달구', '경기도 수원시 영통구',
    '경기도 성남시', '경기도 성남시 수정구', '경기도 성남시 중원구', '경기도 성남시 분당구', '경기도 의정부시',
    '경기도 안양시', '경기도 안양시 만안구', '경기도 안양시 동안구', '경기도 부천시', '경기도 광명시', '경기도 평택시',
    '경기도 동두천시', '경기도 안산시', '경기도 안산시 상록구', '경기도 안산시 단원구', '경기도 고양시',
    '경기도 고양시 덕양구', '경기도 고양시 일산동구', '경기도 고양시 일산서구', '경기도 과천시', '경기도 구리시',
    '경기도 남양주시', '경기도 오산시', '경기도 시흥시', '경기도 군포시', '경기도 의왕시', '경기도 하남시',
    '경기도 용인시', '경기도 용인시 처인구', '경기도 용인시 기흥구', '경기도 용인시 수지구', '경기도 파주시',
    '경기도 이천시', '경기도 안성시', '경기도 김포시', '경기도 화성시', '경기도 광주시', '경기도 양주시',
    '경기도 포천시', '경기도 여주시', '경기도 연천군', '경기도 가평군', '경기도 양평군',
]
gangwons = [
    '강원도 춘천시', '강원도 원주시', '강원도 강릉시', '강원도 동해시', '강원도 태백시', '강원도 속초시',
    '강원도 삼척시', '강원도 홍천군', '강원도 횡성군', '강원도 영월군', '강원도 평창군', '강원도 정선군',
    '강원도 철원군', '강원도 화천군', '강원도 양구군', '강원도 인제군', '강원도 고성군', '강원도 양양군',
]
chungbuks = [
    '충청북도 청주시', '충청북도 청주시 상당구', '충청북도 청주시 서원구', '충청북도 청주시 흥덕구',
    '충청북도 청주시 청원구', '충청북도 충주시', '충청북도 제천시', '충청북도 보은군', '충청북도 옥천군',
    '충청북도 영동군', '충청북도 증평군', '충청북도 진천군', '충청북도 괴산군', '충청북도 음성군', '충청북도 단양군',
]
chungnams = [
    '충청남도 천안시', '충청남도 공주시', '충청남도 보령시', '충청남도 아산시', '충청남도 서산시', '충청남도 논산시',
    '충청남도 계룡시', '충청남도 당진시', '충청남도 금산군', '충청남도 부여군', '충청남도 서천군', '충청남도 청양군',
    '충청남도 홍성군', '충청남도 예산군', '충청남도 태안군',
]
jeonbuks = [
    '전라북도 전주시', '전라북도 전주시 완산구', '전라북도 전주시 덕진구', '전라북도 군산시', '전라북도 익산시',
    '전라북도 정읍시', '전라북도 남원시', '전라북도 김제시', '전라북도 완주군', '전라북도 진안군', '전라북도 무주군',
    '전라북도 장수군', '전라북도 임실군', '전라북도 순창군', '전라북도 고창군', '전라북도 부안군',
]
jeonnams = [
    '전라남도 목포시', '전라남도 여수시', '전라남도 순천시', '전라남도 나주시', '전라남도 광양시', '전라남도 담양군',
    '전라남도 곡성군', '전라남도 구례군', '전라남도 고흥군', '전라남도 보성군', '전라남도 화순군', '전라남도 장흥군',
    '전라남도 강진군', '전라남도 해남군', '전라남도 영암군', '전라남도 무안군', '전라남도 함평군', '전라남도 영광군',
    '전라남도 장성군', '전라남도 완도군', '전라남도 진도군', '전라남도 신안군',
]
gyeongbuks = [
    '경상북도 포항시', '경상북도 포항시 남구', '경상북도 포항시 북구', '경상북도 경주시', '경상북도 김천시',
    '경상북도 안동시', '경상북도 구미시', '경상북도 영주시', '경상북도 영천시', '경상북도 상주시', '경상북도 문경시',
    '경상북도 경산시', '경상북도 군위군', '경상북도 의성군', '경상북도 청송군', '경상북도 영양군', '경상북도 영덕군',
    '경상북도 청도군', '경상북도 고령군', '경상북도 성주군', '경상북도 칠곡군', '경상북도 예천군', '경상북도 봉화군',
    '경상북도 울진군', '경상북도 울릉군',
]
gyeongnams = [
    '경상남도 창원시', '경상남도 진주시', '경상남도 통영시', '경상남도 사천시', '경상남도 김해시', '경상남도 밀양시',
    '경상남도 거제시', '경상남도 양산시', '경상남도 의령군', '경상남도 함안군', '경상남도 창녕군', '경상남도 고성군',
    '경상남도 남해군', '경상남도 하동군', '경상남도 산청군', '경상남도 함양군', '경상남도 거창군', '경상남도 합천군',
]
jejus = ['제주특별자치도 제주시', '제주특별자치도 서귀포시']

regions = {
    '부산': busans, '대구': daegus, '인천': incheons, '광주': gwangjus, '대전': daejeons,
    '울산': ulsans, '세종': sejongs, '경기': gyeonggis, '강원': gangwons, '충북': chungbuks, '충남': chungnams,
    '전북': jeonbuks, '전남': jeonnams, '경북': gyeongbuks, '경남': gyeongnams, '제주': jejus,
}

driver = webdriver.Chrome('C:/Users/LHG/PycharmProjects/untitled1/chromedriver.exe')
r_num = 0
max_page = 1
dff = pd.DataFrame(['지역', '시군구', '제목', '모집기관', '봉사기간'])

def titl_filter(t_list):
    t_res = []
    for titl in t_list:
        ko_1 = re.compile('[^ ㄱ-ㅣ가-힣\(\)\[\]\<\>]+')
        result=ko_1.sub('', titl.text)
        result = re.sub('새로운글', '', result)
        t_res.append(result)
    return t_res


def inst_filter(i_list):
    i_res = []
    for inst in i_list:
        ko_1 = re.compile('[^ ㄱ-ㅣ가-힣\(\)\[\]\<\>]+')
        result = ko_1.sub('', inst.text)
        i_res.append(result)
    return i_res


def date_filter(d_list):
    d_res = []
    for date in d_list:
        ko_1 = re.compile('[^ 0-9\(\)\[\]\<\>\-]+')
        result = ko_1.sub('', date.text)
        d_res.append(result)
    return d_res


def num_puri(r_su):
    r_su = re.sub(',', '', r_su.text)
    r_su = int(r_su)
    return r_su


def page_cal(r_su):
    r_su = r_su // 15
    r_su = r_su + 1
    return r_su


def crawler_vms():
    board_list=soup.select("#rightArea > div.con > div.boardList.boardListService > ul > li > a > p")
    board_list = titl_filter(board_list)

    kikwan_list = soup.select(
        "#rightArea > div.con > div.boardList.boardListService > ul > li > a > div.data.clear > dl:nth-child(3) > dd")
    kikwan_list = inst_filter(kikwan_list)

    day_list = soup.select(
        "#rightArea > div.con > div.boardList.boardListService > ul > li > a > div.data.clear > dl:nth-child(2) > dd")
    day_list = date_filter(day_list)

    result = {'제목': board_list, '모집기관': kikwan_list, '봉사기간': day_list}
    print(str(len(result['제목'])) + ", " + str(len(result['모집기관'])) + ", " + str(len(result['봉사기간'])))
    print(result)
    df = pd.DataFrame(result, columns=['제목', '모집기관', '봉사기간'])
    print(df)
    return df

for reg, cities in regions.items():
    print('--- crawling ' + reg + '---')

    for city in cities:
        print(city)
        gu_df = pd.DataFrame(columns=['제목', '모집기관', '봉사기간'])

        driver.get('https://www.vms.or.kr/partspace/recruit.do')
        driver.find_element_by_xpath("//*[@id='area']").send_keys(reg)
        time.sleep(1)
        driver.find_element_by_css_selector("#searchFm > div.tc.btn_search > button").click()
        err_num = driver.find_element_by_css_selector("#rightArea > div.con > div.searchForm.searchFormTop.clear > p > span")
        err_num = num_puri(err_num)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='areagugun']").send_keys(city)
        time.sleep(0.5)
        driver.find_element_by_css_selector("#searchFm > div.tc.btn_search > button").click()
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        r_num = driver.find_element_by_css_selector("#rightArea > div.con > div.searchForm.searchFormTop.clear > p > span")
        r_num = num_puri(r_num)
        if r_num == err_num:
            driver.find_element_by_xpath("//*[@id='area']").send_keys(reg)
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='areagugun']").send_keys(city)
            time.sleep(0.5)
            driver.find_element_by_css_selector("#searchFm > div.tc.btn_search > button").click()
            time.sleep(5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
        else:
            print(str(r_num) + str(err_num))

        max_page = page_cal(r_num)
        now_page = 1
        while now_page <= max_page:
            print("@@@@@@@@@@@@ now on page " + str(now_page))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            pg_df = crawler_vms()
            gu_df = pd.concat([gu_df, pg_df])
            print("crawled " + str(now_page) + "/" + str(max_page))

            if now_page == max_page:
                now_page += 1
                continue
            else:
                driver.execute_script("goPage(" + str(now_page + 1) + "); return false;")
                # time.sleep(2)
                time.sleep(5)
                now_page += 1
        print('gu_df 프린트')
        print(gu_df)

        gu_df['지역'] = reg
        gu_df['시군구'] = city
        add_path = "C:/Users/LHG/PycharmProjects/untitled1/DB/addressDB/VMS/" + reg
        addr_df = pd.read_csv(add_path + "/" + city + ".csv")
        addr_list = []
        inst_list = gu_df["모집기관"].tolist()

        for inst in inst_list:
            try:
                aaa = addr_df.loc[addr_df['기관']  == inst]
                bbb = addr_df.loc[addr_df['기관'] == inst, '주소'].values[0]

            except IndexError:
                print("해당 시군구 안에 모집처가 없습니다.")
                bbb = '없음'

            print("aaaaaaaaaaa  " + bbb)
            addr_list.append(bbb)
        gu_df['주소'] = addr_list
        gu_df.head()
        print(gu_df['주소'])

        for name in gu_df.주소:
            tmp = gmaps.geocode(name, language='ko')
            try:
                gu_df.loc[gu_df['주소']==name, 'formatted_address']=tmp[0].get("formatted_address")
                tmp_loc = tmp[0].get("geometry")
                gu_df.loc[gu_df['주소'] == name, 'lat'] = tmp_loc['location']['lat']
                gu_df.loc[gu_df['주소'] == name, 'lng'] = tmp_loc['location']['lng']
            except IndexError:
                print(tmp)
                pass
        gu_df.head()

        gu_align = pd.DataFrame(gu_df, columns=['시군구', 'lat', 'lng', '제목', '모집기관', 'formatted_address', '봉사기간'])
        try:
            path = "C:/Users/LHG/PycharmProjects/untitled1/DB/VMS/" + reg + "/"
            access_rights = 0o707
            os.mkdir(path, access_rights)
        except OSError:
                print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)

        gu_align.to_csv(path + city + ".csv")
