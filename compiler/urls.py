from django.urls import path,re_path
from compiler import views

app_name="compiler"

urlpatterns=[
    # path('',views.compiler,name="compiler"),
    path('lexer',views.index,name='lexer'),
    path('lexer_json',views.getJson,name='lexer_json'),
]