# from queue import Queue,LifoQueue,PriorityQueue
import re  # 正则表达式匹配模块
import sys  # 停止程序暂停模块
import pickle
from collections import deque  # 队列区域
import getsym

getsym.main()

f = open('outpro.txt', 'rb')
QT = pickle.load(f)
print(QT)
#
'''
QT = [
        [['main', ' ', ' ', 'int'], ['begin_t', ' ', ' ', ' '], [' ', 'b', ' ', 'int'], [' ', 'c', ' ', 'int'],
        ['=', 5, ' ', 'c'], ['=', 0, ' ', 'b'], ['>', 'c', 2, '1t'], ['if', '1t', ' ', ' ']],
        [['!=', 'c', 'b', '2t'], ['if', '2t', ' ', ' ']],
        [['+', 'c', 3, '3t']],
        [['ie', ' ', ' ', ' '], ['=', 7, ' ', 'c']],
        [['ie', ' ', ' ', ' '], ['*', 'b', 'c', '4t'], ['=', '4t', ' ', 'b'], ['end', ' ', ' ', ' ']]

 ]  # 算术四元组区
 '''
# RDL = {'R0`': 'null', 'R1`': 'null', "M*": ['a', 'b', 'c', 'd']}  # 寄存器状态描述表  当前变量x值在该寄存器中
# RDL = {'R`': 'null', 'M*': ['a', 'b', 'c', 'x']}
RDL = {'R0`': 'null', 'R1`': 'null', "M*": []}
ANS = []  # 汇编代码生成存储部分
operator = {"*", "+", "-", "/"}
operator1 = {"*": 'MUL', '/': 'DIV', '+': 'ADD', '-': 'SUB'}
operator2 = {'>', '<', '>=', '<=', '!=', '=='}
operator3 = {'>': 'JBE', '<': 'JAE', '>=': 'JB', '<=': 'JA', '!=': 'JE', '==': 'JNE'}
# 特别用例seg4——仿造状态表
seg4 = {}
# 用于存储最新状态
seg5 = {}
# 用于标注跳转模式状态
goto_state = deque()
# goto_state1 =deque()
switch_wh = 0
# 存储if while 子函数标号的地址栈
if_stack = deque()  # 放的是回填的位置
delay_stack = []  # 延时栈
while_stack = deque()  # 放的是回填内容和回填位置，会自动进行区分
do_stack1 = []
do_stack2 = []
# 哈哈哈，绝了，神他妈两种思路
# 跳转位置标号规则设置记录栈
f_count = []
# 生成指令数
order_quantity = 0
# 函数返回数据类型
function_data_type = ["int", 'void']
function_name = []
# 四元式头值区分
four_head = ["+", '-', '*', '/', 'return', 'wh', 'do', 'we', 'if', 'el', 'ie', 'begin', 'end', 'begin_t']
# 主函数状态
if_main = []
# 指令数量
num_instructions = 0
# 寄存器对应
register_list = {"R0`": "BX", 'R1`': "CX"}
# 数据类型
data_type = ['int', 'float']
#
function_name1 = ' '
start = 0


# 从符号表中单独读取 出所有变量名称


def get_names(table):
    SEQ1 = []
    for i_nan in table:
        if i_nan[0] in operator or i_nan[0] == '=' or i_nan[0] in operator2:
            for k in range(1, 4):
                if SEQ1.count(i_nan[k]) == 0 and type(i_nan[k]) == str and i_nan[k] != " ":
                    SEQ1.append(i_nan[k])
    for boy in SEQ1:
        seg5[boy] = 0
    return SEQ1


# 多寄存器活跃状态填写函数


