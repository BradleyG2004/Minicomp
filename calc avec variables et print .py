# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
reserved = {
   'print' : 'PRINT'
   }
tokens = [
    'NUMBER','MINUS',
    'PLUS','TIMES','DIVIDE',
    'LPAREN','RPAREN', 'OR', 'AND', 'SEMI', 'NAME', 'EGAL', 'INF'
    ] + list(reserved.values())

precedence = (
 ('left', 'OR','AND'),
 ('nonassoc', 'EGAL','INF'),
 ('left','PLUS','MINUS'),
 ('left','TIMES','DIVIDE'),
)
# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_OR = r'\|'
t_AND = r'\&'
t_SEMI = r'\;'

t_EGAL = r'\='
t_INF = r'<'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
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

names={}

def p_bloc(p):
    '''bloc : statement SEMI bloc 
    | statement SEMI'''
    
def p_assign(p):
    'statement : NAME EGAL expression'
    names[p[1]]=p[3]
    
    
def p_statement_expr(p):
    'statement : PRINT LPAREN expression RPAREN'
    print('CALC>', p[3])

def p_expression_binop_INF(p):
    'expression : expression INF expression'
    p[0] = p[1] < p[3]
    
def p_expression_binop_AND(p):
    'expression : expression AND expression'
    p[0] = p[1] and p[3]
    
def p_expression_binop_OR(p):
    'expression : expression OR expression'
    p[0] = p[1] or p[3]
    
def p_expression_binop_plus(p):
    'expression : expression PLUS expression'
    p[0] = p[1] + p[3]

def p_expression_binop_plusplus(p):
    'statement : expression PLUS PLUS'
    p[0]=p[1]-p[1]/p[1]

def p_expression_binop_times(p):
    'expression : expression TIMES expression'
    p[0] = p[1] * p[3]

def p_expression_binop_divide_and_minus(p):
    '''expression : expression MINUS expression
				| expression DIVIDE expression'''
    if p[2] == '-': p[0] = p[1] - p[3]
    else : p[0] = p[1] / p[3]	
    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    p[0] = names[p[1]]
    
def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

s = input('calc > ')
yacc.parse(s)

    