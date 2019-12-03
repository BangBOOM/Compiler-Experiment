import os,collections
class Lexer:
    DICT={
        'k':collections.OrderedDict(),     #关键字
        'p':collections.OrderedDict(),     #界符
        'con':collections.OrderedDict(),   #常数
        'c':collections.OrderedDict(),     #字符
        's':collections.OrderedDict(),     #字符串
        'i':collections.OrderedDict(),     #标识符
    }
    INPUT=[]
    CUR_ROW=-1
    CUR_LINE=0
    def __init__(self):
        path1=os.path.abspath('lexer_static/keyword_list')
        path2=os.path.abspath('lexer_static/p_list')
        with open(path1,'r',encoding='utf-8') as f:
            for i,item in enumerate(f.readlines()):
                item=item.strip()
                self.DICT['k'][item]=i
        with open(path2,'r',encoding='utf-8') as f:
            for i, item in enumerate(f.readlines()):
                item=item.strip()
                self.DICT['p'][item] = i
    def getInput(self,input_list):
        '''
        :param input_list:['...','...'] the string split by '\n'
        :return:
        '''
        self.INPUT=input_list

    def getNextChar(self):
        self.CUR_ROW+=1
        if self.CUR_LINE==len(self.INPUT):
            return "END"
        while self.CUR_ROW==len(self.INPUT[self.CUR_LINE]):
            '''the end of each line or the line is empty'''
            self.CUR_ROW=0
            self.CUR_LINE+=1
            if self.CUR_LINE==len(self.INPUT):
                return "END"
        return self.INPUT[self.CUR_LINE][self.CUR_ROW]

    def backOneStep(self):
        self.CUR_ROW-=1

    def __getId(self,demo,typ):
        return self.DICT[typ].setdefault(demo,len(self.DICT[typ]))


    def scanner(self):
        item=self.getNextChar().strip()
        if item=='':
            return None
        if item=="END":
            return ("END")
        if item.isalpha() or item=='_':
            demo=""
            while item.isalpha() or item.isdigit() or item=="_":
                demo+=item
                if self.CUR_ROW==len(self.INPUT[self.CUR_LINE])-1:
                    self.CUR_LINE+=1
                    self.CUR_ROW=0
                    break
                else:
                    item=self.getNextChar()
            self.backOneStep()
            id=self.DICT['k'].get(demo,-1)
            if id==-1:
                id=self.__getId(demo,'i')
                return ('i',id)
            else:
                return ('k',id)
        if item.isdigit():
            demo=""
            while item.isdigit() or item==".":
                demo+=item
                if self.CUR_ROW==len(self.INPUT[self.CUR_LINE])-1:
                    self.CUR_LINE+=1
                    self.CUR_ROW=0
                    break
                else:
                    item=self.getNextChar()
            self.backOneStep()
            id=self.__getId(demo,'con')
            return ('con',id)
        if item=='"':
            demo='"'
            item=self.getNextChar()
            demo+=item
            while item!='"':
                item=self.getNextChar()
                demo+=item
            id=self.__getId(demo,'s')
            return ('s',id)
        if item=="'":
            demo="'"
            for i in range(2):
                item=self.getNextChar()
                demo+=item
            id=self.__getId(demo,'c')
            return ('c',id)
        id=self.DICT['p'].get(item)
        return ('p',id)

    def analyse(self):
        TOKEN_LIST=[]
        while True:
            tmp=self.scanner()
            if tmp=="END":
                break
            if tmp:
                TOKEN_LIST.append(tmp)
        return TOKEN_LIST



if __name__=="__main__":
    lex=Lexer()
    INPUT=input("input something:").split('\n')
    lex.getInput(INPUT)
    res=lex.analyse()
    print(res)