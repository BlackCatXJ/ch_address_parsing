import pandas as pd
import re
import wlb.ACautomaton as ac

AREA_SUFFIXES = ["自治区", "省", "市", "区", "县"]
PRO_CODE_LEN = 10
CIT_CODE_LEN = 15
DIS_CODE_LEN = 20
IS_AC = True
data = pd.DataFrame(pd.read_csv('wlb/area.txt', encoding='utf-8'))
area_name = data['name'].values
model = ac.Trie(area_name)
no_suf = []
for index in range(len(area_name)):
    name = area_name[index]
    flg = 1
    for suf in AREA_SUFFIXES:
        if name.endswith(suf):
            tmp = name.replace(suf, '')
            no_suf.append(tmp)
            flg = 0
            break
    if flg:
        no_suf.append(name)
t_model = ac.Trie(no_suf)


def parse_address(text):
    address = {
        "province": "",
        "city": "",
        "district": "",
        "street": "",
        "other": ""
    }
    if IS_AC:
        get_address_ac(text, "", address)
        fill_parent(address)
        get_address_ac(text, AREA_SUFFIXES, address)
    else:
        get_address(text, "", address)
        fill_parent(address)
        get_address(text, AREA_SUFFIXES, address)
    index = find_index(address["district"],text)
    if index != -1:
        text = text[index:]
        mat = re.match(".*?(镇|街道|街|乡镇|区|乡)", text, flags=0)
        if mat is not None:
            span = mat.span()
            address["street"] = text[span[0]:span[1]]
            address["other"] = text[span[1]:]
    return address


def get_address_ac(text, suffix, address):
    if (suffix == ""):
        words = model.search(text)
        for word in words.keys():
            index = list(data['name']).index(word)
            set_address(index,address)
    else:
        words = t_model.search(text)
        for word in words.keys():
            if len(word) <= 1:
                continue
            else:
                index = no_suf.index(word)
                set_address(index,address)


def get_address(text, suffix, address):
    word_list = []
    i = 0
    while i < len(text):
        longest_word = text[i]
        for j in range(i + 1, len(text) + 1):
            word = text[i: j]
            if(suffix == ""):
                if word in data['name'].values:
                    index = list(data['name']).index(word)
                    set_address(index,address)
                    longest_word = word
                    break
            else:
                for suf in AREA_SUFFIXES:
                    if word+suf in data['name'].values:
                        index = list(data['name']).index(word+suf)
                        set_address(index, address)
                        longest_word = word
                        break

        word_list.append(longest_word)
        i += len(longest_word)
    return word_list


def set_address(index,address):
    word = data['name'][index]
    code = '0000'+str(data['code'][index])
    if len(code) == PRO_CODE_LEN and address['province'] == "":
        address['province'] = word
    elif len(code) == CIT_CODE_LEN and address['city'] == "":
        address['city'] = word
    elif len(code) == DIS_CODE_LEN and address['district'] == "":
        address['district'] = word


def find_index(area,text):
    temp = text.find(area)
    if temp == -1:
        for s in AREA_SUFFIXES:
            tmp = area.replace(s,"")
            temp = text.find(tmp)
            if temp == -1:
                continue
            else: return temp+len(tmp)
        return -1
    return temp+len(area)


def fill_parent(address):
    if address['city'] != "" and address['province'] == "":
        index = list(data['name']).index(address['city'])
        print(data['parent_id'][index])
        address['province'] = data['name'][data['parent_id'][index]-1]
    if address['district'] != "" and address['city'] == "":
        index = list(data['name']).index(address['district'])
        address['city'] = data['name'][data['parent_id'][index]-1]
        fill_parent(address)


parse_address("湖北武汉")
