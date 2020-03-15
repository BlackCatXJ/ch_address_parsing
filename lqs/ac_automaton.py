# _*_ coding:utf-8 _*_
# @Time: 2020-03-08 10:12
# @Author: qs_lau
# @FileName: ac_automaton.py
# @Project: ch_address_parsing

from collections import defaultdict


class TrieNode(object):
    def __init__(self, value=None):
        # 值
        self.value = value
        # fail指针
        self.fail = None
        # 尾标志：标志为i表示第i个模式串串尾，默认为0
        self.tail = 0
        # 子节点，{value:TrieNode}
        self.children = {}


class Trie(object):
    def __init__(self, words):
        print("初始化")
        # 根节点
        self.root = TrieNode()
        # 模式串个数
        self.count = 0
        self.words = words
        for word in words:
            self.insert(word)
        self.ac_automation()
        print("初始化完毕")

    def insert(self, sequence):
        """
        基操，插入一个字符串
        :param sequence: 字符串
        :return:
        """
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

    def ac_automation(self):
        """
        构建失败路径
        :return:
        """
        queue = [self.root]
        # BFS遍历字典树
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
        """
        模式匹配
        :param self:
        :param text: 长文本
        :return:
        """
        p = self.root
        # 记录匹配起始位置下标
        start_index = 0
        # 成功匹配结果集
        rst = defaultdict(list)
        text_len = len(text)
        i=0
        while i < text_len:
            single_char = text[i]
            while single_char not in p.children and p is not self.root:
                p = p.fail
            if single_char in p.children and p is self.root:
                start_index = i
            # 若找到匹配成功的字符结点，则指向那个结点，否则指向根结点
            if single_char in p.children:
                p = p.children[single_char]
            else:
                start_index = i
                p = self.root
            temp = p
            #注释可识别多个词 比如 不知、不觉、不知不觉都在字典中存在的，均识别出
            # while temp is not self.root:
            #     # 尾标志为0不处理，但是tail需要-1从而与字典下标一致
            #     # 循环原因在于，有些词本身只是另一个词的后缀，也需要辨识出来
            #     if temp.tail:
            #         rst[self.words[temp.tail - 1]].append((i- len(self.words[temp.tail - 1]) + 1, i))
            #     temp = temp.fail
            # 识别出最长的串
            if temp.tail:
                if text_len <= i+1 or text[i+1] not in temp.children:
                    rst[self.words[temp.tail - 1]].append((start_index, i))
                    temp = temp.fail
                    #加上这句，湖南京，只会匹配到湖南，不会匹配出南京
                    p = self.root
            i = i + 1
        return rst

    def most_long_search(self, text):
        """
        只匹配出最长的字符串，比如词典有：湖南、南京市   输入 湖南京市  只得到南京市
        如果词典有 湖南、南京  输入 湖南京， 只得到湖南
        :param self:
        :param text: 长文本
        :return:
        """
        p = self.root
        # 成功匹配结果集
        rst = defaultdict(list)
        text_len = len(text)
        last_word = ''
        last_end_pos = 0
        last_start_pos = 0
        i = 0
        while i < text_len:
            single_char = text[i]
            while single_char not in p.children and p is not self.root:
                p = p.fail
            # 若找到匹配成功的字符结点，则指向那个结点，否则指向根结点
            if single_char in p.children:
                p = p.children[single_char]
            else:
                p = self.root
            temp = p
            # 识别出最长的串
            if temp.tail:
                if text_len <= i + 1 or text[i + 1] not in temp.children :
                    now_start_pos = i - len(self.words[temp.tail - 1]) + 1
                    now_word = self.words[temp.tail - 1]
                    if (last_end_pos == 0):
                        last_word = now_word
                        last_end_pos = i
                        last_start_pos = now_start_pos
                    elif last_end_pos >= now_start_pos and len(last_word) < len(now_word) :
                        last_word = now_word
                        last_end_pos = i
                        last_start_pos = now_start_pos
                    elif last_end_pos >= now_start_pos and len(last_word) >= len(now_word) :
                        continue
                    elif last_end_pos < now_start_pos:
                        rst[last_word].append((last_start_pos, last_end_pos))
                        last_word = now_word
                        last_end_pos = i
                        last_start_pos = now_start_pos
                        temp = temp.fail
                        # 加上这句，湖南京，只会匹配到湖南，不会匹配出南京
                        #p = self.root
            i = i + 1
        rst[last_word].append((last_start_pos, last_end_pos))
        return rst

if __name__ == "__main__":
    # test_words = ["she", "he","say","shr","herr","ha","haha","a"]
    # test_text = "hahayasherrhs"
    test_words = ["湖南", "南京", "湖南京", "南京市区"]
    test_text = "湖南京市区湖南京市区湖南京市区湖南京市区湖南"
    model = Trie(test_words)
    print(str(model.most_long_search(test_text)))