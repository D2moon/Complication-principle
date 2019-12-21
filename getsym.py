import translate
import sys
translate.main()
Get = translate.Get
t_tol = translate.tol
pos = 0
Map = {}  # 映射函数到四元式
Map1 = {}
idl = ''
Len = {'int': 2, 'float': 8, 'double': 8, 'char': 1, 'bool': 1}  # 长度表


def get_st(lens):
    global pos
    pp = pos
    pos = pos + lens
    pp = str(pp)
    p1 = 'DS:[' + pp
    p1 = p1 + ']'
    return p1


class Ed:
    def __init__(self):
        self.type = ''
        self.val = ''


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
        self.len = 0  # 数据长度
        self.pos = 0  # 数据起始地址

    def add(self, name):
        if name in Len:
            ss = Elem()
            self.to = ss.add(name)
            self.len = self.to.len
            self.pos = get_st(self.len)
        # 结构体和数组长度再加

    def get_pos(self):
        return self.pos


class Symbol:  # 变量表类
    def __init__(self):
        self.tol = []

    def get(self, name):
        for i in range(0, len(self.tol)):
            if self.tol[i].name == name:
                return i
        return False

    def add(self, ss):
        self.tol.append(ss)

    def len(self):
        return len(self.tol)


Sym_tol = Symbol()


class Han:
    def __init__(self):
        self.st = 0
        self.en = 0
        self.num = 0
        self.can = []
        self.bl = []
        self.len = 0
        self.name = ''
        self.type = ''


class Hans:
    def __init__(self):
        self.han = []

    def find(self, name):
        for i in range(0, len(self.han)):
            if self.han[i].name == name:
                return True
        return False

    def add(self, name):
        self.han.append(name)

    def todo(self):
        for i in range(0, len(self.han)):
            Map[self.han[i].name] = i


Han_tol = Hans()


class Funi:  # 定义函数表元素
    def __init__(self):
        self.name = ''  # 函数名
        self.type = ''  # 函数返回类型
        self.num = ''  # 函数参数个数
        self.param = Symbol()  # 函数参数表
        self.bl = Symbol()  # 函数变量表

    def get(self, name):
        t1 = self.param.get(name)
        if not t1:
            t2 = self.bl.get(name)
            if not t2:
                return False
            return self.bl.tol[t2].pos
        return self.param.tol[t1].pos


Stack = []  # 函数处理栈


def solve_pro():
    global idl
    for i in range(0, t_tol):
        new = Sym()
        idl = str(i)+'t'
        print(idl)
        new.name = idl
        new.type = 'int'
        new.add('int')
        Sym_tol.add(new)
        idl = ''
    flag = False
    for i in range(0, len(Get)):
        if Get[i].op == '' and Get[i].type == 'int':
            new = Sym()
            new.name = Get[i].t1
            new.type = Get[i].type
            new.add(Get[i].type)
            if not flag:
                Sym_tol.add(new)
            else:
                Han_tol.han[-1].bl.append(new)
        if Get[i].op == 'begin' or Get[i].op == 'begin_t':
            flag = True
            j = i - 1
            new = Han()
            new.st = i + 1
            name = Get[j].op
            new.name = name
            idl = name
            new.type = Get[j].type
            while j >= 0 and Get[j].op == name:
                if Get[j].t1 != '':
                    new.num += 1
                    new.can.insert(0, Get[j].t1)
                if Get[j].t2 != '':
                    new.num += 1
                    new.can.insert(0, Get[j].t2)
                j -= 1
            Han_tol.add(new)

        elif Get[i].op == 'end':
            Han_tol.han[-1].len = Han_tol.han[-1].num * 2
            Han_tol.han[-1].en = i - 1
        elif Get[i].op == 'return':
            Map1[idl] = Get[i].type
    Han_tol.todo()


def find_re(now):
    return get_pos(Map1[now])


def solve(now):
    if Get[now].type == 'int' and Get[now].op == '':
        new = Sym()
        new.name = Get[now].t1
        new.type = 'int'
        new.add('int')
        Stack[-1].bl.add(new)
    elif Get[now].type == 'int' or Get[now].type == 'void':
        if Get[now].op in Map and Get[now-1].type != Get[now].type:
            new = Funi()
            ti = Map[Get[now].op]
            last = Han_tol.han[ti]
            new.name = last.name
            new.type = last.type
            for i in range(0, len(last.can)):
                sp = Sym()
                sp.name = last.can[i]
                sp.type = 'int'
                sp.add('int')
                new.param.add(sp)
            for i in range(0, len(last.bl)):
                sp = Sym()
                sp.name = last.bl[i]
                sp.type = 'int'
                sp.add('int')
                new.bl.add(sp)
            Stack.append(new)
        else:
            return
    elif Get[now].op == 'end':
        Stack.pop()


def get_pos(now):
    print(now, end=' pos = ')
    ns = Stack[-1]
    t1 = ns.get(now)
    if not t1:
        t2 = Sym_tol.get(now)
        if not t2:
            print(now, end='为未定义变量')
        else:
            print(Sym_tol.tol[t2].get_pos())
            return Sym_tol.tol[t2].get_pos()
    else:
        print(t1)
        return t1


def main():
    translate.main()
    solve_pro()


if __name__ == '__main__':
    main()