def is_active_plus(seg1, seg2):
    # 初始化状态表 seg1 ——变量表
    # seg2基本块内四元式区
    # 该函数修改seg2 返回seg3——最终的各个变量（含中间变量）活跃状态表
    seg3 = {}
    num = len(seg2) - 1

    for item in range(0, len(seg1)):
        if re.match(r'^[0-9]+t', seg1[item]) is None:
            seg3[seg1[item]] = "y"
        else:
            seg3[seg1[item]] = "n"

    # print(seg3)
    while num >= 0:
        if seg2[num][0] in operator or seg2[num][0] == '=' or seg2[num][0] in operator2:
            no = 3
            while no >= 0:
                if seg2[num][no] in seg3.keys():
                    np = seg2[num][no]
                    seg2[num][no] = {seg2[num][no]: seg3[np]}
                    if no == 3:
                        seg3[np] = 'n'
                    else:
                        seg3[np] = num + 1
                no = no - 1
        num = num - 1
    return seg3


#  寻址函数 location(X)=Ri则其证明其在Ri中，


def location(x):
    # if x == 'null' or type(x) == int:
    # print("fuck")
    # sys.exit(0)
    if re.match(r'^R[0-9]*`$', x):
        if RDL[x] == 'null':
            #  print(x + "此寄存器为空")
            return x
        else:
            return location(RDL[x])
    else:
        for name in RDL.keys():
            if name != 'M*' and RDL[name] == x:
                #  print(x + "存于寄存器" + name + "中")
                return name
        if x in RDL['M*']:
            # print(x + "已存于内存中")
            return x
        else:
            print(x + "所代表值并未存储，无法查址")
            return "null"


