import word_analyzer
import lexicalpro

Dirt = lexicalpro.dirt
Grammar = lexicalpro.Grammar
Token = word_analyzer.Token
Map = lexicalpro.mapa
List1 = []  # 处理声明语句
Get = []  # 存入最终四元式
Pick = []  # 进行语法分析
Stack = []  # 符号表处理栈，存储活动记录

Len = {'int': 2, 'float': 8, 'double': 8, 'char': 1, 'bool': 1}  # 长度表


class Ed:
    def __init__(self):
        self.type = ''
        self.val = ''


class Funi:  # 定义函数表元素
    def __init__(self):
        self.name = ''   # 函数名
        self.type = ''   # 函数返回类型
        self.level = ''  # 函数的层次
        self.off = ''    # 函数的区距
        self.num = ''    # 函数参数个数
        self.param = ''  # 函数参数表
        self.bl = []     # 函数变量表
        self.entry = ''  # 函数入口地址

    def add(self, name):
        if self.bl.get(name):
            print('error3')
        else:
            self.bl.add(name)


class Fun:  # 函数表总表
    def __init__(self):
        self.tol = []

    def get(self, name):
        for i in range(0, len(self.tol)):
            if self.tol[i].name == name:
                return self.tol[i].type
        return False

    def add(self, name):
        self.tol.append(name)

    def addsym(self, ss):
        self.tol[-1].num = ss.len()
        self.tol[-1].param = ss

    def addele(self, ss):
        self.tol[-1].bl.append(ss)


Funs = Fun()  # 函数表


class Elem:  # 表示数据表
    def __init__(self):
        self.name = ''  # 定义结构体名，基本数据为数据类型，结构体等为结构体名
        self.val = ''  # 指向数据实际结构，基本数据为''
        self.len = 0  # 定义数据类型的长度

    def add(self, name):
        if name in Len:
            self.len = Len[name]
            self.val = ''
            self.name = name
        # 结构体和数组长度再加
        return self


class Sym:  # 单个变量表元素
    def __init__(self):
        self.name = ''  # 数据名称
        self.type = ''  # 表示数据类型,i为整型,d为double,b为bool,c为char,f为float
        self.to = ''  # 存下对应的数据类

    def add(self, name):
        if name in Len:
            ss = Elem()
            self.to = ss.add(name)
        # 结构体和数组长度再加


class Symbol:  # 变量表类
    def __init__(self):
        self.tol = []

    def get(self, name):
        for i in range(0, len(self.tol)):
            if self.tol[i].name == name:
                return self.tol[i].type
        return False

    def add(self, ss):
        self.tol.append(ss)

    def len(self):
        return len(self.tol)


Tol = Symbol()  # 全局变量表
Can = Symbol()  # 函数行参数


def solve_pro():
    j = len(Token) - 1
    while j >= 0:
        if Token[j].str == 'int' or Token[j].str == 'void':
            List1.append(Token[j])
            List1.append(Token[j + 1])
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


def solve():
    stack = ['#', 'q1']
    i = 0
    while i < len(Pick) - 1:
        now = stack[-1]
        tt1 = Map[Pick[i].type]
        if now == 'mm1':
            l1 = List1[-1]
            List1.pop()
            l2 = List1[-1]
            List1.pop()
            s1 = Sym()
            s1.name = l1.str
            s1.type = l2.str
            e1 = Elem()
            e1.add(l2.str)
            s1.to = e1
            Tol.add(e1)
            stack.pop()
        elif now == 'mm2':
            l1 = List1[-1]
            List1.pop()
            l2 = List1[-1]
            List1.pop()
            ss = Funi()
            ss.name = l1.str
            ss.type = l2.str
            if not Funs.get(ss.name):
                Funs.add(ss)
            else:
                print('error2')
            stack.pop()
        elif now == 'mm3':
            l1 = List1[-1]
            List1.pop()
            l2 = List1[-1]
            List1.pop()
            ss = Sym()
            ss.name = l1.str
            ss.type = l2.str
            ss.add(l2.str)
            if not Can.get(l1.str):
                Can.add(ss)
            else:
                print('error1')
            stack.pop()
        elif now == 'mm4':
            l1 = List1[-1]
            List1.pop()
            l2 = List1[-1]
            List1.pop()
            ss = Sym()
            ss.name = l1.str
            ss.type = l2.str
            ss.add(l2.str)
            Funs.addele(ss)
            stack.pop()
        elif now == 'mm5':
            Funs.addsym(Can)
            Can.tol.clear()
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
                    while i < len(Pick) - 1 and stack[-1] == Pick[i].type:
                        i += 1
                        stack.pop()


def main():
    solve_pro()
    solve()


if __name__ == '__main__':
    main()

# grammar3.txt
