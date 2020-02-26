# _*_ coding:utf-8 _*_
# @Time: 2020-02-26 17:59
# @Author: BlackCatXJ
# @FileName: infer.py
# @Project: addr_reg
import json

import hg.parse_add
import lqs.parse_add
import wlb.parse_add
import wyw.parse_add


def print_addr_result(addr_dict):
    print("省: " + addr_dict["province"])
    print("市：" + addr_dict["city"])
    print("区：" + addr_dict["district"])
    print("街道：" + addr_dict["street"])
    print("其他：" + addr_dict["other"])


if __name__ == '__main__':
    with open("data/test_data.txt") as f:
        lines = f.readlines()
        for line in lines:
            print("====== wlb ======")
            wlb_result = wlb.parse_add.parse_address(line)
            print_addr_result(wlb_result)
            print("====== lqs ======")
            lqs_result = lqs.parse_add.parse_address(line)
            print_addr_result(lqs_result)
            print("====== wyw ======")
            wyw_result = wyw.parse_add.parse_address(line)
            print_addr_result(wyw_result)
            # print("====== hg ======")
            # hg_result = hg.parse_add.parse_address(line)
            # print_addr_result(hg_result)


