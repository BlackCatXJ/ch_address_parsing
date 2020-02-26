import cpca
import re


def parse_address(text):
    np = []
    np.append(text)
    df = cpca.transform(np, cut=False, pos_sensitive=True, lookahead=5)
    province = df['省'][0]
    city = df['市'][0]
    district = df['区'][0]
    other = df['地址'][0]
    province_pos = df['省_pos'][0]
    city_pos = df['市_pos'][0]
    district_pos = df['区_pos'][0]
    a = []
    b = []
    a.append(district)
    a.append(city)
    a.append(province)
    b.append(district_pos)
    b.append(city_pos)
    b.append(province_pos)
    for i in range(0, 3):
        if b[i] != -1:
            index = other.find(a[i])
            if index != -1:
                other = other[index + len(a[i]):]
            break
    mat = re.match(".*?(镇|街道|街)", other, flags=0)
    street = ""
    if mat is not None:
        span = mat.span()
        street = other[span[0]:span[1]]
        other = other[span[1]:]
    if province_pos == -1:
        province = ""
    if city_pos == -1:
        city = ""
    if district_pos == -1:
        district = ""
    address = {
        "province": province,
        "city": city,
        "district": district,
        "street": street,
        "other": other
    }
    return address
