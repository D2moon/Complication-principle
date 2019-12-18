import word_analyzer
import lexicalpro

Dirt = lexicalpro.dirt
Grammar = lexicalpro.Grammar
Token = word_analyzer.Token
Mapa = lexicalpro.mapa


class Node:  # 四元式类
    def __init__(self):
        self.type = ''
        self.op = ''
        self.t1 = ''
        self.t2 = ''


class Ed:
    def __init__(self):
        self.type = ''
        self.val = ''


tol = 0  # 四元式的中间变量
List1 = []  # 处理声明语句
Get = []  # 存入最终四元式
Pick = []  # 进行语法分析
Can = []  # 存函数参数
Bds = []  # 处理表达式


def solve_pro():
    j = len(Token)-1
    while j >= 0:
        if Token[j].str == 'int' or Token[j].str == 'void':
            List1.append(Token[j])
            List1.append(Token[j+1])
        j -= 1
    for i in range(0, len(Token)):
        t1 = Ed()
        if Token[i].type == 'C':
            t1.type = 'sz'
            t1.val = Token[i].val
        elif Token[i].type == 'P' or Token[i].type == 'K':
            t1.type = Token[i].str
            t1.val = Token[i].str
        elif Token[i].type == 'I':
            t1.type = 'id'
            t1.val = Token[i].str
        Pick.append(t1)


fu = []
shu = []


def new_id():
    global tol
    idd = str(tol)
    tol += 1
    idd += 't'
    return idd


def call():
    to = Node()
    to.t2 = shu[-1].val
    shu.pop()
    to.t1 = shu[-1].val
    shu.pop()
    idd = new_id()
    to.op = fu[-1]
    fu.pop()
    to.type = idd
    tt = Ed()
    tt.type = 'I'
    tt.val = idd
    Get.append(to)
    shu.append(tt)


def todo():
    if len(Bds) == 0:
        return ''
    if len(Bds) == 1:
        return Bds[0].val
    fu.append('#')
    level = {'#': 6, '(': 5, '*': 4, '/': 4, '+': 3, '-': 3, ')': 2}
    for i in range(0, len(Bds)):
        if Bds[i].type == 'id' or Bds[i].type == 'sz':
            shu.append(Bds[i])
        else:
            t1 = Bds[i].val
            t2 = fu[-1]
            if t2 == '#':
                fu.append(t1)
            elif t2 == '(' and t1 == ')':
                fu.pop()
            elif t2 == '(':
                fu.append(t1)
            elif level[t2] < level[t1]:
                fu.append(t1)
            else:
                flag = True
                while level[t2] >= level[t1]:
                    t2 = fu[-1]
                    if t2 == '(' and t1 == ')':
                        fu.pop()
                        flag = False
                        break
                    elif t2 == '#' and t1 == '#':
                        fu.pop()
                        flag = False
                    else:
                        call()
                if flag:
                    fu.append(t1)
    while len(shu) > 1:
        call()
    mt = shu[-1].val
    shu.clear()
    fu.clear()
    return mt


