import pickle
from queue import Queue

f = open('outpro.txt', 'rb')
sou = pickle.load(f)


class Node:
    def __init__(self):
        self.fir = ' '
        self.sec = []
        self.op = ' '
        self.can = []


op_tol = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '>=', '<=']
fir = []
sec = []
end = []
Nodes = []
dirt = {}
to = {}
spe = []


def init_node(a):
    t1 = Node()
    t1.fir = a
    Nodes.append(t1)
    dirt[a] = len(Nodes)-1


def is_mid(a):
    if a[-1] == 't':
        if '0' <= a[0] <= '9':
            return True
        else:
            return False
    else:
        return False


def is_num(a):
    if a.replace('.', '', 1).isdigit():
        return True
    else:
        return False


def solve_pro(now):
    spe.clear()
    a = now
    for i in range(0, len(now)):
        if a[i][0] == 'if' or a[i][0] == 'do' or a[i][0] == 'end' or a[i][0] == 'el' or \
                a[i][0] == 'return' or a[i][0] == 'we':
            end.append(a[i])
        elif a[i][0] == 'ie' or a[i][0] == 'wh' or a[i][0] == 'begin' or a[i][0] == 'begin_t':
            fir.append(a[i])
        elif a[i][3] == 'int' or a[i][3] == 'void':
            fir.append(a[i])
            if a[i][0] != ' ':
                if a[i][1] != ' ':
                    spe.append(a[i][1])
                    init_node(a[i][1])
                    Nodes[-1].sec.append(a[i][1])
                if a[i][2] != ' ':
                    spe.append(a[i][2])
                    Nodes[-1].sec.append(a[i][2])
                    init_node(a[i][2])
            else:
                if a[i][1] != ' ':
                    init_node(a[i][1])
                if a[i][2] != ' ':
                    init_node(a[i][2])

        else:
            sec.append(a[i])


def add_node(a, to_pos):
    t1 = to_pos.fir
    if is_mid(t1):
        if is_mid(a):
            to_pos.sec.append(a)
        else:
            to_pos.sec.append(t1)
            to_pos.fir = a
    elif is_num(t1):
        to_pos.sec.append(a)
    else:
        if is_num(a):
            to_pos.sec.append(t1)
            to_pos.fir = a
        else:
            to_pos.sec.append(a)


def find(a):
    for i in range(0, len(Nodes)):
        flag = True
        if Nodes[i].op == a.op and len(Nodes[i].can) == len(a.can):
            for j in range(0, len(Nodes[i].can)):
                if Nodes[i].can[j] != Nodes[i].can[j]:
                    flag = False
                    break
            if flag:
                return i
    return False


