
k_word={'int':1,'void':2}
p_word={'{':1,'}':2,'(':3,')':4,'[':5,']':6,'=':7,'<':8,'>':9,'<=':10,'>=':11,'!=':12,'==':13,'+':14,'-':15,'*':16,'/':17,';':18,',':19}
i_word={}
c_word={}
s_word={}
ch_word={}
numk=2
numi=0
numch=0
numc=0
nums=0
nump=19
fo=open('output.txt','w')
def addtoi_word(s):#添加至标识符
    global numi
    if len(s)==0:
        return
    elif (not(s in k_word)):
        if(not(s in i_word)):
            numi=numi+1
            i_word[s]=numi
        fo.write('<I,%d>\n' %i_word[s])
    else:
        fo.write('<K,%d>\n' %k_word[s])

def addtos_word(s):               #添加至字符串
    global nums
    if (not(s in s_word)):
        nums=nums+1
        s_word[s]=nums
    fo.write('<S,%d>\n' %s_word[s])

def todo(): #整活
    global numi
    global nums
    global nump
    global numk
    global numc
    global numch
    f=open('input.txt')
    
    lines=f.readlines()
    for line in lines:
        lens=len(line)
        
        state=0               #标识符
        strs=''               #存放字符串
        strp=''               #存放界符
        strc=''               #存放常数
        statech=0
        for i in range(0,lens):
            if(line[i]=='\"' and state==0):  #字符串开始
                state=1
                continue
            elif (state==1 and line[i]=='\"'):  #字符串结束
                addtos_word(strs)
                strs=''
            if (state==1 and line[i]!='\"'):
                strs=strs+line[i]
                continue
            if(line[i]=='\'' and statech==0):       #字符
                statech=1
                continue
            elif(statech==1 and line[i]!='\''):
                if(not(line[i] in ch_word)):
                    numch=numch+1
                    ch_word[line[i]]=numch
                fo.write('<CH,%d>\n' %ch_word[line[i]])
                continue
            elif(statech==1 and line[i]=='\''):
                statech=0
                continue

            if(line[i]=='/' and line[i+1]=='/'):       #注释
                break
            if(line[i]>='0' and line[i]<='9'):           #判断数字
                addtoi_word(strs)
                strs=''
                strc=strc+line[i]
                i=i+1
                statec=0              #小数点标识符
                while(i<len(line) and ((line[i]<='9' and line[i]>='0') or line[i]=='.') ):
                    if(line[i]=='.' and statec==0):
                        statec=1
                        strc=strc+line[i]
                        i=i+1
                        continue
                    elif(line[i]<='9' and line[i]>='0'):
                        strc=strc+line[i]
                    elif(line[i]=='.'and statec==1):
                        break
                    i=i+1
                i=i-1
                addtoi_word(strs)
                if(not(strc in c_word)):
                    numc=numc+1
                    c_word[strc]=numc
                fo.write('<C,%d>\n' %c_word[strc])
                #strn=''
                continue
            stn=''
            stn=stn+line[i]
            if(stn in p_word):
                addtoi_word(strs)
                strs=''
                strp=strp+line[i]
                if(line[i]=='>'or line[i]=='<'or line[i]=='!'or line[i]=='='):
                    if(line[i+1]=='='):
                        i=i+1
                        strp=strp+line[i]
                fo.write('<P,%d>\n' %p_word[strp])
                continue
            if(line[i]==' '):
                addtoi_word(strs)
                strs=''
            if(line[i]!=' '):
                strs=strs+line[i]
    addtoi_word(strs)
    f.close()

todo()
fo.close()
print(k_word)
print(i_word)
print(p_word)
print(s_word)
print(c_word)
print(ch_word)


            
            




                
                
                
            
