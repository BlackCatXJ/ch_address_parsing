import re
def loadAddrDict():
    codeDIc={}
    nameDic={}
    with open("data/addr_wyw.txt", 'r', encoding="UTF-8") as file:
        while True:
            line = file.readline().replace("\n","")
            if not line:
                break
            l=line.split("	")
            nameDic[l[0]]=l[1]
            codeDIc[l[1]]=l[0]
    return nameDic,codeDIc
nameDic,codeDic=loadAddrDict()
#可省略的后缀
omit=["省","市","区","自治区","自治州","地区","县","自治县","自治旗","旗","特别行政区"]

#递归匹配地名
def dg(text,i,res,pos):
    j=i
    have = {}
    str = ""
    if i==len(text):
        return
    tempDic = {}
    for i in range(i,len(text)):
        flag = False
        str += text[i]
        dic={}
        if tempDic:
            dic=tempDic
        else:
            dic = nameDic
        for key in dic:
            if key.startswith(str):
                tempDic[key]=dic[key]
                flag = True
            # 直接匹配
            if key == str:
                have[key] = i
                break;
            # 省略匹配
            for omt in omit:
                if str + omt == key:
                    have[str + omt] = i
                    break

        if not flag or (flag and i == len(text)-1):
            have=sorted(have.items(), key=lambda item: item[1], reverse=True)
            for k in have:
                l=len(nameDic[k[0]])
                if l==10 and res["province"]=="":
                    res["province"]=k[0]
                    pos["province"] = k[1]
                elif l==15 and res["city"]=="":
                    #校验
                    # if res["province"] !="":
                    #     if not codeDic[nameDic[k[0]][0:10]]==res["province"]:
                    #         continue
                    res["city"] = k[0]
                    pos["city"] = k[1]
                elif l==20 and res["district"]=="":
                    #校验
                    # if res["province"] != "":
                    #     if not codeDic[nameDic[k[0]][0:10]] == res["province"]:
                    #         continue
                    # if res["city"] != "":
                    #     if not codeDic[nameDic[k[0]][0:15]] == res["city"]:
                    #         continue
                    res["district"] = k[0]
                    pos["city"] = k[1]
                break
            if res["province"]!="" and res["city"]!="" and res["district"]!="":
                break
            if j-i==0:
                dg(text,i+1,res,pos)
            else:
                dg(text, i, res,pos)
            return
#地址解析
def do_parse(text):
    street=""
    pos={}
    res={   "province": "",
            "city": "",
            "district": ""
        }
    dg(text,0,res,pos)
    maxPos=0
    for key in pos:
        if maxPos < pos[key]:
            max=pos[key]

    text = text[max + 1:]
    # 拿到省市区，准备拿街道和详细地址
    other = text
    mat = re.match(".+?(镇|街道|街|地区|乡|行政事务管)", text, flags=0)
    if mat is not None:
        span = mat.span()
        street = text[span[0]:span[1]]
        other = text[span[1]:]
    return res["province"],res["city"],res["district"],street,other

def parse_address(text):
    province, city, district,street,other= do_parse(text)
    address = {
        "province": province,
        "city": city,
        "district": district,
        "street": street,
        "other": other
    }
    return address
if __name__ == '__main__':

    pass

