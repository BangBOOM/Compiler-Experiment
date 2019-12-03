import os
from lexer_x import Lexer
import copy

class GrammarParser:
    GRAMMAR_DICT = {}
    P_LIST = []
    FIRST = []
    FIRST_VT = {}  # {A:a|A->a...}
    FOLLOW = {}
    VN = set()
    VT = set()
    Z = 'E'
    SELECT = []

    def __init__(self):
        path = os.path.abspath('grammar_static/grammar.txt')
        with open(path, 'r', encoding='utf-8') as f:
            for item in f.readlines():
                vn, tmp = item.strip().split('->')
                self.P_LIST.append((vn, tmp))
                self.GRAMMAR_DICT.setdefault(vn, []).append(tmp)
                self.VN.add(vn)
        for item in self.P_LIST:
            for x in item[1]:
                if x not in self.VN and x != '$':
                    self.VT.add(x)

    def initList(self):
        self.__calFirstvt()
        self.__calFirst()
        self.__calFollow()
        self.__calSelect()


    def __calFirstvt(self):
        def helper(vn):
            fir = self.FIRST_VT.setdefault(vn, set([]))
            if not fir:
                for item in self.GRAMMAR_DICT[vn]:
                    for i in item:
                        if i in self.VT:
                            fir.add(i)
                        elif i in self.VN:
                            fir.update(helper(i))
                            if '$' in self.GRAMMAR_DICT[i]:
                                continue
                        break
            return fir

        for vn in self.VN:
            helper(vn)

    def __calFirst(self):
        for _, item in self.P_LIST:
            demo = set([])
            for i in item:
                if i in self.VT:
                    demo.add(i)
                elif i in self.VN:
                    demo.update(self.FIRST_VT[i])
                    if '$' in self.GRAMMAR_DICT[i]:
                        continue
                break
            self.FIRST.append(demo)

    def __calFollow(self):
        state=dict(zip(list(self.VN),[False]*len(self.VN)))
        def helper(vn):
            if state[vn]==True:
                return
            for x,item in self.P_LIST:
                try:
                    id = item.index(vn)
                    follow = self.FOLLOW.setdefault(vn, set())
                    while True:
                        if id + 1 == len(item):
                            follow.add('#')
                            if x!=item[-1]:
                                helper(x)
                            follow.update(self.FOLLOW[x])
                        elif item[id + 1] in self.VT:
                            follow.add(item[id + 1])
                        elif item[id + 1] in self.VN:
                            follow.update(self.FIRST_VT[item[id + 1]])
                            if '$' in self.GRAMMAR_DICT[item[id + 1]]:
                                id += 1
                                continue
                        break
                except:
                    pass
            state[vn]=True
        for vn in self.VN:
            helper(vn)

    def __calSelect(self):
        for p,f in zip(self.P_LIST,self.FIRST):
            if f:
                self.SELECT.append(f)
            else:
                self.SELECT.append(self.FOLLOW[p[0]])





class LL1(GrammarParser):
    analysis_table={}
    INPUT_L=[]
    RES_TOKEN=[]
    def __init__(self):
        GrammarParser.__init__(self)
        self.initList()
        self.initAnalysisTable()
        self.lex=Lexer()

    def initAnalysisTable(self):
        for vn in self.VN:
            self.analysis_table[vn]=dict([(vt,-1) for vt in self.VT]+[('#',-1)])
        for i,item in enumerate(self.P_LIST):
            for x in self.SELECT[i]:
                self.analysis_table[item[0]][x]=i

    def getInput(self,INPUT):  # ['12-a+b']
        self.lex.getInput(INPUT)
        self.RES_TOKEN=self.lex.analyse()
        self.lex.dict_for_search()
        for item in self.RES_TOKEN:
            if item[0] == 'p':
                self.INPUT_L.append(list(self.lex.DICT['p'])[item[1]])
            else:
                self.INPUT_L.append('I')
        self.INPUT_L.append('#')

    def autoSetINPUT_L(self,tmp):
        '''
        you can set INPUT_L by your function
        :param tmp:
        :return:
        '''
        pass

    def analyzeInputString(self):
        stack=['#',self.Z]
        strList=copy.copy(self.INPUT_L)
        w=strList.pop(0)
        while stack:
            x=stack.pop()
            if x!=w:
                if x not in self.VN:
                    return "error1"
                id=self.analysis_table[x][w]
                if id==-1:
                    return "error2"
                tmp=self.P_LIST[id][1]
                if tmp!='$':
                    tmp=list(tmp)
                    stack+=tmp[::-1]
            else:
                if w=='#':
                    return "acc"
                w=strList.pop(0)
        return "error3"


if __name__ == "__main__":
    ll1=LL1()
    INPUT=input("input:").split('\n')
    ll1.getInput(INPUT)
    res=ll1.analyzeInputString()
    print(res)
