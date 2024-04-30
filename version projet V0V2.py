from genereTreeGraphviz2 import printTreeGraph
import ast
#les reserved sont des tokens natifs du langage
reserved = {
   'while':'WHILE',
   'for':'FOR',
   'if' : 'IF',
   'else' : 'ELSE',
   'print' : 'PRINT',
   'void' : 'VOID'
   }

#Les tokens definissent une sorte d'aphabet , qui sera utilisee dans les regles de grammaire
tokens = [
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE', 
    'LPAREN','RPAREN','LACCO','RACCO','DOTS', 'COLON','GUI', 'AND', 'OR', 'EQUAL', 'EQUALS', 'LOWER','HIGHER'
    ]+list(reserved.values())

# Tokens
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

t_PLUS    = r'\+'
t_DOTS=r':'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUAL  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_GUI = r'\"'
t_LACCO=r'\{'
t_RACCO=r'\}'
t_COLON = r';'
t_AND  = r'\&'
t_OR  = r'\|'
t_EQUALS  = r'=='
t_LOWER  = r'\<'
t_HIGHER  = r'\>'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()



# Parsing rules

def p_start(t):
    ''' start : linst'''
    t[0] = ('start',t[1])
    print(t[0])
    printTreeGraph(t[0])
    #eval(t[1])
    evalInst(t[1])
names={}
tf=[]

def evalInst(t):
    print('evalInst', t)
    if type(t)!=tuple : 
        print('warning')
        return
    if t[0]=='print' :
        print('CALC>', evalExpr(t[1]))
    if t[0]=='assign' : 
        names[t[1]]=evalExpr(t[2])
    if t[0]=='linst' : 
        evalInst(t[1])
        evalInst(t[2])       
    if t[0]=='if':
        if evalExpr(t[1]):
            evalInst(t[2])
    if t[0]=='if_else':
        if evalExpr(t[1]):
            evalInst(t[2])
        else:
            evalInst(t[3])
    if t[0]=='while':
        evalInst(t[1])
        while evalExpr(t[2]):
            evalInst(t[3])
    if t[0]=='for':
        evalInst(t[1])
        while evalExpr(t[2]):
            evalInst(t[4])
            evalInst(t[3])
    if t[0]=='void':
        names[t[1]]=t[2]
    if t[0]=='appel':
        print(t[1])
        evalInst(names[t[1]])
    if t[0]=='voidp':
        names[t[1]]={}
        if(t[2][0]=='lexp'):#cas de plusieurs parametres
            print(t)
            names[t[1]]['param']=[]
            if t[2][1][0]=='lexp':
                evalInst(('tuplecut',t[1],t[2][1],t[2][2]))
                tf.reverse()
                print(tf)
                for elmt in tf:
                    names[t[1]]['param'].append(elmt)
            else:
                names[t[1]]['param'].append(t[2][1][0])
                names[t[1]]['param'].append(t[2][1][1])
                names[t[1]]['param'].append(t[2][2][0])
                names[t[1]]['param'].append(t[2][2][1])
        else:
            names[t[1]]['param']=[]
            names[t[1]]['param'].append(t[2][0])
            names[t[1]]['param'].append(t[2][1])     
        names[t[1]]['inst']=str(t[3])
        print(names[t[1]])
    if t[0]=='tuplecut':
        print("interieur de tuplecut")
        if t[2][0]!='lexp':
            tf.append(t[3][0])
            tf.append(t[3][1])
            tf.append(t[2][0])
            tf.append(t[2][1])
        else:
            tf.append(t[3][0])
            tf.append(t[3][1])
            evalInst(('tuplecut',t[1],t[2][1],t[2][2]))
    if t[0]=='tuplecutt':
        print("interieur de tuplecutt")
        if(type(t[2])!=tuple):
            tf.append(t[3])
            tf.append(t[2])
        else:
            tf.append(t[3])
            evalInst(('tuplecutt',t[1],t[2][1],t[2][2]))
    if t[0]=='appel1': 
        if(type(t[2])!=tuple):
            if(t[2] in names):
                if(type(names[t[2]])==int):
                    if(names[t[1]]['param'][0]=='integer'):
                        names[t[1]]['inst']=names[t[1]]['inst'].replace("'"+names[t[1]]['param'][1]+"'",str(names[t[2]]))
                        print(names[t[1]]['inst'])
                    else:
                        print("Mauvais parametre")
                elif(type(names[t[2]])==float):
                    if(names[t[1]]['param'][0]=='floatt'):
                        names[t[1]]['inst']=names[t[1]]['inst'].replace("'"+names[t[1]]['param'][1]+"'",str(names[t[2]]))
                        print(names[t[1]]['inst'])
                    else:
                        print("Mauvais parametre")
                elif(type(names[t[2]])==str):
                    if(names[t[1]]['param'][0]=='string'):
                        names[t[1]]['inst']=names[t[1]]['inst'].replace("'"+names[t[1]]['param'][1]+"'",str(names[t[2]]))
                        print(names[t[1]]['inst'])
                    else:
                        print("Mauvais parametre")
        else:
            if(type(t[2][1])==tuple):
                 evalInst(('tuplecutt',t[1],t[2][1],t[2][2]))
            else:
                tf.append(t[2][1])
                tf.append(t[2][2])
            if(len(tf)==len(names[t[1]]['param'])/2):
                i=0
                j=i+1
                for elmt in tf:
                    if(elmt in names):
                        if(type(names[elmt])==int):
                            if(names[t[1]]['param'][i]=='integer'):
                                names[t[1]]['inst']=names[t[1]]['inst'].replace("'"+names[t[1]]['param'][j]+"'",str(names[elmt]))
                            else:
                                print("Mauvais parametre")
                        elif(type(names[elmt])==float):
                            if(names[t[1]]['param'][i]=='floatt'):
                                names[t[1]]['inst']=names[t[1]]['inst'].replace("'"+names[t[1]]['param'][j]+"'",str(names[elmt]))
                            else:
                                print("Mauvais parametre")
                        elif(type(names[elmt])==str):
                            if(names[t[1]]['param'][i]=='string'):
                                names[t[1]]['inst']=names[t[1]]['inst'].replace("'"+names[t[1]]['param'][j]+"'",str(names[elmt]))
                            else:
                                print("Mauvais parametre")
                    i=i+2
                    j=j+2
            e=ast.literal_eval(names[t[1]]['inst'])
            evalInst(e)
    
                





        

    

        





