k_word = {'int': 1, 'void': 2, 'if': 3, 'return': 4, 'while':5, 'else':6}          # 关键字表
p_word = {'{': 1, '}': 2, '(': 3, ')': 4, '[': 5, ']': 6, '=': 7, '<': 8, '>': 9, '<=': 10, '>=': 11, '!=': 12,
          '==': 13, '+': 14, '-': 15, '*': 16, '/': 17, ';': 18, ',': 19, '!': 20}   # 界符表
i_word = {}                             # 标识符表
c_word = {}                             # 数字表
s_word = {}                             # 字符串表
ch_word = {}                            # 字符表
numk = 2
numi = 0        # 当前标识符的数量
numch = 0
numc = 0
nums = 0        # 当前字符串的数量
nump = 19
statep = 0


class Data:
    def __init__(self, _type='', _val=0, _str=''):
        self.type = _type
        self.val = _val
        self.str = _str


Token = []

fo = open('output.txt', 'w')


def addtoi_word(s):  # 添加至标识符
    #print(s)
    global numi
    if len(s) == 0:
        return
    elif not(s in k_word):
        if not (s in i_word):
            numi = numi + 1
            i_word[s] = numi
        fo.write('<I,%d>\n' % i_word[s])
        d1 = Data('I', 0, s)
        Token.append(d1)
    else:
        fo.write('<K,%d>\n' % k_word[s])
        d1 = Data('K', 0, s)
        Token.append(d1)


def addtos_word(s):  # 添加至字符串
    global nums
    if not (s in s_word):
        nums = nums + 1
        s_word[s] = nums
    fo.write('<S,%d>\n' % s_word[s])
    d1 = Data('S', 0, s)
    Token.append(d1)


def todo():  # 整活
    global numi
    global nums
    global nump
    global numk
    global numc
    global numch
    global statep
    f = open('input.txt')           # f代表要读取的文件

    lines = f.readlines()           # 读出文件的内容，按行存储在列表lines中
    #print(lines)
    for line in lines:
        lens = len(line)
        #print(line)
        state = 0  # 标识符
        strs = ''  # 存放字符串
        strp = ''  # 存放界符
        strc = ''  # 存放常数
        statech = 0
        i = 0
        while i < lens:
            if line[i] == '\n':
                i += 1
                continue
            if line[i] == '\"' and state == 0:  # 字符串开始
                state = 1
                i += 1
                continue
            elif state == 1 and line[i] == '\"':  # 字符串结束
                addtos_word(strs)
                strs = ''
                i += 1
                continue
            if state == 1 and line[i] != '\"':
                strs = strs + line[i]
                i += 1
                continue
            if line[i] == '\'' and statech == 0:  # 字符
                statech = 1
                i += 1
                continue
            elif statech == 1 and line[i] != '\'':
                if not (line[i] in ch_word):
                    numch = numch + 1
                    ch_word[line[i]] = numch
                fo.write('<CH,%d>\n' % ch_word[line[i]])
                d1 = Data('CH', 0, line[i])
                Token.append(d1)
                i += 1
                continue
            elif statech == 1 and line[i] == '\'':
                statech = 0
                i += 1
                continue
            if line[i] == '/' and line[i + 1] == '/':  # 注释
                i += 1
                break
            if line[i] >= '0' and line[i] <= '9':  # 判断数字
                addtoi_word(strs)
                strs = ''
                strc = strc + line[i]
                i = i + 1
                statec = 0  # 小数点标识符
                while i < len(line) and ((line[i] <= '9' and line[i] >= '0') or line[i] == '.'):
                    if (line[i] == '.' and statec == 0):
                        statec = 1
                        strc = strc + line[i]
                    elif line[i] <= '9' and line[i] >= '0':
                        strc = strc + line[i]
                    elif line[i] == '.' and statec == 1:
                        break
                    i = i + 1
                i = i - 1

                addtoi_word(strs)
                strs=''
                if not (strc in c_word):
                    numc = numc + 1
                    c_word[strc] = numc
                fo.write('<C,%d>\n' % c_word[strc])
                d1 = Data('C', strc, '')
                Token.append(d1)
                strc = ''
                i += 1
                continue
            stn = ''

            stn = line[i]
            if stn in p_word:       # 界符
                addtoi_word(strs)
                strs = ''
                if statep==1:
                    statep=0
                    i += 1
                    continue
                strp = strp + line[i]
                if line[i] == '>' or line[i] == '<' or line[i] == '!' or line[i] == '=':
                    ali = i
                    if ali+1 < len(line):
                        if line[ali+1] == '=':
                            statep=1
                            strp = strp + line[ali+1]
                fo.write('<P,%d>\n' % p_word[strp])
                d1 = Data('P', 0, strp)
                Token.append(d1)

                strp = ''
                i += 1
                continue
            if line[i] == ' ' or line[i] == '\t':
                addtoi_word(strs)
                strs = ''
                i += 1
            elif line[i] != ' ' and line[i]!='\n':
                strs = strs + line[i]
                i += 1
        addtoi_word(strs)
    f.close()


todo()
d1 = Data('#', 0, '#')
Token.append(d1)
fo.close()
