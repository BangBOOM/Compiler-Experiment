class GrammarParser:
    def __init__(self):
        self.GRAMMAR={} #{A:xxx} 字典形式存放文法
        self.VN=set()
        self.VT=set()
        self.Z='E'
        self.P_LIST=[]  #文法规则
        self.FIRST=[]   #first集合
        self.FOLLOW={}  #{A:{a|..Aa...}}
        self.SELECT = []
        self.FIRDIC = {}  # {A:{a|A->a.....}}

    def initGrammar(self,path):
        with open(path, 'r', encoding='utf-8') as f:
            GRAMMAR = [l.strip('\n').split('->') for l in f.readlines()]
        VN = set()
        VT = set()
        for i in GRAMMAR:
            VN.add(i[0])
        for i in GRAMMAR:
            for x in i[1]:
                if x not in VN:
                    VT.add(x)
        for item in GRAMMAR:
            self.P_LIST.append(item)
            if item[0] not in self.GRAMMAR.keys():
                self.GRAMMAR[item[0]] = [item[1]]
            else:
                self.GRAMMAR[item[0]].append(item[1])
        self.VN |= VN
        self.VT |= VT
        self.calFirst()
        self.calFollow()
        self.calSelect()


    def calFirst(self):
        for item in self.P_LIST:
            if item[1] == '$':
                self.FIRST.append(set([]))
                continue
            if item[1][0] in self.VT:
                self.FIRST.append(set([item[1][0]]))
                continue
            demo = self._getFir(item)
            self.FIRST.append(set(list(demo)))

        for item in zip(self.P_LIST, self.FIRST):
            if item[0][0] not in self.FIRDIC.keys():
                self.FIRDIC[item[0][0]] = item[1]
            else:
                self.FIRDIC[item[0][0]] = self.FIRDIC[item[0][0]] | item[1]

    def _getFir(self, item):
        res = ''
        if item[1] == '$':
            pass
        elif item[1][0] in self.VT:
            return res + item[1][0]
        elif item[1][0] in self.VN:
            for i in self._getFirByVN(item[1][0]):
                res += self._getFir(i)
            return res

    def _getFirByVN(self, l):
        return [[l, x] for x in self.GRAMMAR[l]]

    def calFollow(self):
        for item in self.VN:
            res = self._getFollow(item)
            self.FOLLOW[item] = res

    def _getFollow(self, l):
        final = set()
        for item in self.P_LIST:
            if l in item[1]:
                tmp = set()
                is_end = False
                for i in range(item[1].index(l) + 1, len(item[1])):
                    demo = item[1][i]
                    if demo in self.VT:
                        tmp.add(demo)
                        break
                    if demo in self.VN:
                        res = self.FIRDIC[demo]
                        if len(res) != 0:
                            tmp |= res
                            is_end='$' in self.GRAMMAR[demo] and i==len(item[1])-1
                            if '$' not in self.GRAMMAR[demo]:
                                break

                if (len(tmp) == 0 and l != item[0]) | is_end:
                    if item[0] in self.FOLLOW.keys():
                        tmp |= self.FOLLOW[item[0]]
                    else:
                        tmp |= self._getFollow(item[0])
                    tmp.add('#')
                final |= tmp
        return final
    def calSelect(self):
        for item in zip(self.P_LIST, self.FIRST):
            if len(item[1]) != 0:
                self.SELECT.append(item[1])
            elif len(item[1]) == 0:
                self.SELECT.append(self.FOLLOW[item[0][0]])


class LL1(GrammarParser):
    def __init__(self, path):
        GrammarParser.__init__(self)
        self.analysis_table = {}
        self.initGrammar(path)

    def initAnalysisTable(self):
        for vn in self.VN:
            self.analysis_table[vn] = {}
            for vt in self.VT:
                self.analysis_table[vn].update({vt: -1})
            self.analysis_table[vn].update({'#': -1})
        for i, item in enumerate(self.P_LIST):
            for x in self.SELECT[i]:
                self.analysis_table[item[0]][x] = i

    def analyzeInputString(self,l_in=None):
        analyze_stack = ['#', self.Z]
        str_list=[]
        if not l_in:
            str_list = ['I', '+', '(', 'I', '-', 'I', '#']
            print("hello")
        else:
            str_list=l_in
        w = str_list.pop(0)
        while analyze_stack:
            x = analyze_stack.pop()
            if x != w:
                if x not in self.VN:
                    return "error1"
                id = self.analysis_table[x][w]
                if id == -1:
                    return "error2"
                tmp = self.P_LIST[id][1]
                if tmp != '$':
                    tmp = list(tmp)
                    tmp.reverse()
                    analyze_stack += tmp
            else:
                if w == '#':
                    return "acc"
                w = str_list.pop(0)
        return "error3"

# if __name__ == "__main__":
#     path='grammar_static/grammar.txt'
#     ll_1=LL1(path)
#     ll_1.initAnalysisTable()
#     print(ll_1.analyzeInputString())