# 寄存器求取函数
def getR(Q, r_add, b_add, c_add):
    # 四元式必须是可以利用该函数的，确认好的东西
    global order_quantity
    py = []  # 活跃向量
    for girl in range(0, 4):
        if type(Q[girl]) == dict:
            h = list(Q[girl].keys())
            if h[0] not in py:
                py.append(h[0])
                seg5[h[0]] = Q[girl][h[0]]
    state1 = 0
    if type(Q[1]) != dict and type(Q[2]) != dict:
        state1 = 3
        b_add = str(Q[1])
        c_add = str(Q[2])
    elif type(Q[1]) != dict and type(Q[2]) == dict and (Q[0] != "+" and Q[0] != "*"):
        b_add = str(Q[1])
        state1 = 5

    for i in RDL:
        if i != "M*" and type(Q[1]) == dict and RDL[i] in Q[1]:
            state1 = 1
            break

        elif (type(Q[2]) == dict and type(Q[1]) == int and (Q[0] == "+" or Q[0] == "*")) or \
                (i != "M*" and (type(Q[2]) == dict and RDL[i] in Q[2]) and (Q[0] == "+" or Q[0] == "*")):
            t = Q[2]
            Q[2] = Q[1]
            Q[1] = t
            return getR(Q, r_add, b_add, c_add)

    if state1 == 1:
        # print("主动释放")
        name = RDL[i]
        if (seg5[name] == 'y' or (type(seg5[name]) == int and seg5[name] > 0)) and \
                (name not in RDL['M*'] or name not in Q[3]):
            state2 = 0
            for j in RDL.keys():
                if RDL[j] == "null" and Q[0] != '=':
                    ANS.append("MOV " + register_list[j] + ", " + register_list[i])
                    order_quantity = order_quantity + 1
                    RDL[j] = name
                    state2 = 1
                    break
            if state2 == 0:
                ANS.append("MOV " + getsym.get_pos(name) + ", " + register_list[i])
                order_quantity = order_quantity + 1
                RDL['M*'].append(name)
        r_add = location(i)
        b_add = location(list(Q[1].keys())[0])
        if (Q[0] in operator or Q[0] in operator2) and type(Q[2]) == dict:
            c_add = location(list(Q[2].keys())[0])
        elif type(Q[2]) == int:
            c_add = str(Q[2])
        else:
            c_add = "null"
        RDL[i] = "null"
        return [r_add, b_add, c_add]
    elif state1 == 3:  # 两操作数皆为数据
        for jk in RDL.keys():
            if jk != "M*" and RDL[jk] == "null":
                state1 = 4
                break
        if state1 == 4:
            r_add = jk
            return [r_add, b_add, c_add]
        else:
            list2 = list(RDL.keys())
            list2.remove("M*")
            grade1 = 0
            for name1 in list2:
                if seg5[RDL[name1]] == 'n':
                    r_add = name1
                    RDL[r_add] = 'null'
                    return [r_add, b_add, c_add]
                elif seg5[RDL[name1]] == 'y':
                    r_add = name1
                    break
                else:
                    if seg5[RDL[name1]] > grade1:
                        r_add = name1
                        grade1 = seg5[RDL[name1]]
            if RDL[r_add] not in RDL['M*']:
                RDL["M*"].append(RDL[r_add])
            RDL[r_add] = "null"
            return [r_add, b_add, c_add]
    elif state1 == 5:  # 不可交换 数 + 变量的  空替换 和强制替换
        # print("数+字典+不可交换")
        grade2 = 0
        for ik in RDL.keys():
            if ik != "M*" and RDL[ik] == "null":
                r_add = location(ik)
                c_add = location(list(Q[2].keys())[0])
                return [r_add, b_add, c_add]
            elif ik != "M*" and seg5[RDL[ik]] == 'n':
                r_add = location(ik)
                if RDL[r_add] in list(Q[2].keys()) and RDL[r_add] not in RDL["M*"]:
                    h_name = getsym.get_pos(RDL[r_add])
                    ANS.append("MOV " + h_name + ', ' + register_list[r_add])
                    order_quantity = order_quantity + 1
                    RDL['M*'].append(RDL[ik])
                RDL[ik] = "null"
                c_add = location(list(Q[2].keys())[0])
                return [r_add, b_add, c_add]
            elif ik != "M*" and seg5[RDL[ik]] == 'y':
                state1 = 7
                r_add = location(ik)

            elif ik != "M*" and seg5[RDL[ik]] > grade2 and state1 == 5:
                grade2 = seg5[RDL[ik]]
                r_add = location(ik)
        if RDL[r_add] not in RDL['M*']:
            ANS.append("MOV " + getsym.get_pos(RDL[r_add]) + ', ' + register_list[r_add])
            order_quantity = order_quantity + 1
            ['M*'].append(RDL[r_add])
        RDL[r_add] = "null"
        return [r_add, b_add, location(list(Q[2].keys())[0])]
    else:
        for i in RDL.keys():
            if i != "M*" and RDL[i] == "null":
                state1 = 2
                break
        if state1 == 2:
            # print("选空闲者")
            r_add = location(i)
            b_add = location(list(Q[1].keys())[0])
            if (Q[0] in operator or Q[0] in operator2) and type(Q[2]) == dict:
                c_add = location(list(Q[2].keys())[0])
            elif type(Q[2]) == int:
                c_add = str(Q[2])
            else:
                c_add = "null "
            return [r_add, b_add, c_add]
        else:
            # print("强制释放")
            list1 = list(RDL.keys())
            list1.remove("M*")
            grade = " "
            register = " "
            state3 = 0
            grade1 = 0
            for name in list1:
                if seg5[RDL[name]] == 'n':
                    if type(Q[2]) == dict and RDL[name] in Q[2].keys():
                        continue
                    grade = RDL[name]
                    register = name
                    state3 = 1
                    break
                elif seg5[RDL[name]] == 'y':
                    state3 = 2
                    break
                else:
                    if seg5[RDL[name]] > grade1:
                        grade1 = seg5[RDL[name]]
                        register = name
                        grade = RDL[name]
            if state3 == 2:
                register = name
                grade = RDL[register]
            if grade not in RDL['M*'] and grade != "null" and state3 != 1:
                ANS.append("MOV " + getsym.get_pos(grade) + ", " + register_list[register])
                order_quantity = order_quantity + 1
                RDL['M*'].append(grade)
            r_add = location(register)
            b_add = location(list(Q[1].keys())[0])
            if (Q[0] in operator or Q[0] in operator2) and type(Q[2]) == dict:
                c_add = location(list(Q[2].keys())[0])
            elif type(Q[2]) == int:
                c_add = str(Q[2])
            else:
                c_add = "null"
            RDL[register] = "null"
            return [r_add, b_add, c_add]


