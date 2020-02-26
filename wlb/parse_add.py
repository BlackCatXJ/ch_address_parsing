import jieba


def parse_address(text):
    address = {
        "province": "",
        "city": "",
        "district": "",
        "street": "",
        "other": ""
    }
    jieba.load_userdict("data/location.txt")
    word = jieba.lcut(text)
    # print(word)
    for text in word:
        if ("省" in text or "自治区" in text or "上海市" in text or "重庆市" in text or "天津市" in text or "北京市" in text) and (
                address["province"] == ""):
            address["province"] = text
        elif "市" in text and (address["city"] == ""):
            address["city"] = text
        elif ("区" in text or "县" in text) and (address["district"] == ""):
            address["district"] = text
        elif "街" in text and (address["street"] == ""):
            address["street"] = text
        else:
            address["other"] += text
    # print(address)
    return address
