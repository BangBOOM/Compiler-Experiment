from django.shortcuts import render
from .my_func import lexer, grammar,quaternary
from django.http import JsonResponse


# Create your views here.

def make_one_list(lex):
    len = lex.full_list()
    res = []
    for i in range(len):
        demo = [i + 1, lex.IDENTIFIER_LIST[i], lex.CHAR_LIST[i], lex.STRING_LIST[i], lex.CONSTANT_LIST[i],
                lex.K_LIST[i],
                lex.P_LIST[i],
                ]
        res.append(demo)
    return res


def getLexerJson(request):
    src = request.GET['src'].split('\n')
    lex = lexer.Lexer()
    lex.get_input_str(src)
    res_list = lex.analyse()
    table_list = make_one_list(lex)
    return JsonResponse({'res': res_list, 'table': table_list}, safe=False)


def dealSrcFromWeb(src):
    lex = lexer.Lexer()
    lex.get_input_str([src])
    res = lex.analyse(False)
    list_for_grammar = []
    for item in res:
        if item[0] == 'p':
            list_for_grammar.append(lex.dic['p'][item[1] - 1])
        else:
            list_for_grammar.append('I')
    list_for_grammar.append('#')
    return list_for_grammar,lex.dic,res


def getReJson(request):
    '''
    递归子程序
    :param request:
    :return: acc or error
    '''
    src = request.GET['src'].strip()
    list_for_grammar,dic,l = dealSrcFromWeb(src)
    path = "D:\CSE\jetbrains\pycharm\webforcomplier\compiler\my_func\grammar_static\grammar.txt"
    re = grammar.RecursiveSubroutineFunc(path)
    re.INPUT = list_for_grammar
    res = re.analyse()
    qua=[]
    if res=='acc':
        qua=getQuaternaryList(l,dic)
    return JsonResponse({'res': res,'qua':qua}, safe=False)


def getLL1Json(request):
    '''
    LL1分析法
    :param request:
    :return:select table
    '''
    src = request.GET['src'].strip()
    list_for_grammar,dic,l = dealSrcFromWeb(src)
    path = "D:\CSE\jetbrains\pycharm\webforcomplier\compiler\my_func\grammar_static\grammar.txt"
    ll_1 = grammar.LL1(path)
    ll_1.initAnalysisTable()
    select=[list(item) for item in ll_1.SELECT]
    res = ll_1.analyzeInputString(list_for_grammar)
    qua=[]
    if res=='acc':
        qua=getQuaternaryList(l,dic)
    return JsonResponse({'res': res, 'select': select, 'p_list': ll_1.P_LIST,'qua':qua}, safe=False)

def getQuaternaryList(l,d):
    qua=quaternary.Quaternary(l,d)
    return qua.quaternary


def index(request):
    return render(request, 'compiler.html')
