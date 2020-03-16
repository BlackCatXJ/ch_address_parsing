# -*- coding:utf-8 -*-
"""
Description: AC自动机
"""
from collections import defaultdict
import pandas as pd


class TrieNode(object):
    def __init__(self, value=None):
        # 值
        self.value = value
        # fail指针
        self.fail = None
        # 尾标志：标志为i表示第i个模式串串尾，默认为0
        self.tail = 0
        # 子节点
        self.children = {}


class Trie(object):
    def __init__(self, words):
        # 根节点
        self.root = TrieNode()
        # 模式串个数
        self.count = 0
        self.words = words
        for word in words:
            self.insert(word)
        self.ac_automation()

    def insert(self, sequence):
        self.count += 1
        cur_node = self.root
        for item in sequence:
            if item not in cur_node.children:
                # 插入结点
                child = TrieNode(value=item)
                cur_node.children[item] = child
                cur_node = child
            else:
                cur_node = cur_node.children[item]
        cur_node.tail = self.count
        cur_node.length = len(sequence)

    def ac_automation(self):
        queue = [self.root]
        while len(queue):
            temp_node = queue[0]
            # 取出队首元素
            queue.remove(temp_node)
            for value in temp_node.children.values():
                # 根的子结点fail指向根自己
                if temp_node == self.root:
                    value.fail = self.root
                else:
                    # 转到fail指针
                    p = temp_node.fail
                    while p:
                        # 若结点值在该结点的子结点中，则将fail指向该结点的对应子结点
                        if value.value in p.children:
                            value.fail = p.children[value.value]
                            break
                        # 转到fail指针继续回溯
                        p = p.fail
                    # 若为None，表示当前结点值在之前都没出现过，则其fail指向根结点
                    if not p:
                        value.fail = self.root
                # 将当前结点的所有子结点加到队列中
                queue.append(value)

    def search(self, text):
        p = self.root
        # 记录匹配起始位置下标
        start_index = 0
        # 成功匹配结果集
        rst = defaultdict(list)
        for i in range(len(text)):
            single_char = text[i]
            while single_char not in p.children and p is not self.root:
                p = p.fail
            if single_char in p.children and p is self.root:
                start_index = i
            if single_char in p.children:
                p = p.children[single_char]
            else:
                start_index = i
                p = self.root
            temp = p
            # while temp is not self.root:
            #     if temp.tail:
            #         rst[self.words[temp.tail - 1]].append((start_index, i))
            #     temp = temp.fail
            if temp.tail:
                if len(text) <= i+1 or text[i+1] not in temp.children:
                    rst[self.words[temp.tail - 1]].append((start_index, i))
                    p = self.root
        return rst

    def longest_search(self, text):
        p = self.root
        index = 0
        # 成功匹配结果集
        rst = []
        tmp_rst = []
        for i in range(len(text)):
            single_char = text[i]
            while single_char not in p.children and p is not self.root:
                p = p.fail
            if single_char in p.children:
                p = p.children[single_char]
            else:
                p = self.root
            temp = p
            if temp.tail:
                tmp_word = self.words[temp.tail - 1]
                if len(tmp_rst):
                    if i - len(tmp_word) < index:
                        tmp_rst.append(tmp_word)
                    else:
                        longest_word = ""
                        for t_word in tmp_rst:
                            if len(t_word) > len(longest_word):
                                longest_word = t_word
                        rst.append(longest_word)
                        tmp_rst = [tmp_word]
                        index = i
                else:
                    index = i
                    tmp_rst.append(tmp_word)
                if i == len(text)-1:
                    longest_word = ""
                    for t_word in tmp_rst:
                        if len(t_word) > len(longest_word):
                            longest_word = t_word
                    rst.append(longest_word)
        return rst


data = pd.DataFrame(pd.read_csv('area.txt', encoding='utf-8'))
area_name = data['name'].values
t_model = Trie(area_name)
no_suf = []
AREA_SUFFIXES = ["自治区", "省", "市", "区", "县"]
for index in range(len(area_name)):
    name = area_name[index]
    flg = 1
    for suf in AREA_SUFFIXES:
        if name.endswith(suf):
            tmp = name.replace(suf, '')
            no_suf.append(tmp)
            flg = 0
            break
    if flg:
        no_suf.append(name)
test = ["湖南","南京市"]
no_suf.append("南京市")
no_suf.remove("青")
model = Trie(no_suf)
print(model.longest_search("青海南京"))
