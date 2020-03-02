# _*_ coding:utf-8 _*_
# @Time: 2020-03-02 18:15
# @Author: BlackCatXJ
# @FileName: addr_generator.py
# @Project: ch_address_parsing
import csv
import os
import random
from address import Address

# 地址数据文件夹地址
addr_dir = "data/addr"
# 乡镇
villages_path = os.path.join(addr_dir, "villages.csv")
# 街道
street_path = os.path.join(addr_dir, "streets.csv")
# 地区
district_path = os.path.join(addr_dir, "areas.csv")
# 城市
city_path = os.path.join(addr_dir, "cities.csv")
# 省
province_path = os.path.join(addr_dir, "provinces.csv")


def generate_addr(max_num):
    # 初始化地区集合
    addr = []
    # 获取省的词典
    province_dict = get_addr_dict(province_path)
    # 获取市的词典
    city_dict = get_addr_dict(city_path)
    # 获取地区词典
    district_dict = get_addr_dict(district_path)
    # 获取街道词典
    street_dict = get_addr_dict(street_path)
    # 获取乡镇集合
    village_content = read_csv(villages_path)[1:]
    random.shuffle(village_content)
    # 随机遍历获取地址
    count = 0
    for village in village_content:
        if count < max_num:
            address = Address()
            # 省
            address.province_code = village[3]
            address.province = province_dict[village[3]]
            # 市
            address.city_code = village[4]
            address.city = city_dict[village[4]]
            # 区
            address.district_code = village[5]
            address.district = district_dict[village[5]]
            # 街道
            address.street_code = village[2]
            address.street = street_dict[village[2]]
            # 其他
            address.other = village[1]
            # 地址完整描述
            address.text = address.province + address.city + address.district + address.street + address.other
            addr.append(address)
            count += 1
    return addr


def read_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        csv_content = list(reader)
        return csv_content


def get_addr_dict(file_path):
    dict = {}
    csv_content = read_csv(file_path)[1:]
    for content in csv_content:
        if len(content) > 1:
            dict[content[0]] = content[1]
    return dict


if __name__ == '__main__':
    addrs = generate_addr(100)
    for addr in addrs:
        print(addr.text)
