from grammar import LL1
from lexer import Lexer


if __name__=="__main__":
    lex=Lexer()
    demo=input("make some in put:").split('\n')
    lex.get_input_str(demo)
    res=lex.analyse(False)
    list_for_grammar=[]
    for item in res:
        if item[0]=='p':
            list_for_grammar.append(lex.dic['p'][item[1]-1])
        else:
            list_for_grammar.append('I')
    list_for_grammar.append('#')
    path='grammar_static/grammar.txt'
    ll_1=LL1(path)
    ll_1.initAnalysisTable()
    print(ll_1.analyzeInputString(list_for_grammar))



