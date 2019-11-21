from django.shortcuts import render
from .function.lexer import lexer
from django.http import JsonResponse


# Create your views here.

class Item:
    def __init__(self, **kwargs):
        self.src = kwargs['src']
        self.tgt = kwargs['tgt']
        self.table = kwargs['table']
        # self.k=kwargs['k']
        # self.p=kwargs['p']
        # self.con=kwargs['con']
        # self.char=kwargs['char']
        # self.str=kwargs['str']
        # self.iden=kwargs['iden']


def make_one_list(lex):
    len = lex.full_list()
    res = []
    for i in range(len):
        demo = [i+1, lex.IDENTIFIER_LIST[i], lex.CHAR_LIST[i], lex.STRING_LIST[i], lex.CONSTANT_LIST[i], lex.K_LIST[i],
                lex.P_LIST[i],
                ]
        res.append(demo)
    return res


def getJson(request):
    src = request.GET['src']
    lex = lexer.Lexer()
    lex.get_input_from_web(src)
    res_list = lex.analyse()
    table_list = make_one_list(lex)
    return JsonResponse({'res': res_list, 'table': table_list}, safe=False)


def index(request):
    return render(request, 'index_jq.html')






# def compiler(request):
#     if request.method == "GET":
#         return render(request, 'index.html')
#     elif request.method == "POST":
#         src = request.POST.get('code')
#         if len(src) != 0:
#             out = {'src': src}
#             src = src.split('\n')
#             lex = lexer.Lexer()
#             lex.get_input_from_web(src)
#             res_list = lex.analyse()
#             table_list = make_one_list(lex)
#             out.update(
#                 {
#                     'tgt': res_list,
#                     'table': table_list,
#                 }
#             )
#             final = Item(**out)
#             return render(request, 'index.html', {'res': final})
#     return render(request, 'index.html')