# 生成汇编代码


def mak_assemble(tetrad):
    R_add = ' '
    B_add = ' '
    C_add = ' '
    global switch_wh
    global function_name1
    global order_quantity
    global num_instructions
    global start
    if tetrad[0] == 'end':
        for jk in RDL.keys():
            if jk != "M*" and RDL[jk] != 'null':
                if seg5[RDL[jk]] != 'n' and seg5[RDL[jk]] != 0 and RDL[jk] not in RDL['M*']:
                    # print(seg5)
                    # print(QT)
                    h = getsym.get_pos(RDL[jk])
                    if type(h) != str:
                        print(h)
                        sys.exit(-3)
                    ANS.append("MOV " + h + ', ' + register_list[jk])
                    RDL['M*'].append(RDL[jk])
                    RDL[jk] = 'null'
                elif seg5[RDL[jk]] == 'n':
                    RDL[jk] = 'null'

    getsym.solve(num_instructions)
    num_instructions = num_instructions + 1
    order_quantity = 0
    # address获取为空调试函数  千万误删！！！！
    '''
    for i in range(0,len(address)):
        #print(type(address[i]))
        if address[i]==None:
            print(str(i)+"处值为空 "+"四元式为")
            print(tetrad)
            print(ANS)
            print(RDL)
            sys.exit(0)

'''
    if tetrad[0] == '=':
        address = getR(tetrad, R_add, B_add, C_add)
        '''
        for i in range(0, len(address)):
            # print(type(address[i]))
            if address[i] == "null":
                print(str(i) + "处值为空 " + "四元式为")
                print(tetrad)
                print(ANS)
                print(RDL)
                sys.exit(0)
        '''
        if address[0] != address[1]:
            h_name = address[1]
            if not h_name.isdigit():
                h_name = getsym.get_pos(h_name)
            else:
                h_name = num_change(hex(int(h_name))) + "H"

            if address[0] not in register_list.keys():
                print(address[0])
                sys.exit(-2)
            if not h_name:
                print(address[1])
                print(address)
                print(tetrad)
                sys.exit(-1)
            if type(register_list[address[0]]) != str or type(h_name) != str:
                print(register_list[address[0]])
                print(h_name)
                sys.exit(0)
            ANS.append("MOV " + register_list[address[0]] + ", " + h_name)
            order_quantity = order_quantity + 1
        if tetrad == ['=', {'3t': 'n'}, ' ', {'c': 'y'}]:
            print(order_quantity)
            print(ANS[len(ANS) - 1])
            print(RDL)

        mm = list(tetrad[3].keys())
        if mm[0] in RDL['M*']:
            RDL['M*'].remove(mm[0])
        for j in RDL:
            if j != 'M*' and RDL[j] == mm[0]:
                RDL[j] = 'null'
        RDL[address[0]] = mm[0]
    elif tetrad[0] in operator:
        address = getR(tetrad, R_add, B_add, C_add)
        if address[0] != address[1]:
            if not address[1].isdigit():
                h_name = getsym.get_pos(address[1])
                ANS.append("MOV " + register_list[address[0]] + ", " + h_name)
            else:
                h_name = num_change(hex(int(address[1]))) + "H"
                ANS.append("MOV " + register_list[address[0]] + ", " + h_name)
            order_quantity = order_quantity + 1
        op = operator1[tetrad[0]]
        if op == "MUL" or op == "DIV":
            ANS.append("MOV AX," + register_list[address[0]])
            if not address[2].isdigit() and re.match(r'^R[0-9]+`', address[2]) is None:
                h_name = getsym.get_pos(address[2])
                ANS.append(op + " " + h_name)
                order_quantity = order_quantity + 1
            elif re.match(r'^R[0-9]+`', address[2]):
                h_name = register_list[address[2]]
                ANS.append(op + " " + h_name)
                order_quantity = order_quantity+1
            else:
                h_name = num_change(hex(int(address[2]))) + "H"
                ANS.append("MOV DX, " + h_name)
                ANS.append(op + ' DX')
                order_quantity = order_quantity + 2
            h = getsym.get_pos(list(tetrad[3].keys())[0])
            ANS.append("MOV " + h + ",AX")
            print(RDL)
            print(tetrad[3])
            RDL['M*'].append(list(tetrad[3].keys())[0])

        else:
            h_name = address[2]
            if not h_name.isdigit() and re.match(r'^R[0-9]+`$', h_name) is None:
                h_name = getsym.get_pos(h_name)
            elif re.match(r'^R[0-9]+`$', h_name):
                h_name = register_list[h_name]
            else:
                h_name = num_change(hex(int(h_name))) + "H"
            print(tetrad)
            ANS.append(op + ' ' + register_list[address[0]] + ', ' + h_name)
            order_quantity = order_quantity + 1
        mm = list(tetrad[3].keys())
        if mm[0] in RDL['M*']:
            RDL['M*'].remove(mm[0])
        for j in RDL:
            if j != 'M*' and RDL[j] == mm[0]:
                RDL[j] = 'null'
        RDL[address[0]] = mm[0]
    elif tetrad[0] == 'if':
        goto_state.append(1)
        if_stack.append(len(ANS) - 1)
    elif tetrad[0] == 'el':  # 此处为无条件跳转
        for jk in RDL.keys():
            if jk != "M*" and RDL[jk] != 'null':
                if seg5[RDL[jk]] != 'n' and seg5[RDL[jk]] != 0 and RDL[jk] not in RDL['M*']:
                    h_name = getsym.get_pos(RDL[jk])
                    ANS.append("MOV " + h_name + ', ' + register_list[jk])
                    order_quantity = order_quantity + 1
                    RDL['M*'].append(RDL[jk])
                    RDL[jk] = 'null'
        ANS.append("JMP ")
        order_quantity = order_quantity + 1
        delay_stack.append(if_stack.pop())
        if_stack.append(len(ANS) - 1)
        goto_state.append(2)
        return False
    elif tetrad[0] == 'ie':
        for t_name in RDL.keys():
            if t_name != 'M*' and RDL[t_name] in seg5 and seg5[RDL[t_name]] != 'n' \
                    and seg5[RDL[t_name]] != 0 and RDL[t_name] not in RDL['M*']:
                ANS.append("MOV " + getsym.get_pos(RDL[t_name]) + ', ' + register_list[t_name])
        goto_state.append(3)
        if len(if_stack) > 0:
            delay_stack.append(if_stack.pop())
        return True  # 这个true  就返回的很有灵性，需要好好仔细研究一下
    elif tetrad[0] == 'wh':
        switch_wh = 1
    elif tetrad[0] == 'do':
        do_stack1.append(len(ANS) - 1)
        return True
    elif tetrad[0] == 'we':
        for jk in RDL.keys():
            if jk != "M*" and RDL[jk] != 'null':
                if seg5[RDL[jk]] != 'n' and seg5[RDL[jk]] != 0 and RDL[jk] not in RDL['M*']:
                    ANS.append("MOV " + getsym.get_pos(RDL[jk]) + ', ' + register_list[jk])
                    RDL['M*'].append(RDL[jk])
                    RDL[jk] = 'null'
                elif seg5[RDL[jk]] == 'n':
                    RDL[jk] = 'null'
        # while  end  部分生成JMP部分
        print(while_stack)
        print(ANS)
        cat = while_stack.pop()
        if type(cat) == str:
            ANS.append("JMP " + cat)
            order_quantity = order_quantity + 1
        else:
            print(cat)
            print(ANS[len(ANS) - 1])
            print(tetrad)
            print(while_stack)

            # print(len(while_stack))
            sys.exit(-1)
        '''
        if len(goto_state1) > 0:
            h1 = goto_state1.popleft()
            if h1 == 3:
                new_name = 's' + str(len(f_count)) + 'f'
                f_count.append(new_name)
                ANS[len(ANS) - order_quantity] = new_name + ": " + ANS[len(ANS) - order_quantity]
                mmp = while_stack.popleft()
                ANS[mmp] = ANS[mmp] + new_name

        '''
        if len(do_stack1) > 0:
            do_stack2.append(do_stack1.pop())
        return False
    elif tetrad[0] not in four_head and type(tetrad[3]) == str \
            and tetrad[3] not in function_data_type:
        ANS.append("CALL " + tetrad[0])
        print(tetrad)
        m_name = getsym.find_re(tetrad[0])
        h_name = getsym.get_pos(tetrad[3])
        ANS.append("MOV " + 'AX, ' + m_name)
        ANS.append("MOV " + h_name + ", AX")
        RDL['M*'].append(tetrad[3])
        print(RDL)
        order_quantity = order_quantity + 2
    elif tetrad[0] not in four_head and tetrad[0] != 'main' and tetrad[0] != ' ' and type(tetrad[3]) == str \
            and tetrad[3] in function_data_type:
        print(tetrad)
        ANS.append(tetrad[0] + '  PROC NEAR')
        function_name.append(tetrad[0])
        function_name1 = tetrad[0]
        order_quantity = order_quantity + 1
    elif tetrad[0] == 'begin':
        if_main.append(0)
        return True
    elif tetrad[0] == 'begin_t':
        start = 1
        ANS.append("assume  cs:code")
        ANS.append("code    segment")
        ANS.append("MOV  AX,  123BH")
        ANS.append("MOV  DS,   AX")
        ANS.append("MOV  AX,  1000H")
        ANS.append("MOV  SS,  AX")
        ANS.append("MOV  SP,  0010H")
        if_main.append(1)
    elif tetrad[0] == 'end':
        ip = if_main.pop()
        if ip == 0:
            name = function_name.pop()
            ANS.append("ret")
            order_quantity = order_quantity + 2
        else:
            ANS.append("MOV AX, 4C00H")
            ANS.append("INT 21H")
            ANS.append("code ends")
            ANS.append("end ")
            order_quantity = order_quantity + 4
        if len(goto_state) > 1:
            num_second = goto_state.pop()
            num_first = goto_state.pop()
            if len(delay_stack) > 0 and order_quantity > 0:
                if num_second == 2:
                    goto_state.append(num_second)
                mark1 = 's' + str(len(f_count)) + 'f'
                f_count.append(mark1)
                ANS[len(ANS) - order_quantity] = mark1 + ': ' + ANS[len(ANS) - order_quantity]
                for k_name in delay_stack:
                    ANS[k_name] = ANS[k_name] + mark1
                delay_stack.clear()
                if_stack.clear()
            else:
                # print(tetrad)
                goto_state.append(num_first)
                goto_state.append(num_second)
                # print(goto_state)
        # while 回填创建标号部分
        if len(do_stack2) > 0 and order_quantity > 0:
            if re.match(r'^s[0-9]+f', ANS[len(ANS) - order_quantity]):
                for ice in range(0, len(ANS[len(ANS) - order_quantity]) - 1):
                    if ANS[len(ANS) - order_quantity][ice] != ':':
                        ice = ice + 1
                    else:
                        break
                new_name = ANS[len(ANS) - order_quantity][0:ice]
            else:
                new_name = 's' + str(len(f_count)) + 'f'
                f_count.append(new_name)
                ANS[len(ANS) - order_quantity] = new_name + ": " + ANS[len(ANS) - order_quantity]
            for mmp in do_stack2:
                ANS[mmp] = ANS[mmp] + new_name
            do_stack2.clear()
            do_stack1.clear()
        elif switch_wh == 1:
            '''
            new_name = 's' + str(len(f_count)) + 'f'
            f_count.append(new_name)
            ANS[len(ANS) - order_quantity] = new_name + ": " + ANS[len(ANS) - order_quantity]
            '''
            if re.match(r'^s[0-9]+f', ANS[len(ANS) - order_quantity]):
                for ice in range(0, len(ANS[len(ANS) - order_quantity]) - 1):
                    if ANS[len(ANS) - order_quantity][ice] != ':':
                        ice = ice + 1
                    else:
                        break
                new_name = ANS[len(ANS) - order_quantity][0:ice]
            else:
                new_name = 's' + str(len(f_count)) + 'f'
                f_count.append(new_name)
                ANS[len(ANS) - order_quantity] = new_name + ": " + ANS[len(ANS) - order_quantity]
            while_stack.append(new_name)
            switch_wh = 0

        return False
    elif tetrad[0] == "return":
        h_name = getsym.find_re(function_name1)
        if type(tetrad[3]) == int:
            i_num = tetrad[3]
            i_num = num_change(str(hex(i_num))) + 'H'
            ANS.append("MOV " + h_name + ', ' + i_num)
        else:
            s_time = getsym.get_pos(tetrad[3])
            ANS.append("MOV AX," + s_time)
            ANS.append("MOV " + h_name + ', ' + "AX")
            order_quantity = order_quantity + 1
        return True
    elif tetrad[0] == ' ' and tetrad[3] in data_type:
        RDL['M*'].append(tetrad[1])
    elif tetrad[0] == "main":
        return False
    elif tetrad[0] in operator2:
        address = getR(tetrad, R_add, B_add, C_add)
        if address[0] != address[1]:
            if not address[1].isdigit():
                h_name = getsym.get_pos(address[1])
                ANS.append("MOV " + register_list[address[0]] + ", " + h_name)
            else:
                h_name = num_change(hex(int(address[1]))) + "H"
                ANS.append("MOV " + register_list[address[0]] + ", " + h_name)
            order_quantity = order_quantity + 1
        '''
        op = operator1[tetrad[0]]
        if op == "MUL" or op == "DIV":
            ANS.append("MOV AX," + register_list[address[0]])
            if not address[2].isdigit():
                h_name = getsym.get_pos(address[2])
                ANS.append(op + " " + h_name)
            else:
                h_name = num_change(hex(int(address[2]))) + "H"
                ANS.append(op + ' ' + h_name)
            order_quantity = order_quantity + 2
        else:
        '''
        h_name = address[2]
        if not h_name.isdigit():
            # sys.exit(0)
            h_name = getsym.get_pos(h_name)
        else:
            h_name = num_change(hex(int(h_name))) + "H"
        ANS.append('CMP ' + register_list[address[0]] + ', ' + h_name)
        ANS.append(operator3[tetrad[0]] + ' ')
        order_quantity = order_quantity + 2
        mm = list(tetrad[3].keys())
        if mm[0] in RDL['M*']:
            RDL['M*'].remove(mm[0])
        for j in RDL:
            if j != 'M*' and RDL[j] == mm[0]:
                RDL[j] = 'null'
        RDL[address[0]] = mm[0]
    else:
        print("未设计")
        print(tetrad)
        sys.exit(0)

    # 开始进行if--返填动作
    if len(goto_state) > 1:
        if order_quantity == 0 and tetrad[0] != 'if':
            print(tetrad)
            print(RDL)
            print(seg5)
            print(ANS[len(ANS) - 1])
        num_second = goto_state.pop()
        num_first = goto_state.pop()
        if len(delay_stack) > 0 and order_quantity > 0:
            if num_second == 2:
                goto_state.append(num_second)
            mark = 's' + str(len(f_count)) + 'f'
            f_count.append(mark)
            ANS[len(ANS) - order_quantity] = mark + ': ' + ANS[len(ANS) - order_quantity]
            for k_name in delay_stack:
                ANS[k_name] = ANS[k_name] + mark
            delay_stack.clear()
        else:
            print(tetrad)
            print("abc")
            goto_state.append(num_first)
            goto_state.append(num_second)
            print(goto_state)
        # while 回填创建标号部分

    if len(do_stack2) > 0 and order_quantity > 0:
        print(re.match(r'^s[0-9]+f', ANS[len(ANS) - order_quantity]))
        if re.match(r'^s[0-9]+f', ANS[len(ANS) - order_quantity]):
            for ice in range(0, len(ANS[len(ANS) - order_quantity]) - 1):
                if ANS[len(ANS) - order_quantity][ice] != ':':
                    ice = ice + 1
                else:
                    break
            new_name = ANS[len(ANS) - order_quantity][0:ice]
        else:
            new_name = 's' + str(len(f_count)) + 'f'
            f_count.append(new_name)
            ANS[len(ANS) - order_quantity] = new_name + ": " + ANS[len(ANS) - order_quantity]
        for mmp in do_stack2:
            ANS[mmp] = ANS[mmp] + new_name
        do_stack2.clear()
    elif switch_wh == 1 and order_quantity > 0:

        '''new_name = 's' + str(len(f_count)) + 'f'
        f_count.append(new_name)
        ANS[len(ANS) - order_quantity] = new_name + ": " + ANS[len(ANS) - order_quantity]
        '''
        if re.match(r'^s[0-9]+f', ANS[len(ANS) - order_quantity]):
            for ice in range(0, len(ANS[len(ANS) - order_quantity]) - 1):
                if ANS[len(ANS) - order_quantity][ice] != ':':
                    ice = ice + 1
                else:
                    break
            new_name = ANS[len(ANS) - order_quantity][0:ice]
        else:
            new_name = 's' + str(len(f_count)) + 'f'
            f_count.append(new_name)
            ANS[len(ANS) - order_quantity] = new_name + ": " + ANS[len(ANS) - order_quantity]
        while_stack.append(new_name)
        switch_wh = 0
    '''
    if start == 1 and tetrad[0] != 'begin_t' and order_quantity != 0:
        print(tetrad)
        ANS[len(ANS)-order_quantity] = "start: "+ANS[len(ANS)-order_quantity]
        start = 0
    '''
    order_quantity = 0

    return True


