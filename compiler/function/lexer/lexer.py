class Lexer:
    def __init__(self,):
        with open("compiler/function/lexer/keyword_list", 'r', encoding='utf-8') as f:
            self.K_LIST = [item.strip() for item in f.readlines()]
        with open("compiler/function/lexer/p_list", 'r', encoding='utf-8') as f:
            self.P_LIST = [item.strip() for item in f.readlines()]
        self.cur_row=-1
        self.cur_line=0
        self.input_str=[]
        self.CONSTANT_LIST=[]   #常数
        self.IDENTIFIER_LIST=[] #标识符
        self.STRING_LIST=[] #字符串
        self.CHAR_LIST=[]   #字符

    def get_char(self):
        self.cur_row+=1
        if self.cur_row==len(self.input_str[self.cur_line]):
            self.cur_row=0
            self.cur_line+=1
            if self.cur_line == len(self.input_str):
                return "END"
        while self.cur_row>=len(self.input_str[self.cur_line]):
            self.cur_line+=1
            if self.cur_line == len(self.input_str):
                return "END"
        return self.input_str[self.cur_line][self.cur_row]

    def get_input_from_web(self, str_s):
        self.input_str=str_s

    def get_input_str(self):
        filename="c_l"
        with open(filename,'r',encoding='utf-8') as f:
            self.input_str=[l.strip() for l in f.readlines()]

    def back_one(self):
        if self.cur_row>0:
            self.cur_row-=1
        else:
            self.cur_line-=1
            self.cur_row=len(self.input_str[self.cur_line])-1

    def scanner(self):
        item=self.get_char().strip()
        if item=="":
            return None
        if item=="END":
            return "END"

        if item.isalpha() or item=="_":
            demo=""
            while item.isalpha() or item.isdigit() or item=="_":
                demo+=item
                item=self.get_char()
            self.back_one()
            if demo in self.K_LIST:
                return ['k',self.K_LIST.index(demo)+1]
            if demo not in self.IDENTIFIER_LIST:
                self.IDENTIFIER_LIST.append(demo)
            return ['i',self.IDENTIFIER_LIST.index(demo)+1]
        if item.isdigit():
            demo=""
            while item.isdigit() or item==".":
                demo+=item
                item=self.get_char()
            self.back_one()
            demo=eval(demo)
            if demo not in self.CONSTANT_LIST:
                self.CONSTANT_LIST.append(demo)
            return ['con',self.CONSTANT_LIST.index(demo)+1]
        if item=='"':
            demo='"'
            item=self.get_char()
            demo+=item
            while item!='"':
                item=self.get_char()
                if item==";" and self.cur_row==len(self.input_str[self.cur_line])-1:
                    return ["error","missing \"",self.cur_line,self.cur_row]
                demo+=item
            if demo not in self.STRING_LIST:
                self.STRING_LIST.append(demo)
            return ['s',self.STRING_LIST.index(demo)+1]
        if item=="'":
            demo="'"
            item=self.get_char()
            demo+=item
            while item!="'":
                item=self.get_char()
                demo+=item
            if demo not in self.CHAR_LIST:
                self.CHAR_LIST.append(demo)
            return ['c',self.CHAR_LIST.index(demo)+1]
        if item in self.P_LIST:
            return ['p',self.P_LIST.index(item)+1]


    def analyse(self):
        res_list=[]
        while True:
            demo=self.scanner()
            if demo=="END":
                break
            if demo!=None:
                res_list.append(demo)
                if demo[0]=="error":
                    break
        temp=func(res_list,6)
        res_list=[]
        for i in temp:
            res_list.append(i)
        return res_list

    def get_max_len(self):
        return max(len(self.K_LIST),len(self.P_LIST),len(self.CHAR_LIST),len(self.CONSTANT_LIST),len(self.IDENTIFIER_LIST),len(self.STRING_LIST))

    def full_list(self):
        max_len=self.get_max_len()
        if len(self.K_LIST)<max_len:
            self.K_LIST+=['-']*(max_len-len(self.K_LIST))
        if len(self.STRING_LIST)<max_len:
            self.STRING_LIST+=['-']*(max_len-len(self.STRING_LIST))
        if len(self.CONSTANT_LIST)<max_len:
            self.CONSTANT_LIST+=['-']*(max_len-len(self.CONSTANT_LIST))
        if len(self.P_LIST) < max_len:
            self.P_LIST += ['-'] * (max_len - len(self.P_LIST))
        if len(self.IDENTIFIER_LIST)<max_len:
            self.IDENTIFIER_LIST+=['-']*(max_len-len(self.IDENTIFIER_LIST))
        if len(self.CHAR_LIST)<max_len:
            self.CHAR_LIST+=['-']*(max_len-len(self.CHAR_LIST))
        return max_len

def func(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]


def main():
    lex=Lexer()
    lex.get_input_str()
    while True:
        res=lex.scanner()
        if res=="END":
            break
        if res!=None:
            print(res)
            if res[0]=="error":
                break

if __name__ == "__main__":
    main()