def solve():
    i = 0
    ans1 = []
    ans = []
    sp = []
    le = len(sec)-1
    while le >= 0:
        if not is_num(sec[le][3]) and sec[le][3] not in sp:
            sp.append(sec[le][3])
        le -= 1
    while i < len(sec):
        now = sec[i]
        t1 = now[3]
        if t1 in dirt:
            tt1 = dirt[t1]
            ne = Nodes[tt1]
            if ne.fir == t1:
                flag1 = False
                for ti in range(0, len(ne.sec)):
                    if is_num(ne.sec[ti]):
                        ne.fir = ne.sec[ti]
                        ne.sec[ti] = '#'
                        flag1 = True
                        break
                if not flag1:
                    for ti in range(0, len(ne.sec)):
                        if not is_mid(ne.sec[ti]) and ne.sec[ti] != '#':
                            ne.fir = ne.sec[ti]
                            ne.sec[ti] = '#'
                            flag1 = True
                            break
                    if not flag1:
                        for ti in range(0, len(ne.sec)):
                            if ne.sec[ti] != '#':
                                ne.fir = ne.sec[ti]
                                ne.sec[ti] = '#'
                                flag1 = True
                                break
            else:
                for ti in range(0, len(ne.sec)):
                    if ne.sec[ti] == t1:
                        ne.sec[ti] = '#'
                        break
        n1 = Node()
        if now[0] not in op_tol:
            n1.op = now[0]
            while sec[i][0] == now[0]:
                if sec[i][1] != ' ':
                    if sec[i][1] in dirt:
                        p1 = dirt[sec[i][1]]
                        n1.can.append(p1)
                    else:
                        init_node(sec[i][1])
                        p1 = len(dirt)-1
                        n1.can.append(p1)
                if sec[i][2] != ' ':
                    if sec[i][2] in dirt:
                        p1 = dirt[sec[i][2]]
                        n1.can.append(p1)
                    else:
                        init_node(sec[i][2])
                        p1 = len(dirt)-1
                        n1.can.append(p1)
                i += 1
            flag = find(n1)
            if not flag:
                n1.fir = t1
                Nodes.append(n1)
                dirt[now[3]] = len(Nodes)-1
            else:
                dirt[now[3]] = flag
                add_node(now[3], Nodes[flag])
        elif now[0] == '=':
            if now[1].isdigit():
                ans1.append(now)
            if now[1] in dirt:
                t2 = Nodes[dirt[now[1]]]
            else:
                init_node(now[1])
                t2 = Nodes[len(Nodes)-1]
            dirt[now[3]] = len(Nodes)-1
            add_node(now[3], t2)
            i += 1
        else:
            n1.op = now[0]
            if sec[i][1] != ' ':
                if sec[i][1] in dirt:
                    p1 = dirt[sec[i][1]]
                    n1.can.append(p1)
                else:
                    init_node(sec[i][1])
                    p1 = len(dirt) - 1
                    n1.can.append(p1)
            if sec[i][2] != ' ':
                if sec[i][2] in dirt:
                    p1 = dirt[sec[i][2]]
                    n1.can.append(p1)
                else:
                    init_node(sec[i][2])
                    p1 = len(dirt) - 1
                    n1.can.append(p1)
            flag = find(n1)
            if not flag:
                n1.fir = t1
                Nodes.append(n1)
                dirt[now[3]] = len(Nodes)-1
            else:
                dirt[now[3]] = flag
                add_node(now[3], Nodes[flag])
            i += 1
    sp_t = []
    sp_s = sp
    pq = Queue(maxsize=10000)
    for i in range(0, len(fir)):
        ans.append(fir[i])

    get = []
    for i in range(0, len(sp)):
        if sp[i] not in sp_t:
            t1 = dirt[sp[i]]
        pq.put(t1)
        while pq.qsize() > 0:
            t1 = pq.get()
            if Nodes[t1].fir in sp_t:
                continue
            if dirt[Nodes[t1].fir] == t1:
                sp_t.append(Nodes[t1].fir)
            j = 0
            op = Nodes[t1].op
            type = Nodes[t1].fir
            nn = []
            ss = []
            ss1 = []
            while j < len(Nodes[t1].can):
                s1 = Nodes[t1].can[j]
                tt1 = ' '
                tt2 = ' '
                if j < len(Nodes[t1].can):
                    tt1 = Nodes[t1].can[j]
                    tt1 = Nodes[tt1].fir
                    pt1 = dirt[tt1]
                    if len(Nodes[pt1].can) > 0:
                        pq.put(pt1)
                    j += 1
                if j < len(Nodes[t1].can):
                    tt2 = Nodes[t1].can[j]
                    tt2 = Nodes[tt2].fir
                    pt2 = dirt[tt2]
                    if len(Nodes[pt2].can) > 0:
                        pq.put(pt2)
                    j += 1
                nn.append(op)
                nn.append(tt1)
                nn.append(tt2)
                nn.append(type)
                ss.append(nn)
            lee = len(ss)-1
            while lee >= 0:
                get.append(ss[lee])
                lee -= 1
    for i in range(0, len(ans1)):
        ans.append(ans1[i])
    lee2 = len(get)-1
    while lee2 >= 0:
        ans.append(get[lee2])
        lee2 -= 1
    for i in range(0, len(end)):
        ans.append(end[i])
    return ans


final = []


def main():
    print(sou)
    for i in range(0, len(sou)):
        ss1 = []
        solve_pro(sou[i])
        ss1 = solve()
        fir.clear()
        sec.clear()
        end.clear()
        final.append(ss1)
    print(final)


if __name__ == '__main__':
    main()