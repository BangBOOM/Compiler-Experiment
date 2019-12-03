# 编译原理实验

##简介
+ 将三次实验做成了一个网站用于展示后端提供数据，前端只做数据的渲染不对数据进行其他处理
+ 框架后端：django 前端：bootstrap+jquery
+ download项目在根目录输入`python manage.py runserver` 即可启动项目，几个绝对路径需要改

## 主要组成
+ 关于框架就不赘述了，主要说一下实验的部分，实验代码在 `compiler\my_func` 下面
+ 分别是 `lexer.py` 词法分析 `grammer.py` 语法分析 `quaternary.py` 四元式生成 这三个文件是用于网页的内容处理的，写的比较粗糙
+ 在上面三个文件后面加上了 `_x` 是重写了一遍优化过的可以作为实验参考，每后面一次实验是基于前一次的结果的
+ lexer 部分借鉴了[link](https://github.com/HIT-Alibaba/HIT_Compiler_Experiment) 
+ grammar和quaternary均使用LL1分析法自己按照课本和自己的理解写的

## 总结
+ 第一次尝试将三次实验完全连接起来，感觉自己设计全部结构真的挺难的，代码写的也很冗杂，仅供参考。





