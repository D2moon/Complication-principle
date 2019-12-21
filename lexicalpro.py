import numpy as np  # 导入Numpy库

ExpGrammar = []  # 文法
Grammar = []  # 拆解后文法

terminal = ["!", "+", "-", "*", "/", "id", ";", "(", ")", "{", "}", "==", "!=", "<", ">", "<=", ">=", "int", "if",
            "return", "while", "else", "void", "=", ",", "sz", "#"]  # 终结符

unterminal = []  # 非终结符
list1 = []


def judge(s1):
    if s1 not in terminal:
        if s1 not in unterminal:
            unterminal.append(s1)


# mea = input('请输入开启文件位置 :')  # 文法输入文件
mea = 'grammar2.txt'
with open(mea, mode='r', encoding='UTF-8', errors='ignore') as fuck:
    list1 = fuck.readlines()
len1 = len(list1)
for i in range(0, len1 - 1):
    len2 = len(list1[i])
    ExpGrammar.append(list1[i][0:len2 - 1])
ExpGrammar.append(list1[len1 - 1])

# print(ExpGrammar)


Grammar.append([])
for i in range(0, len1):
    list2 = []
    pos = ExpGrammar[i].rfind('->')
    len2 = len(ExpGrammar[i])
    unt = ExpGrammar[i][0:pos]
    judge(unt)
    pos += 2
    pot = ExpGrammar[i][pos:len2].rfind(' ')
    while pot != -1:
        unt = ExpGrammar[i][pos + pot + 1:len2]
        list2.append(unt)
        judge(unt)
        len2 = pos + pot
        pot = ExpGrammar[i][pos:len2].rfind(' ')
    unt = ExpGrammar[i][pos:len2]
    list2.append(unt)
    judge(unt)
    Grammar.append(list2)
fuck.close()


# 麻烦自己按照文件写入方式进行读取

# 求fist 集合

# 单个符号
def getFirst1(word1):
    first = set()
    if word1 in terminal:
        first.add(word1)
    else:
        target = word1
        for wod in ExpGrammar:
            for i in range(0, len(wod)):
                if wod[i] == '>':
                    break
            if target == wod[0:i - 1]:
                for j in range(i + 1, len(wod)):
                    if wod[j] == " ":
                        gm = wod[i + 1:j]
                        break
                    if j == len(wod) - 1:
                        gm = wod[i + 1:]
                kid = getFirst1(gm)
                first = first.union(first, kid)

    return first


# 式子的first集
def getFirst(formula):
    First = set()
    ccc = 0
    big = 0
    for i in range(0, len(formula)):
        if formula[i] == " ":
            hub = formula[big: i]
            ccc = 1
            big = i + 1
        if i == len(formula) - 1:
            hub = formula[big:]
            ccc = 1

        i = i + 1
        if ccc == 1:
            First = First.union(First, getFirst1(hub))

            ccc = 0
            if "!" in getFirst1(hub):
                continue
            else:
                break

    return First


# 判断是否为空
def IsEmpty(mm):
    ccc = 0
    big = 0
    for wto in range(0, len(mm)):
        if mm[wto] == " ":
            hub = mm[big:wto]
            ccc = 1
            wto = wto + 1
            big = wto
        elif wto == len(mm) - 1:
            hub = mm[big:]
            ccc = 1

        if ccc == 1:

            if "!" in getFirst(hub):
                ccc = 0
                continue

            else:

                return False

    if wto == len(mm) - 1:
        return True
    else:
        # print(wto)
        return False


# 求follow 集合
def getFollow(word2):
    global num
    fool = set()

    for i in ExpGrammar:
        for j in range(0, len(i)):
            if i[j] == "-":
                ha = i[0:j]
                break
        j = j + 2
        big = j
        odd = 0
        # state=set()
        for k in range(j, len(i)):
            if i[k] == " ":
                he = i[big:k]
                big = k + 1
                odd = 1
            if k == len(i) - 1:
                he = i[big:]
                odd = 1
                big = len(i)
            if odd == 1:
                if he == "!" and ha == word2:
                    fool.add("#")
                    break
                if he == word2:
                    if k < len(i) - 1 and big != len(i):
                        o = i[big:]
                        fool = fool.union(fool, getFirst(o))
                        for num in range(0, len(o)):
                            if o[num] == " ":
                                break
                        if num == 0:
                            ppp = o[0]
                        else:
                            ppp = o[0:num]

                        if '!' in getFirst(o) and ppp in unterminal:
                            fool = fool.union(fool, getFollow(ppp))
                            break
                    if k == len(i) - 1 and ha != he:
                        fool.add("#")
                        fool = fool.union(fool, getFollow(ha))
    fool.discard('!')
    return fool


# 求sele集合
def getSele(word):
    sele = set()
    a = word.find("-")
    ha = word[0:a]
    a = a + 2
    hb = word[a:]
    if IsEmpty(hb):
        sele = sele.union(getFirst(hb), getFollow(ha))
        sele.discard("!")
        return sele
    else:
        sele = getFirst(hb)
        sele.discard("!")
        return sele


# 创建数组分析表
# 用numpy 二维数组么？
# 还是list嵌套 吧
Terminal = []


def makelist():
    terminal1 = terminal[:]
    terminal1.remove("!")
    terminal1.append("#")
    global Terminal
    Terminal = terminal1
    Sele = []
    Anatab = []
    anatab = {}
    for i in ExpGrammar:
        jj = []
        for j in getSele(i):
            jj.append(j)
        Sele.append(jj)

    for k in unterminal:
        mmp = [0] * len(terminal1)
        for i in range(0, len(ExpGrammar)):
            a = ExpGrammar[i].find("-")
            ha = ExpGrammar[i][0:a]
            if ha == k:
                for kkk in range(0, len(terminal1)):
                    if terminal1[kkk] in Sele[i]:
                        mmp[kkk] = i + 1
        Anatab.append(mmp)

    for i in range(0, len(Anatab)):
        anatab[unterminal[i]] = Anatab[i]
    return anatab


for i in ExpGrammar:
    getSele(i)

dirt = makelist()

mapa = {}
for i in range(0, len(Terminal)):
    mapa[Terminal[i]] = i


'''
#print(dirt['cons3'], end=' ')
for i in range(0, len(terminal)):
    print(dirt['cons3'][i], end=' ')
    print(terminal[i])
'''

'''
#  select集输出
name2 = 'output.txt'     #name2=input("请输入存储位置:   ")
with open(name2, mode='w') as fuck_you:
    for i in ExpGrammar:
        for j in getSele(i):
            fuck_you.write(j+" ")
        fuck_you.write("\n")

fuck_you .close()
'''
