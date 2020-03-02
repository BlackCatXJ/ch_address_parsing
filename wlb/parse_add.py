import pandas as pd
import re

AREA_SUFFIXES = ["自治区", "省", "市", "区", "县"]
PRO_CODE_LEN = 10
CIT_CODE_LEN = 15
DIS_CODE_LEN = 20
data = pd.DataFrame(pd.read_csv('wlb/area.txt', encoding='utf-8'))


def parse_address(text):
    address = {
        "province": "",
        "city": "",
        "district": "",
        "street": "",
        "other": ""
    }
    forward_segment(text ,"",address)
    index = f(address["district"],text)
    if index != -1:
        text = text[index:]
        mat = re.match(".*?(镇|街道|街|乡镇|区|乡)", text, flags=0)
        if mat is not None:
            span = mat.span()
            address["street"] = text[span[0]:span[1]]
            address["other"] = text[span[1]:]
    return address


def forward_segment(text, suffix,address):
    word_list = []
    i = 0
    while i < len(text):
        longest_word = text[i]
        for j in range(i + 1, len(text) + 1):
            word = text[i: j]
            if(suffix == ""):
                if word in data['name'].values:
                    set_address(word,address)
                    longest_word = word
                    break
            else:
                for suf in AREA_SUFFIXES:
                    if word+suf in data['name'].values:
                        set_address(word+suf, address)
                        longest_word = word
                        break

        word_list.append(longest_word)
        i += len(longest_word)
    return word_list


def set_address(word,address):
    index = list(data['name']).index(word)
    code = '0000'+str(data['code'][index])
    if len(code) == PRO_CODE_LEN and address['province'] == "":
        address['province'] = word
    elif len(code) == CIT_CODE_LEN and address['city'] == "":
        address['city'] = word
    elif len(code) == DIS_CODE_LEN and address['district'] == "":
        address['district'] = word


def f(area,text):
    temp = text.find(area)
    if temp ==-1:
        for s in AREA_SUFFIXES:
            tmp=area.replace(s,"")
            temp=text.find(tmp)
            if temp == -1:
                continue
            else: return temp+len(tmp)
        return -1
    return temp+len(area)


def fill_parent(address):
    if address['city'] != "" and address['province'] == "":
        index = list(data['name']).index(address['city'])-1
        address['province'] = data['name'][data['parent_id'][index]]
    if address['district'] != "" and address['city'] == "":
        index = list(data['name']).index(address['district'])-1
        address['city'] = data['name'][data['parent_id'][index]]
        fill_parent(data)
