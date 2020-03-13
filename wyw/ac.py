
class node(object):
    def __init__(self):
        self.next = {}       #相当于指针，指向树节点的下一层节点
        self.fail = None     #失配指针，这个是AC自动机的关键
        self.isWord = False  #标记，用来判断是否是一个标签的结尾
        self.word = ""       #用来储存标签
class ac_automation(object):
    def __init__(self):
        self.root = node()  #定义根节点

    def add(self, word):
        temp_root = self.root
        for char in word:  # 遍历标签的每个字
            if char not in temp_root.next:  # 如果节点下没有这个字，就加入这个字的节点
                temp_root.next[char] = node()
            temp_root = temp_root.next[char]  # 沿着标签建立字典
        temp_root.isWord = True  # 标签结束，表示从根到这个节点是一个完整的标签
        temp_root.word = word

    def make_fail(self):
        temp_que = []  # 使用BFS来遍历这棵字典树
        temp_que.append(self.root)
        while len(temp_que) != 0:
            temp = temp_que.pop(0)
            p = None
            for key in temp.next:
                if temp == self.root:  # 根节点的孩子们的fail都指向根
                    temp.next[key].fail = self.root
                else:
                    p = temp.fail
                    while p is not None:  # 寻找fial指针指向的地方
                        if key in p.next:  # 如果是另一个fail指针下面找到了，就储存
                            temp.next[key].fail = p.next[key]
                            break
                        p = p.fail
                    if p is None:  # 如果该节点fail指针不存在，就指向根
                        temp.next[key].fail = self.root
                temp_que.append(temp.next[key])

    def search(self, content):
        p = self.root
        result = []
        currentposition = 0  # 用来标记当前标签的汉字

        while currentposition < len(content):
            word = content[currentposition]
            while word not in p.next and p != self.root:  # 搜索状态机，直到匹配
                p = p.fail

            if word in p.next:
                p = p.next[word]
            else:
                p = self.root

            if p.isWord:  # 若状态到达标签结尾，就添加入结果中
                result.append(p.word)
            currentposition += 1

    def dosearch(self,p,result):
        if p.isWord:
            result.append(p.word)
        for key in p.next:
            ac_automation.dosearch(self,p.next[key],result)

    def searchPrefix(self, content):
        p = self.root
        result = []
        currentposition = 0  # 用来标记当前标签的汉字
        while currentposition < len(content):
            word = content[currentposition]
            if word not in p.next:
                return []
            else:
                p = p.next[word]
            currentposition += 1
        ac_automation.dosearch(self,p,result)
        return result




