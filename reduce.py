import translate
import pickle
translate.main()
Get = translate.Get


a = []


def solve_pro():
    for i in range(0, len(Get)):
        li = [Get[i].op, Get[i].t1, Get[i].t2, Get[i].type]
        a.append(li)


part = []


def divide(a):
    state = 0
    for i in range(0, len(a)):
        for j in range(0, 4):
            if a[i][j] == '':
                a[i][j] = ' '
            # elif a[i][j].replace('.', '', 1).isdigit():
            #     a[i][j] = int(a[i][j])
        if a[i][0] == 'if' or a[i][0] == 'do' or a[i][0] == 'end' or a[i][0] == 'el' or\
                a[i][0] == 'return' or a[i][0] == 'we':
            # print(a[i])
            part.append(a[i])
            # print('divide over')
            part.append('divide over')

        elif a[i][0] == 'ie' or a[i][0] == 'wh':
            # print('divide over')
            part.append('divide over')
            # print(a[i])
            part.append(a[i])
        else:
            # print(a[i])
            part.append(a[i])


final = []


def block_into_list(part):
    block_part = []
    for i in range(0, len(part)):
        if part[i] != 'divide over':
            block_part.append(part[i])
        elif part[i] == 'divide over':
            final.append(block_part)
            block_part = []


def main():
    solve_pro()
    divide(a)
    block_into_list(part)
    print(final)
    f = open('outpro.txt', 'wb')
    pickle.dump(final, f)


if __name__ == '__main__':
    main()






































































