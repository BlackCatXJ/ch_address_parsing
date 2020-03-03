# _*_ coding:utf-8 _*_
# @Time: 2020-03-02 19:36
# @Author: BlackCatXJ
# @FileName: main.py
# @Project: ch_address_parsing

import hg.parse_add
import lqs.parse_add
import wlb.parse_add
import wyw.parse_add
from validate import validate

if __name__ == '__main__':
    # lqs
    print("="*6+" lqs "+"="*6)
    validate(lqs.parse_add.parse_address)
    # wyw
    print("="*6+" wyw "+"="*6)
    validate(wyw.parse_add.parse_address)
    # wlb
    print("="*6+" wlb "+"="*6)
    # validate(wlb.parse_add.parse_address)
    # hg
    print("="*6+" hg "+"="*6)
    validate(hg.parse_add.parse_address)
