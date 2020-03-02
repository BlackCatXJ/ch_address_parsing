import json
import re

pri_suffix_list = ['省','维吾尔自治区','市','特别行政区','回族自治区','壮族自治区','自治区']
dist_suffix_list = ['自治区','自治县','区','县','市']
street_suffix_list = ['街道','乡','镇','地区']
f = open('data/new_addr.txt', 'r+', encoding='utf-8')
str_json = f.read()
addr_dict = json.loads(str_json)

def get_by_dict(input_str):
    address = {'province': '',
               'city': '',
               'district': '',
               'street': '',
               'other': ''
            }
    for privs in addr_dict:
        if address['province']!='':
            break
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
                    area = areas['name']
                    re_areas_str = re_district(area)
                    if re_areas_str in input_str:
                        address['district'] = area
                        for street in areas['street']:
                            re_street_str = re_street(street)
                            if re_street_str in input_str:
                                address['street'] = street

    return address


def get_province(address, input_str):
    res = re.search('.+省', input_str)
    if hasattr(res, 'group') and res.group(0) != '':
        address['province'] = res.group(0)
    return address


def get_city(address, input_str):
    reg_prefix = ''
    if address['province'] != '':
        if address['province'] in input_str:
            reg_prefix = address['province']
        else:
            reg_prefix = re_privince(address['province'])
    res = re.search('(?<='+ reg_prefix + ').+?(市|自治区|自治州)', input_str)
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
    res = re.search(reg_prefix + '(?P<dist>.*(区|县|自治县|市))(?!级)', input_str)
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
    for pri_suffix in pri_suffix_list:
        if pri_suffix in pri:
            pri = pri.replace(pri_suffix, '')
            break
    return pri


def re_city(city):
    if '市' in city:
        city = city.replace('市', '')
    return city

def  complet_addr(address):
    if address['province'] !='' and address['city']!='' and address['district']!='':
        return address
    else:
        for privs in addr_dict:
            for citys in privs['city']:
                city = citys['name']
                if city ==  address['city'] and address['province'] =='':
                    address['province'] = privs['name']
                for areas in citys['area']:
                    if address['district'] == areas['name']:
                        if address['province'] ==  '':
                            address['province'] = privs['name']
                        if address['city'] == '':
                            address['city'] = city
                    if address['district'] == '':
                        if address['province'] == privs['name'] or address['city'] == citys['name']:
                            for street in areas['street']:
                                if street in address['street']:
                                    if address['street'] == street:
                                        address['district'] = areas['name']
                                    if address['city'] == '':
                                        address['city'] = city
                        else:
                            for street in areas['street']:
                                if street in address['street']:
                                    if address['street'] == street:
                                        address['district'] = areas['name']
                                    if address['city'] == '':
                                        address['city'] = city
                                    if address['province'] == '':
                                        address['province'] = privs['name']
    return address

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
    address = complet_addr(address)
    return address


def re_district(district):
    for dist_suffix in dist_suffix_list:
        if dist_suffix in district:
            district = district.replace(dist_suffix, '')
            break
    return district

def re_street(street):
    for street_suffix in street_suffix_list:
        if street_suffix in street:
            street = street.replace(street_suffix, '')
    return street

if __name__ == '__main__':
    input_str = '四川锦江督院街街道123'
    address = parse_address(input_str)
    print(address)
