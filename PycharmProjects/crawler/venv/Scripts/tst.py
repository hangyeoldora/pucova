import re

def titl_filter(h_list):
    html_t1 = re.compile('<dt class=\"tit_board_list\">')
    ht1 = html_t1.sub('', h_list)
    html_t2 = re.compile("</dt>")
    html_t3 = re.compile('<em class="em">' + '(' + '모집중' + ')' + '</em>')
    ht2 = html_t2.sub('', ht1)
    ht3 = html_t3.sub('', ht2)
    ht4 = re.sub(r'\([^)]*\)', '', ht3)

    result = ht4.strip()
    return result
aa = "<dt class=\"tit_board_list\">"
aa +=""
aa +="										[종로]종로구 이화동 주민센터 방문 선별검진 기본정보조사 및 검진장소 안내 봉사활동"
aa +="										<em class=\"em\">(모집중)</em>"
aa +="</dt>"



# # titl_filter(aa)
# aa = re.sub('<.+?>', '', aa, 0).strip()
# aa = re.sub(r'\([^)]*\)', '', aa)
# aa = aa.strip()
# print('\'' + aa + '\'')

print('\'' + aa + '\'')
aaa = []
aaa.append(aa)
aaa.append(aa)
aaa.append(aa)
aaa.append("<dt class=\"tit_board_list\">										[종로]종로구 마지막 주민센터 방문 선별검진 기본정보조사 및 검진장소 안내 봉사활동										<em class=\"em\">(모집중)</em></dt>")
bbb = []
def list_tester(aaa):
    while aaa:
        popped = aaa.pop()
        aa2 = re.sub('<.+?>', '', popped, 0).strip()
        aa2 = re.sub(r'\([^)]*\)', '', aa2)
        aa2 = aa2.strip()
        # global bbb
        bbb.append(aa2)
        bbb.reverse()

    return bbb

ccc = list_tester(aaa)
print(bbb)
print("------------@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@-----------")
print(ccc)

'2019-08-22
											 ~
											      2019-08-22'