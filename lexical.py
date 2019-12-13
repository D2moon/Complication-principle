import word_analyzer
import lexicalpro

Dirt = lexicalpro.dirt
Grammar = lexicalpro.Grammar
Token = word_analyzer.Token
Mapa = lexicalpro.mapa


def main():
    pick = []
    for i in range(0, len(Token)):
        if Token[i].type == 'C':
            pick.append('sz')
        elif Token[i].type == 'P':
            pick.append(Token[i].str)
        elif Token[i].type == 'I':
            pick.append('id')
        elif Token[i].type == 'K':
            pick.append(Token[i].str)
        #       elif Token[i].type == 'CH':
        #       elif Token[i].type == 'S':    字符与字符串之后处理
        else:
            pick.append('#')
    stack = ['#', 'q1']
    i = 0
    flag = True
    while i < len(pick)-1:
        if pick[i] not in Mapa:
            flag = False
            break
        t1 = Mapa[pick[i]]
        ne = Dirt[stack[-1]][t1]

        if not ne:
            #print(pick[i])
            #print(stack[-1])
            print(stack[-1], end=' ')
            print(pick[i])
            flag = False
            break
        stack.pop()
        for j in range(0, len(Grammar[ne])):
            if Grammar[ne][j] == '!':
                break
            stack.append(Grammar[ne][j])
        while i < len(pick)-1 and stack[-1] == pick[i]:
            i += 1
            stack.pop()
    if i != len(pick)-1:
        flag = False
    if not flag:
        print('语法使用错误')
    else:
        print('语法正确')


if __name__ == '__main__':
    main()
