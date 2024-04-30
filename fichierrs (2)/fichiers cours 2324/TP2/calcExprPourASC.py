from genereTreeGraphviz2 import printTreeGraph# à copier coller dans le script sinon

tokens = (
    'NUMBER','MINUS',
    'PLUS','TIMES','DIVIDE',
    'LPAREN','RPAREN'
    )

# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
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
lex.lex()

precedence = (
 
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
 
    )
 
   
#on defini ce qu'on considere comme  start   
def p_start(p):
    #ci-dessous on a la regle de grammaire de s(start)
    'start : expression'
    #p[0] renvoie au premier terme de la regle formulee ci-dessus
    p[0] = ('START',p[1])
    print(p[0])
    printTreeGraph(p[0])

#les 3 blocs suivants correspondent aux differentes alternatives pour une expression d'apres l'enonce page 40/48 poly.pdf

#(1) Addition
def p_expression_binop_plus(p):
    'expression : expression PLUS expression'
    
#(2) Multiplication    
def p_expression_binop_times(p):
    'expression : expression TIMES expression'
     
#(3) Left-parenthese and Right-parenthese
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    
#(4) Number
def p_expression_number(p):
    'expression : NUMBER'
     

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

s = '(1+2)*3'
yacc.parse(s)

    