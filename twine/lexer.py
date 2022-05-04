from typing import Iterable
from lark import Token
# from .grammar import GRAMMAR
import re

# LEX_LARK:
# def lex(src: str) -> Iterable[Token]:
#     return GRAMMAR.lex(src)

# COMPILADOR_ORG:
# def lex(src: str) -> Iterable[Token]:
#     """
#     Analiza o código fonte e retorna uma sequência de tokens.
#     """
#     yield Token("IDENTIFIER", "main")
#     yield Token("EQUAL", "=")
#     yield Token("F", "f")
#     yield Token("LPAR", "(")
#     yield Token("RETURNS", "returns")
#     yield Token("IDENTIFIER", "integer")
#     yield Token("RPAR", ")")
#     yield Token("INTEGER", "42")

# RE_BASICO:
REGEX_MAP = [
    ("BOOLEAN", r"true | false"),
    ("COMMA", r'\,'),
    ("COMMENT", r"%.*"),
    ("EQUAL", r"\="),
    ("F", r"f"),
    ("HAT", r"\^"),
    ("RETURNS", r"returns"),
    ("IDENTIFIER", r"^[\$a-zA-Z][\$a-zA-Z0-9_]*"),
    ("INTEGER", r"0|[1-9][0-9]*"),
    ("LPAR", r"\("),
    ("LESS", r"<"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("PIPE", r"\|"),
    ("PLUS", r"\+"),
    ("RPAR", r"\)"),
    ("SEMICOLON", r":"),
    ("SLASH", r"\/"),
    ("TILDE", r"~"),
]


def lex(src: str) -> Iterable[Token]:
    words = src.split()
    for word in words:
        kind = classify_token(word)
        if(kind == "COMMENT"): continue
        yield Token(kind, word)
        # se você não reconhece/entende o comando yield, sugiro um 
        # link: http://pythonclub.com.br/python-generators.html

def classify_token(word: str) -> str:
    for (nome, regex) in REGEX_MAP:
        if re.fullmatch(regex, word):
            return nome
    raise SyntaxError(f'elemento não reconhecido: {word!r}')