from grammar_x import LL1
import copy
class Qua(LL1):
    SEM=[]
    QT=[]
    i=0
    def __init__(self):
        LL1.__init__(self)

    def addQT(self,item):
        '''

        :param item:f*,f.,f-,f+
        :return:
        '''
        x2=self.SEM.pop(-1)
        x1=self.SEM.pop(-1)
        self.QT.append([item[1], x1, x2, 't' + str(self.i)])
        self.SEM.append('t' + str(self.i))
        self.i += 1

    def genQua(self):
        SYN=['#','E']
        token=copy.copy(self.RES_TOKEN)
        t, id = token.pop(0)
        w = self.lex.DICT_S[t][id]
        while SYN:
            x=SYN.pop()
            if x[0]=='f':
                self.addQT(x)
                continue
            if t == 'i' or t == 'con':
                w_g = 'I'
            else:
                w_g = w
            if w_g==x:
                if x=='#':
                    break
                if t=='i' or t=='con':
                    self.SEM.append(w)
                if token:
                    t,id=token.pop(0)
                    w=self.lex.DICT_S[t][id]
                else:
                    t='#'
                    w=w_g='#'
            else:
                idx=self.analysis_table[x][w_g]
                _,tmp=self.P_LIST[idx]
                if tmp!='$':
                    tmp1=list(tmp)[::-1]
                    if t=='p' and w!='(' and w!=')':
                        if (tmp1[-1],w) in self.P_LIST:
                            tmp1.insert(-2,'f'+w)
                    SYN+=tmp1

if __name__=="__main__":
    qua=Qua()
    INPUT=input("input:").split('\n')   #sample INPUT=['a+b+c'] must be one line
    qua.getInput(INPUT)
    print(qua.RES_TOKEN)
    if qua.analyzeInputString()=="acc":
        qua.genQua()
        print(qua.QT)
    else:
        print("error")



