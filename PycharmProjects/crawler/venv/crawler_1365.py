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
en_seouls = [
    'jongro', 'jung', 'yongsan', 'seongdong', 'gwangjin', 'dongdaemun', 'jungrang', 'seongbuk', 'gangbuk', 'dobong',
    'nowon', 'eunpyeong', 'seodaemun', 'mapo', 'yangcheon', 'gangseo', 'guro', 'geumcheon', 'yeongdeungpo', 'dongjak',
    'gwanak', 'seocho', 'gangnam', 'songpa', 'gangdong'
]
busans = [
    '사하구', '사상구', '중구', '서구', '동구', '영도구', '부산진구', '동래구', '남구', '북구', '해운대구', '금정구',
    '강서구', '연제구', '수영구', '기장군',
]
en_busans = [
    'saha', 'sasang', 'jung', 'seo', 'dong', 'yeongdo', 'busanjin', 'dongrae', 'nam', 'buk', 'haeundae', 'geumjeong',
    'gangseo', 'yeonje', 'suyeong', 'gijang'
]
daegus = ['중구', '동구', '서구', '남구', '북구', '수성구', '달서구', '달성군']
en_daegus = ['jung', 'dong', 'seo', 'nam', 'buk', 'suseong', 'dalseo', 'dalseong']
incheons = ['중구', '동구', '미추홀구', '연수구', '남동구', '부평구', '계양구', '서구', '강화군', '옹진군']
en_incheons = ['jung', 'dong', 'michuhol', 'yeonsu', 'namdong', 'bupyeong', 'gyeyang', 'seo', 'ganghwa', 'ongjin']
gwangjus = ['동구', '서구', '남구', '북구', '광산구']
en_gwangjus = ['dong', 'seo', 'nam', 'buk', 'gwangsan']
daejeons = ['동구', '중구', '서구', '유성구', '대덕구']
en_daejeons = ['dong', 'jung', 'seo', 'yuseong', 'daeduk']
ulsans = ['중구', '남구', '동구', '북구', '울주군']
en_ulsans = ['jung', 'nam', 'dong', 'buk', 'ulju']
sejongs = ['세종시']
en_sejongs = ['sejong']
gyeonggis = [
    '수원시', '성남시', '고양시', '용인시', '부천시', '안산시', '안양시', '남양주시', '화성시', '평택시', '의정부시',
    '시흥시', '파주시', '광명시', '김포시', '군포시', '광주시', '이천시', '양주시', '오산시', '구리시', '안성시',
    '포천시', '의왕시', '하남시', '여주시', '양평군', '동두천시', '과천시', '가평군', '연천군',
]
en_gyeonggis = [
    'suwon', 'seongnam', 'goyang', 'yongin', 'bucheon', 'ansan', 'anyang', 'namyangju', 'hwaseong', 'pyeongtaek',
    'uijeongbu', 'siheung', 'paju', 'gwangmyeong', 'gimpo', 'gunpo', 'gwangju', 'icheon', 'yangju', 'osan', 'guri',
    'anseong', 'pocheon', 'uiwang', 'hanam', 'yeoju', 'yangpyeong', 'dongducheon', 'gwacheon', 'gapyeong', 'yeoncheon',
]
gangwons = [
    '춘천시', '원주시', '강릉시', '동해시', '태백시', '속초시', '삼척시', '홍천군', '횡성군', '영월군', '평창군',
    '정선군', '철원군', '화천군', '양구군', '인제군', '고성군', '양양군',
]
en_gangwons = [
    'chuncheon', 'wonju', 'gangreung', 'donghae', 'taebak', 'sokcho', 'samcheok', 'hongcheon', 'hoengseong', 'yeongwol',
    'pyeongchang', 'jeongseon', 'cheolwon', 'hwacheon', 'yanggu', 'inje', 'goseong', 'yangyang',
]
chungbuks = [
    '청주시', '충주시', '제천시', '보은군', '옥천군', '영동군', '증평군', '진천군', '괴산군', '음성군', '단양군',
]
en_chungbuks = [
    'cheongju', 'chungju', 'jecheon', 'boeun', 'okcheon', 'yeongdong', 'jeungpyeon', 'jincheon', 'goesan', 'eumseong',
    'danyang'
]
chungnams = [
    '천안시', '공주시', '보령시', '아산시', '서산시', '논산시', '계룡시', '당진시', '금산군', '부여군', '서천군',
    '청양군', '홍성군', '예산군', '태안군',
]
en_chungnams = [
    'cheonan', 'gongju', 'boryeong', 'asan', 'seosan', 'nonsan', 'gyeryong', 'danjin', 'geumsan', 'buyeo', 'seocheon',
    'cheongyang', 'hongseong', 'yesan', 'taean'
]
jeonbuks = [
    '전주시', '군산시', '익산시', '정읍시', '남원시', '김제시', '완주군', '진안군', '무주군', '장수군', '임실군',
    '순창군', '고창군', '부안군',
]
en_jeonbuks = [
    'jeonju', 'gunsan', 'iksan', 'jeongeup', 'namwon', 'gimje', 'wanju', 'jinan', 'muju', 'jangsu', 'imsil', 'sunchang',
    'gochang', 'buan'
]
jeonnams = [
    '목포시', '여수시', '순천시', '나주시', '광양시', '담양군', '곡성군', '구례군', '고흥군', '보성군', '화순군',
    '장흥군', '강진군', '해남군', '영암군', '무안군', '함평군', '영광군', '장성군', '완도군', '진도군', '신안군',
]
en_jeonnams = [
    'mokpo', 'yeosu', 'suncheon', 'naju', 'gwangyang', 'damyang', 'gokseong', 'gurye', 'goheung', 'boseong', 'hwasun',
    'jangheung', 'gangjin', 'haenam', 'yeongam', 'muan', 'hampyeong', 'yeonggwang', 'jangseong', 'wando', 'jindo',
    'sinan'
]
gyeongbuks = [
    '포항시', '경주시', '김천시', '안동시', '구미시', '영주시', '영천시', '상주시', '문경시', '경산시', '군위군',
    '의성군', '청송군', '영양군', '영덕군', '청도군', '고령군', '성주군', '칠곡군', '예천군', '봉화군', '울진군',
    '울릉군',
]
en_gyeongbuks = [
    'pohang', 'gyeongju', 'gimcheon', 'andong', 'gumi', 'yeongju', 'yeongcheon', 'sangju', 'mungyeong', 'gyeongsan',
    'gunwi', 'uiseong', 'chengsong', 'yeongyang', 'yeongdeok', 'cheongdo', 'goryeong', 'seongju', 'chilgok', 'yecheon',
    'bonghwa', 'uljin', 'ulreung',
]
gyeongnams = [
    '창원시', '진주시', '통영시', '사천시', '김해시', '밀양시', '거제시', '양산시', '의령군', '함안군', '창녕군',
    '고성군', '남해군', '하동군', '산청군', '함양군', '거창군', '합천군',
]
en_gyeongnams = [
    'changwon', 'jinju', 'tongyeong', 'sacheon', 'gimhae', 'milyang', 'geoje', 'yangsan', 'ulryeong', 'haman',
    'changnyeong', 'goseong', 'namhae', 'hadong', 'sancheong', 'hamyang', 'geochang', 'hapcheon'
]
jejus = ['제주시', '서귀포시']
jejus = ['jeju', 'seogwipo']

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