def solve():
    stack = ['#', 'q1']
    i = 0
    le = ''
    id1 = ''
    opt = ''
    sign = ''
    re = ''
    flag = False
    ss1 = ''
    ss2 = ''
    while i < len(Pick)-1:
        now = stack[-1]
        tt1 = Mapa[Pick[i].type]
        if flag:
            if now == 'mm7':
                flag = False
                sign = Pick[i].type
                ss1 = todo()
                Bds.clear()
                stack.pop()
            elif now == 'mm9':
                to = Node()
                flag = False
                ss2 = todo()
                Bds.clear()
                to.type = new_id()
                to.op = sign
                sign = ''
                to.t1 = ss1
                to.t2 = ss2
                ss1 = ''
                ss2 = ''
                tot = Node()
                Get.append(to)
                stack.pop()
                if opt == 'while':
                    tot.op = 'do'
                    tot.type = to.type
                    Get.append(tot)
                elif opt == 'if':
                    tot.op = 'if'
                    tot.type = to.type
                    Get.append(tot)
            elif now == 'mm11':
                flag = False
                re = todo()
                Bds.clear()
                to = Node()
                to.op = 'return'
                to.type = re
                Get.append(to)
                stack.pop()
            elif now == 'mm13':
                flag = False
                re = todo()
                Bds.clear()
                to = Node()
                to.op = '='
                to.type = id1
                id1 = ''
                to.t1 = re
                Get.append(to)
                stack.pop()
            else:
                if now in Dirt:
                    stack.pop()
                    ne = Dirt[now][tt1]
                    for j in range(0, len(Grammar[ne])):
                        if Grammar[ne][j] == '!':
                            break
                        stack.append(Grammar[ne][j])
                else:
                    if now == Pick[i].type:
                        while i < len(Pick)-1 and stack[-1] == Pick[i].type:
                            Bds.append(Pick[i])
                            i += 1
                            stack.pop()
        elif now == 'mm2' or now == 'mm5':
            l1 = List1[-1]
            List1.pop()
            l2 = List1[-1]
            List1.pop()
            to = Node()
            to.type = l2.str
            to.t1 = l1.str
            Get.append(to)
            stack.pop()
        elif now == 'mm4':
            l1 = List1[-1]
            List1.pop()
            l2 = List1[-1]
            List1.pop()
            if le == '':
                le = l2.str
            Can.append(l1.str)
            stack.pop()
        elif now == 'mm6' or now == 'mm8' or now == 'mm10' or now == 'mm12':
            flag = True
            stack.pop()
        elif now == 'mm14':
            to = Node()
            to.op = 'else'
            Get.append(to)
            stack.pop()
        elif now == 'mm15':
            to = Node()
            to.op = 'ie'
            Get.append(to)
            stack.pop()
        elif now == 'mm16':
            to = Node()
            to.op = 'we'
            Get.append(to)
            stack.pop()
        elif now == 'tt2':
            l1 = List1[-1]
            List1.pop()
            l2 = List1[-1]
            List1.pop()
            if len(Can) == 0:
                to = Node()
                to.type = l2.str
                to.op = l1.str
                Get.append(to)
            else:
                j = 1
                ttt = l1.str
                l1.str = Can[0]
                Can[0] = ttt
                Can.append(Can[0])
                l2.str = le
                le = ''
                while j < len(Can):
                    t1 = ''
                    t2 = ''
                    if j < len(Can):
                        t1 = Can[j]
                        j += 1
                    if j < len(Can):
                        t2 = Can[j]
                        j += 1
                    to = Node()
                    to.type = l2.str
                    to.op = l1.str
                    print(to.op)
                    to.t2 = t2
                    to.t1 = t1
                    Get.append(to)
                Can.clear()
            tot = Node()
            tot.op = 'begin'
            Get.append(tot)
            stack.pop()
        elif now == 'tt3':
            to = Node()
            to.op = 'end'
            Get.append(to)
            stack.pop()
        else:
            if now in Dirt:
                stack.pop()
                ne = Dirt[now][tt1]
                for j in range(0, len(Grammar[ne])):
                    if Grammar[ne][j] == '!':
                        break
                    stack.append(Grammar[ne][j])
            else:
                if now == Pick[i].type:
                    while i < len(Pick)-1 and stack[-1] == Pick[i].type:
                        if Pick[i].val == 'while':
                            tot = Node()
                            tot.op = 'while'
                            Get.append(tot)
                            opt = 'while'
                        elif Pick[i].val == 'if':
                            opt = Pick[i].val
                        elif Pick[i].type == 'id':
                            id1 = Pick[i].val
                        i += 1
                        stack.pop()


def toprint():
    for i in range(0, len(Get)):
        print('<', end='')
        print(Get[i].op, end=', ')
        print(Get[i].t1, end=', ')
        print(Get[i].t2, end=', ')
        print(Get[i].type, end='>')
        print('')


def main():
    global tol
    tol = 1
    solve_pro()
    solve()
    to = Node()
    to.op = 'end'
    Get.append(to)
    toprint()


if __name__ == '__main__':
    main()


# grammar2.txt