def evalExpr(t):
    # print('evalExpr', t)
    if type(t)!=tuple :
        if(type(t)==int):
            return int(t)
        elif(type(t)==float):
            return float(t)
        elif(type(t)==str):
            if t in names:
                return names[t]
            else:
                # names[t]=t
                return t
    if type(t)==tuple :
        if(t[0]=='lexp'):
            tab=[evalExpr(t[1]),evalExpr(t[2])]
            return tab
        if(t[0]=='*'):
            return evalExpr(t[1])*evalExpr(t[2])
        elif(t[0]=='/'):
            return evalExpr(t[1])/evalExpr(t[2])
        elif(t[0]=='-'):
            return evalExpr(t[1])-evalExpr(t[2])
        elif(t[0]=='+'):
            return evalExpr(t[1])+evalExpr(t[2])
        elif(t[0]=='>'):
            return evalExpr(t[1])>evalExpr(t[2])
        elif(t[0]=='<'):
            return evalExpr(t[1])<evalExpr(t[2])
        elif(t[0]=='>='):
            return evalExpr(t[1])>=evalExpr(t[2])
        elif(t[0]=='<='):
            return evalExpr(t[1])<=evalExpr(t[2])
        elif(t[0]=='=='):
            return evalExpr(t[1])==evalExpr(t[2])
        elif(t[0]=='!='):
            return evalExpr(t[1])!=evalExpr(t[2])  
    else:
        return



def p_line(t):
    '''linst : linst inst 
            | inst '''
    if len(t)== 3 :
        t[0] = ('linst',t[1], t[2])
    else:
        t[0] = ('linst',t[1], 'empty')
    
    

def p_statement_assign(t):
    'inst : NAME EQUAL expression COLON'
    t[0] = ('assign',t[1], t[3])

def p_statement_print(t):
    '''inst : PRINT LPAREN expression RPAREN COLON
            | PRINT LPAREN lexp RPAREN COLON'''
    t[0] = ('print',t[3])