driver = webdriver.Chrome('C:/Users/LHG/PycharmProjects/crawler/chromedriver.exe')
r_num = 0
max_page = 1
dff = pd.DataFrame(['지역', '시군구', '제목', '모집기관', '봉사기간'])


def titl_filter(aaa):
    t_res = []
    for aa in aaa:
        aa2 = re.sub('<.+?>', '', aa.text, 0).strip()
        aa2 = re.sub(r'\([^)]*\)', '', aa2)
        aa2 = aa2.strip()
        t_res.append(aa2)
    return t_res


def inst_filter(i_list):
    i_res = []
    for inst in i_list:
        ins = re.sub('<.+?>', '', inst.text, 0).strip()
        ins = re.sub(':', '', ins).strip()
        i_res.append(ins)
    return i_res


def date_filter(d_list):
    d_res = []
    for date in d_list:
        day = re.sub('<.+?>', '', date.text, 0).strip()
        day = re.sub(':', '', day).strip()
        day = day[:10] + " ~ " + day[-10:]
        d_res.append(day)
    return d_res


def num_puri(r_su):
    r_su = r_su.text[:-1]
    r_su = re.sub(',', '', r_su)
    r_su = int(r_su)
    return r_su


def page_cal(r_su):
    r_su = r_su // 10
    r_su = r_su + 1
    return r_su


def crawler_1365():
    board_list = soup.select("#content > div.content_view > div > div.board_list.data_middle > ul > li > a > dl > dt")
    board_list = titl_filter(board_list)

    kikwan_list = soup.select(
        "#content > div.content_view > div > div.board_list.data_middle > ul > li > a > dl > dd.board_data > dl:nth-child(1) > dd")
    kikwan_list = inst_filter(kikwan_list)

    day_list = soup.select(
        "#content > div.content_view > div > div.board_list.data_middle > ul > li > a > dl > dd.board_data > dl:nth-child(3) > dd")
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

        driver.get('https://1365.go.kr/vols/P9210/partcptn/timeCptn.do')
        driver.find_element_by_xpath("//*[@id='searchHopeArea1']").send_keys(reg)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='searchHopeArea2']").send_keys(city)
        time.sleep(0.5)
        driver.find_element_by_css_selector("#btnSearch").click()
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        r_num = driver.find_element_by_css_selector(".search_result > p:nth-child(1) > em:nth-child(1)")
        r_num = num_puri(r_num)

        max_page = page_cal(r_num)
        now_page = 1
        while now_page <= max_page:
            print("@@@@@@@@@@@@ now on page " + str(now_page))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            pg_df = crawler_1365()
            gu_df = pd.concat([gu_df, pg_df])
            print("crawled " + str(now_page) + "/" + str(max_page))

            if now_page == max_page:
                now_page += 1
                continue
            else:
                driver.execute_script("fnPage(" + str(now_page + 1) + ");return false;")
                time.sleep(5)
                now_page += 1
        print('gu_df 프린트')
        print(gu_df)

        gu_df['지역'] = reg
        gu_df['시군구'] = city
        add_path = "C:/Users/LHG/PycharmProjects/untitled1/DB/addressDB/1365/" + reg + '/'
        addr_df = pd.read_csv(add_path + "/" + city + ".csv")
        addr_list = []
        inst_list = gu_df['모집기관'].tolist()

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
            path = "C:/Users/LHG/PycharmProjects/untitled1/DB/1365/" + reg + "/"
            access_rights = 0o707
            os.mkdir(path, access_rights)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)
        print(path)
        gu_align.to_json(path + city + ".json", orient='records')

