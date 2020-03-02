# _*_ coding:utf-8 _*_
# @Time: 2020-03-02 18:21
# @Author: BlackCatXJ
# @FileName: validate.py
# @Project: ch_address_parsing

from addr_generator import generate_addr
import datetime

valiate_max_num = 1000


def time_me(func):
    '''
    @summary: cal the time of the fucntion
    @param : None
    @return: return the res of the func
    '''

    def wrapper(*args, **kw):
        start_time = datetime.datetime.now()
        res = func(*args, **kw)
        over_time = datetime.datetime.now()
        print('current Function {0} run time is {1}s'.format(func.__name__, (over_time - start_time).total_seconds()))
        return res

    return wrapper


@time_me
def validate_addr(func, addrs):
    # 验证指标
    province_num = 0
    province_right = 0
    province_find = 0
    city_num = 0
    city_right = 0
    city_find = 0
    district_num = 0
    district_right = 0
    district_find = 0
    street_num = 0
    street_right = 0
    street_find = 0
    other_num = 0
    other_right = 0
    other_find = 0
    for addr in addrs:
        result = func(addr.text)
        # 省评估
        if addr.province != "":
            province_num += 1
        if result["province"] != "":
            province_find += 1
            if result["province"] == addr.province:
                province_right += 1
        # 城市评估
        if addr.city != "":
            city_num += 1
        if result["city"] != "":
            city_find += 1
            if result["city"] == addr.city:
                city_right += 1
        # 地区评估
        if addr.district != "":
            district_num += 1
        if result["district"] != "":
            district_find += 1
            if result["district"] == addr.district:
                district_right += 1
        # 街道评估
        if addr.street != "":
            street_num += 1
        if result["street"] != "":
            street_find += 1
            if result["street"] == addr.street:
                street_right += 1
        # 其他评估
        if addr.other != "":
            other_num += 1
        if result["other"] != "":
            other_find += 1
            if result["other"] == addr.other:
                other_right += 1
    # 计算数值
    province_precision = province_right / float(province_find) * 100
    province_recall = province_find / float(province_num) * 100
    print("[province]\tprecision: %.2f%%\trecall: %.2f%%" % (province_precision, province_recall))
    city_precision = city_right / float(city_find) * 100
    city_recall = city_find / float(city_num) * 100
    print("[city]    \tprecision: %.2f%%\trecall: %.2f%%" % (city_precision, city_recall))
    district_precision = district_right / float(district_find) * 100
    district_recall = district_find / float(district_num) * 100
    print("[district]\tprecision: %.2f%%\trecall: %.2f%%" % (district_precision, district_recall))
    street_precision = street_right / float(street_find) * 100
    street_recall = street_find / float(street_num) * 100
    print("[street]  \tprecision: %.2f%%\trecall: %.2f%%" % (street_precision, street_recall))
    other_precision = other_right / float(other_find) * 100
    other_recall = other_find / float(other_num) * 100
    print("[other]   \tprecision: %.2f%%\trecall: %.2f%%" % (other_precision, other_recall))


def validate(func):
    addrs = generate_addr(valiate_max_num)
    validate_addr(func, addrs)
