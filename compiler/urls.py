from django.urls import path,re_path
from compiler import views

app_name="compiler"

urlpatterns=[
    # path('',views.compiler,name="compiler"),
    path('compiler',views.index,name='compiler'),
    path('lexer_json',views.getLexerJson,name='lexer_json'),
    path('LL1_json',views.getLL1Json,name='LL1_json'),
]