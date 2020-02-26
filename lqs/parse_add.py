import json
import re


def load_addr():
    f = open('data/addr.txt', 'r+', encoding='utf-8')
    str_json = f.read()
    temp = json.loads(str_json)
    return temp


def get_by_dict(input_str):
    address = {'province': '',
               'city': '',
               'district': '',
               'street': '',
               'other': ''
               }
    temp = load_addr()
    for privs in temp:
        pri = re_privince(privs['name'])
        if pri in input_str:
            address['province'] = privs['name']
            # if privs['name'] in input_str:
            #     input_str = input_str.replace(privs['name'], '', 1)
            # else:
            #     input_str = input_str.replace(pri, '', 1)
            for citys in privs['city']:
                city = citys['name']
                re_city_str = re_city(city)
                if re_city_str in input_str:
                    address['city'] = city
                    if city in input_str:
                        input_str = input_str.replace(city, '', 1)
                    else:
                        input_str = input_str.replace(re_city_str, '', 1)
                    for areas in citys['area']:
                        re_areas_str = re_district(areas)
                        if re_areas_str in input_str:
                            address['district'] = areas

    return address


def get_province(address, input_str):
    res = re.search('.+省', input_str)
    if hasattr(res, 'group') and res.group(0) != '':
        address['province'] = res.group(0)
    return address


def get_city(address, input_str):
    res = re.search('(?<=省).+?(市|自治区)', input_str)
    if hasattr(res, 'group') and res.group(0) != '':
        address['city'] = res.group(0)
    return address


def get_district(address, input_str):
    reg_prefix = ''
    if address['city'] != '':
        if address['city'] in input_str:
            reg_prefix = address['city']
        else:
            reg_prefix = re_city(address['city'])
    elif address['province'] != '':
        if address['province'] in input_str:
            reg_prefix = address['province']
        else:
            reg_prefix = re_privince(address['province'])
    else:
        reg_prefix = ''
    res = re.search(reg_prefix + '(?P<dist>.*(区|县|自治县|市))', input_str)
    if hasattr(res, 'group') and res.group('dist') != '':
        address['district'] = res.group('dist')
    return address


def get_street(address, input_str):
    reg_prefix = ''
    if address['district'] != '':
        if address['district'] in input_str:
            reg_prefix = address['district']
        else:
            reg_prefix = re_district(address['district'])
    elif address['city'] != '':
        if address['city'] in input_str:
            reg_prefix = address['city']
        else:
            reg_prefix = re_city(address['city'])
    elif address['province'] != '':
        if address['province'] in input_str:
            reg_prefix = address['province']
        else:
            reg_prefix = re_privince(address['province'])
    else:
        reg_prefix = ''
    res = re.search(reg_prefix + '(?P<street>.*?(街道|乡|镇))', input_str)
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
        else:
            reg_prefix = re_district(address['district'])
    elif address['city'] != '':
        if address['city'] in input_str:
            reg_prefix = address['city']
        else:
            reg_prefix = re_city(address['city'])
    elif address['province'] != '':
        if address['province'] in input_str:
            reg_prefix = address['province']
        else:
            reg_prefix = re_privince(address['province'])
    else:
        reg_prefix = ''
    res = re.search('(' + reg_prefix + ')(?P<other>.*)', input_str)
    if hasattr(res, 'group') and res.group('other') != '':
        address['other'] = res.group('other')
    return address


def re_privince(pri):
    if '省' in pri:
        pri = pri.replace('省', '')
    if '市' in pri:
        pri = pri.replace('市', '')
    return pri


def re_city(city):
    if '市' in city:
        city = city.replace('市', '')
    return city


def parse_address(text):
    text.replace(' ', '')
    address = get_by_dict(text)
    if (address['province'] == ''):
        address = get_province(address, text)
    if (address['city'] == ''):
        address = get_city(address, text)
    if (address['district'] == ''):
        address = get_district(address, text)
    address = get_street(address, text)
    address = get_other(address, text)
    return address


def re_district(district):
    if '自治区' in district:
        district = district.replace('自治区', '')
    if '自治县' in district:
        district = district.replace('自治县', '')
    if '区' in district:
        district = district.replace('区', '')
    if '县' in district:
        district = district.replace('县', '')
    if '市' in district:
        district = district.replace('市', '')
    return district

# if __name__ == '__main__':
#     input_str = '香港深水埗区朝阳街道123123'
#     address = parse_address(input_str)
#     print(address)