def p_statement_if(t):
    'inst : IF LPAREN expression RPAREN LACCO linst RACCO'
    t[0]=('if',t[3],t[6]) 

def p_statement_if_else(t):
    'inst : IF LPAREN expression RPAREN LACCO linst RACCO ELSE LACCO linst RACCO '
    t[0]=('if_else',t[3],t[6],t[10])

def p_statement_while(t):
    'inst : inst WHILE LPAREN expression RPAREN LACCO linst RACCO'
    t[0]=('while',t[1],t[4],t[7])

def p_statement_for(t):
    'inst : FOR LPAREN inst expression COLON inst RPAREN LACCO linst RACCO'
    t[0]=('for',t[3],t[4],t[6],t[9])

def p_function_void(t):
    '''inst : VOID NAME LPAREN RPAREN LACCO linst RACCO COLON
            | VOID NAME LPAREN expression RPAREN LACCO linst RACCO COLON
            | VOID NAME LPAREN lexp RPAREN LACCO linst RACCO COLON'''
    if len(t)==9:
        t[0]=('void',t[2],t[6])
    else:
        t[0]=('voidp',t[2],t[4],t[7])

def p_appel(t):
    '''inst : NAME LPAREN RPAREN COLON
            | NAME LPAREN expression RPAREN COLON
            | NAME LPAREN lexp RPAREN COLON'''
    if len(t)==5:
        t[0]=('appel',t[1])
    else:
        t[0]=('appel1',t[1],t[3])
   
def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression PLUS PLUS
                  | expression DOTS expression
                  | expression TIMES TIMES expression
                  | expression PLUS EQUAL expression
                  | expression MINUS expression
                  | expression MINUS MINUS
                  | expression MINUS EQUAL expression
                  | expression TIMES expression
                  | expression TIMES EQUAL expression
                  | expression OR expression
                  | expression AND expression
                  | expression EQUALS expression
                  | expression LOWER expression
                  | expression HIGHER expression
                  | expression DIVIDE expression
                  | expression DIVIDE EQUAL expression'''
    if len(t) == 4:
        if t[2] == '+' and t[3]=='+':
            t[0] = (t[2], t[1], 1)
        elif t[2] == '-' and t[3]=='-':
            t[0] = (t[2], t[1], 1)
        elif t[2] == ':':
            t[0] =   (t[1], t[3],"empty")
        else:
            t[0] = (t[2], t[1], t[3])
    elif len(t) == 5:
        if t[2] == '+':
           t[0] = (t[2], t[1], t[4]) 
        if t[2] == '-':
            t[0] = (t[2], t[1], t[4])
        if t[2] == '*':
            t[0] = (t[2], t[1], t[4])
        if t[2] == '/':
            t[0] = (t[2], t[1], t[4])
    
 
def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    '''expression : NUMBER
                  | GUI NUMBER GUI'''
    
    if len(t)==2:
        t[0] = int(t[1])
    else:
        t[0]=int(t[2])

def p_expression_name(t):
    '''expression : NAME
                  | GUI NAME GUI'''
    if len(t)==2:
        t[0] = t[1]
    else:
        t[0]=t[2]

def p_lexpression(t):
    '''lexp : expression COLON expression
            | lexp COLON expression'''
    
    t[0]=('lexp',t[1],t[3])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

# s='1+2;x=4 if ;x=x+1;'
# s='print(17*2);x=4;x=3+1;'

#1,2a,2b-s='aaa=3;print(aaa+1);'
#2c-s='if(1>2){print(911);}else{print(922);}'
#2d-s='for(i=0;i<3;i=i+1;){print(i);}'
#2d-s='inn=1;while(inn<5){print(inn);inn=inn+1;}'
# s='a=2;b=3;print("toto";"Mumble";a++;b+=7);'
# s='print("toto";10);'
# s='void molten(){a=2;print(a++);};molten();'
s='void Testtt(integer:a;integer:b){print(a-b);};f=10;v=2;Testtt(f;v);'



#with open("1.in") as file: # Use file to refer to the file object

   #s = file.read()
   
parser.parse(s)

