#!/usr/bin/python
# coding=utf-8
# location_str = ["我居住在湖北省鄂州市梁子湖区长梁中学门口", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
import cpca
import sys
import re


def parse_address(text):
    df = cpca.transform(text)

    province = df.iat[0, 0]
    city = df.iat[0, 1]
    district = df.iat[0, 2]

    pattern = re.compile(
        '^([\u4e00-\u9fa5]{2,5}?(?:省|自治区|市)){0,1}([\u4e00-\u9fa5]{2,7}?(?:市|区|县|州)){0,1}([\u4e00-\u9fa5]{2,7}?(?:市|区|县)){0,1}([\u4e00-\u9fa5]{2,7}?(?:街道|街|大道|道|小区|坊|区)){0,1}([\u4e00-\u9fa5]*)$')
    result = pattern.findall(text)
    addr_json = {
        "province": province,
        "city": city,
        "district": district,
        "street": result[0][3],
        "other": result[0][4]
    }
    return addr_json
