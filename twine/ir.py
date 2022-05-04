from typing import Dict, NamedTuple, Union, Tuple, List
from lark import Transformer, v_args, Tree

# Representa um módulo Twine
IR = Dict[str, "Declaration"]

# Representa o lado direito de uma declaração de função
Declaration = Tuple["ArgDefs", type, "SExpr"]

# A lista de argumentos é uma lista de duplas (nome, tipo) para cada argumento
ArgDefs = List[Tuple[str, type]]

# Representa uma expressão Twine como S-Expression
SExpr = Union[list, str, int, bool]


def transform(tree: Tree) -> IR:
    """
    Transforma uma árvore sintática que descreve um módulo Twine
    na representação interna do código como um dicionário de definições.
    """
    transformer = IrTransformer()
    twine = transformer.transform(tree)
    return dict(twine)

class IrTransformer(Transformer):
    def program(self, tree):
        return tree

    @v_args(inline=True)
    def define(self, name, params, type, body):
        return [name,(params, type, body)]
    
    @v_args(inline=True)
    def IDENTIFIER(self, name):
        return name.value

    def params(self, params):
        return list(params)

    @v_args(inline=True)
    def body(self, *args):
        if(len(args) == 1):
            return args[0]
        else:
            l = []
            for arg in args:
                if(type(arg) == list and arg[0] == "print"):
                    l.append(arg[0])
                    l.append(arg[1])
                else:
                    l.append(arg)
            return l

    @v_args(inline=True)
    def print_expression(self, expr):
        return ["print", expr]

    @v_args(inline=True)
    def TYPE(self, type):
        if(type.value == 'integer'):
            return int
        else:
            return bool
    
    @v_args(inline=True)
    def INTEGER(self, token):
        return int(token.value)

    @v_args(inline=True)
    def param(self, tree, v):
        return tuple([tree, v])

    @v_args(inline=True)
    def add(self, x, y):
       return ['+', x, y]

    @v_args(inline=True)
    def sub(self, x, y):
        return ['-', x, y]

    @v_args(inline=True)
    def lt(self, x, y):
        return ['<', x, y]
    
    @v_args(inline=True)
    def cond(self, exp, then, els):
        return ['if', exp, then,els]

    @v_args(inline=True)
    def fcall(self, name, args):
        x = [name]
        for arg in args:
            x.append(arg)
        return x

    @v_args(inline=True)
    def eq(self, x, y):
        return ['=', x, y]

    @v_args(inline=True)
    def BOOLEAN(self, token):
        return token == 'true'
        
    @v_args(inline=True)
    def args(self, exp1, exp2=None):
        if(exp2 != None):
            return [exp1, exp2]
        return [exp1]
    
    @v_args(inline=True)
    def or_(self, x, y):
        return ['|', x, y]

    @v_args(inline=True)
    def and_(self, x, y):
        return ['^', x, y]

    @v_args(inline=True)
    def mul(self, x, y):
        return ['*', x, y]

    @v_args(inline=True)
    def div(self, x, y):
        return ['/', x, y]

    @v_args(inline=True)
    def not_(self, x):
        return ['~', x]

    @v_args(inline=True)
    def neg(self, x):
        return ['-', x]
    