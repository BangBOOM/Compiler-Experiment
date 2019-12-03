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
















