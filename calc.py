import ply.lex as lex
import ply.yacc as yacc
import node
import graph
import evaluator

# Tokens
tokens = (
    'number','plus', 'minus', 'times', 'divide', 'lparen', 'rparen'
)

t_plus = r'\+'
t_minus = r'-'
t_times = r'\*'
t_divide = r'/'
t_lparen = r'\('
t_rparen = r'\)'

def t_number(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(f'Integer value too large: {t.value}')
        t.value = 0
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.couunt('\n')

def t_error(t):
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)

lexer = lex.lex()

# Grammar

# L -> E
# E -> E + T
#   |  E - T
#   | T
# T -> T * F
#   |  T / F
#   | F
# F -> ( E )
#    | number

def p_L_E(t):
    'L : E'
    lnode = node.Node('L', [])
    lnode.add_child(t[1])
    t[0] = lnode

def p_E_EplusT(t):
    'E : E plus T'
    enode = node.Node('E', [])
    enode.add_child(t[1])
    enode.add_child(node.Node('+', []))
    enode.add_child(t[3])
    t[0] = enode

def p_E_EminusT(t):
    'E : E minus T'
    enode = node.Node('E', [])
    enode.add_child(t[1])
    enode.add_child(node.Node('-', []))
    enode.add_child(t[3])
    t[0] = enode

def p_E_T(t):
    'E : T'
    enode = node.Node('E', [])
    enode.add_child(t[1])
    t[0] = enode

def p_T_TtimesF(t):
    'T : T times F'
    tnode = node.Node('T', [])
    tnode.add_child(t[1])
    tnode.add_child(node.Node('*', []))
    tnode.add_child(t[3])
    t[0] = tnode

def p_T_TdivideF(t):
    'T : T divide F'
    tnode = node.Node('T', [])
    tnode.add_child(t[1])
    tnode.add_child(node.Node('/', []))
    tnode.add_child(t[3])
    t[0] = tnode

def p_T_F(t):
    'T : F'
    tnode = node.Node('T', [])
    tnode.add_child(t[1])
    t[0] = tnode

def p_T_lpErp(t):
    'F : lparen E rparen'
    fnode = node.Node('F', [])
    fnode.add_child(node.Node('(', []))
    fnode.add_child(t[2])
    fnode.add_child(node.Node(')', []))
    t[0] = fnode

def p_T_number(t):
    'F : number'
    fnode = node.Node('F', [])
    number_node = node.Node('number', [])
    number_node.value = int(t[1])
    fnode.add_child(number_node)
    t[0] = fnode

def p_error(t):
    print(f'Syntax error at {t.value}')

parser = yacc.yacc()
end_marker = "n"
analisis_type = "   (Ascendente)"
while True:
    try:
        s = input('input > ')
    except EOFError:
        break
    root = parser.parse(s)
    print(f'The result is {evaluator.evaluate(root)}')
    root.add_child(node.Node('n', [])) # Marker for end of input
    graph.create_gv(root)
    graph.view_gv(s+end_marker+analisis_type)
