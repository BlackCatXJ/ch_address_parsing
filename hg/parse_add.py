#!/usr/bin/python
# coding=utf-8
# location_str = ["我居住在湖北省鄂州市梁子湖区长梁中学门口", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
import cpca
import sys
import re

def get_street(address, input_str):
    reg_prefix = ''
    if address['district'] != '':
        if address['district'] in input_str:
            reg_prefix = address['district']
    elif address['city'] != '':
        if address['city'] in input_str:
            reg_prefix = address['city']
    elif address['province'] != '':
        if address['province'] in input_str:
            reg_prefix = address['province']
    else:
        reg_prefix = ''
    res = re.search(reg_prefix + '(?P<street>.*?(街道|乡|镇|地区))', input_str)
    if hasattr(res, 'group') and res.group('street') != '':
        address['street'] = res.group('street')
    return address


def get_other(address, input_str):
    reg_prefix = ''
    if address['street'] != '':
        reg_prefix = address['street']
    elif address['district'] != '':
        if address['district'] in input_str:
            reg_prefix = address['district']
    elif address['city'] != '':
        if address['city'] in input_str:
            reg_prefix = address['city']
    elif address['province'] != '':
        if address['province'] in input_str:
            reg_prefix = address['province']
    else:
        reg_prefix = ''
    res = re.search('(' + reg_prefix + ')(?P<other>.*)', input_str)
    if hasattr(res, 'group') and res.group('other') != '':
        address['other'] = res.group('other')
    return address

def parse_address(text):
    text_arr = {text}
    df = cpca.transform(text_arr, cut=False)

    province = df.iat[0, 0]
    city = df.iat[0, 1]
    district = df.iat[0, 2]
    other = df.iat[0, 3]

    #print(other)

    # pattern = re.compile(district + '(?P<street>.*?(街道|道|站|局|处|街|大道|小区|场|坊|路|团|委员会|区|县|州)){0,1}(\w*){0,1}')
    # result = pattern.findall(text)
    # print(result)

    addr_json = {
        "province": province,
        "city": city,
        "district": district,
        "street": "",
        "other": ""
    }

    addr_json = get_street(addr_json, text)
    addr_json = get_other(addr_json, text)
    # print(addr_json)
    return addr_json
# parse_address("上海市浦东新区高桥镇潼港三村居委会")
