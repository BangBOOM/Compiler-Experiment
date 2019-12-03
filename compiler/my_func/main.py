from grammar_x import LL1





if __name__=="__main__":
    ll_1=LL1()
    ll_1.getInput(['1+2-b'])
    res=ll_1.analyzeInputString()
    print(res)