# 处理每个基本快内


def final(team):
    h_state = False
    for boy in range(0, len(team)):
        if boy == len(team) - 1:
            h_state = mak_assemble(team[boy])
        else:
            mak_assemble(team[boy])
    if h_state:
        for jk in RDL.keys():
            if jk != "M*" and RDL[jk] != 'null':
                if seg5[RDL[jk]] != 'n' and seg5[RDL[jk]] != 0 and RDL[jk] not in RDL['M*']:
                    ANS.append("MOV " + getsym.get_pos(RDL[jk]) + ', ' + register_list[jk])
                    RDL['M*'].append(RDL[jk])
                    RDL[jk] = 'null'
                elif seg5[RDL[jk]] == 'n':
                    RDL[jk] = 'null'
    '''
    for ppp in RDL['M*']:
        if re.match(r'^[0-9]+t$', ppp):
            RDL['M*'].remove(ppp)
'''


# 数字转换函数


def num_change(number):
    number = number[2:]
    if len(number) > 2:
        print("数据越界，无法计算")
        print(number)
        sys.exit(0)
    if not number[0].isdigit() or len(number) < 2:
        number = '0' + number

    return number


'''
for i in range(5, 8):
    n = get_names(QT[i])
    print(n)
    m = is_active_plus(n, QT[i])
    print(QT[i])
    final(QT[i])

for i in ANS:
    print(i)
'''

for h in QT:
    n = get_names(h)
    m = is_active_plus(n, h)
    final(h)
print(QT)

with open("code.asm", mode='w+') as file:
    for i in ANS:
        file.write(i + '\n')
