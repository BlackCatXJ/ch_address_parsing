#!/usr/bin/python
# coding=utf-8
# location_str = ["我居住在湖北省鄂州市梁子湖区长梁中学门口", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
import cpca
import sys
import re
def parse_address(text):
    text_arr = {text}
    df = cpca.transform(text_arr)

    province = df.iat[0,0]
    city = df.iat[0,1]
    district = df.iat[0,2]
    other = df.iat[0,3]

    pattern = re.compile('([\u4e00-\u9fa5]{1,8}?(?:街道|街|大道|道|小区|坊|区|路|镇|县|州)){0,1}(\w*){0,1}')
    result = pattern.findall(other)
    print(result)

    addr_json = {
	"province": province,
	"city": city,
	"district": district,
	"street": result[0][0],
	"other": result[0][1]
    }
    print(addr_json)
    return addr_json;

