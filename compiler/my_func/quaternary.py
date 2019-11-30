from lexer import Lexer
from grammar import LL1
class Quaternary:
    def __init__(self,l,d):
        self.input_token=l #原始输入token串
        self.dic = d    #token序列对应表
        self.priority_relation={'+':1,'-':1,'*':0,'/':0,'(':2}
        self.suffix_list=self.getSuffixList() #后缀表达式
        self.quaternary=self.getQuaternary() #四元式 [[_,_,_,_],[_,_,_,_]...]

    def getSuffixList(self):
        demos=self.input_token
        res_token=[]
        char_stack_token=[]
        while demos:
            item=demos.pop(0)
            if item[0] == 'i' or item[0] == 'con':
                res_token.append(item)
            elif item[0]=='p':
                x=self.dic[item[0]][item[1]-1]
                if (not char_stack_token) or x == '(':
                    char_stack_token.append(item)
                elif x!=')':
                    while char_stack_token and self.priority_relation[x]>=self.priority_relation[self.dic[char_stack_token[-1][0]][char_stack_token[-1][1]-1]]:
                        res_token.append(char_stack_token.pop(-1))
                    char_stack_token.append(item)
                elif x==')':
                    while self.dic[char_stack_token[-1][0]][char_stack_token[-1][1]-1]!='(':
                        res_token.append(char_stack_token.pop(-1))
                    char_stack_token.pop(-1)
        while char_stack_token:
            res_token.append(char_stack_token.pop(-1))
        return res_token

    def getQuaternary(self):
        qua=self.suffix_list
        tmp_stack=[]
        final=[]
        i=1
        while qua:
            item=qua.pop(0)
            if item[0]=='i' or item[0]=='con':
                tmp_stack.append(item)
            else:
                x2=tmp_stack.pop(-1)
                x1=tmp_stack.pop(-1)
                if x1[0]!='t':
                    x1=self.dic[x1[0]][x1[1]-1]
                if x2[0]!='t':
                    x2=self.dic[x2[0]][x2[1]-1]
                t='t'+str(i)
                tmp_stack.append(t)
                i+=1
                final.append([
                    self.dic[item[0]][item[1]-1],
                    x1,
                    x2,
                    t,
                ])
        return final

class Qua:
    def __init__(self,a,l,d,p):
        self.analyze_table=a    #{}
        self.P_LIST=p
        self.input_token=l
        self.dic=d
        self.SEM=[]
        self.QT=[]
        self.i=1


    def get_char(self,item):
        x2=self.SEM.pop(-1)
        x1=self.SEM.pop(-1)
        self.QT.append([item[1],x1,x2,'t'+str(self.i)])
        self.SEM.append('t'+str(self.i))
        self.i+=1

    def analyzeInput(self):
        SYN=['#','E']
        demo=self.input_token
        w = demo.pop(0)
        while SYN:
            x=SYN.pop(-1)
            w_i=self.dic[w[0]][w[1]-1]
            if x[0]=='f':
                self.get_char(x)
                continue
            if w_i!=x:
                if w[0]=='i' or w[0]=='con':
                    w_x='I'
                else: w_x=w_i
                id=self.analyze_table[x][w_x]
                tmp=self.P_LIST[id]
                if tmp[1]!='$':
                    tmp1=list(tmp[1]).reverse()
                    if w[0]=='p' and w_i!='(' and w_i!=')':
                        if [tmp1[-1],w_i] in self.P_LIST:
                            tmp.insert(-2,'f'+w_i)
                    SYN += tmp
            else:
                if w[0]=='i' or w[0]=='con':
                    self.SEM.append(w_i)

#
# if __name__=='__main__':
#     src=input('input:')
#     lex=Lexer()
#     lex.get_input_str([src])
#     res=lex.analyse(False)
#     path = "D:\CSE\jetbrains\pycharm\webforcomplier\compiler\my_func\grammar_static\grammar.txt"
#     ll1=LL1(path)
#     ll1.initAnalysisTable()
#     qua=Qua(ll1.analysis_table,res,lex.dic,ll1.P_LIST)
#     qua.analyzeInput()
#     print(qua.QT)
#
#
#
#
















