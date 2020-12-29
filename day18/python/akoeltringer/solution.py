#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""(cheating) Solution of Problem of Day 18"""

# stdlib imports

# 3rd party lib imports
import sly

# own stuff
import utils


class CalcLexer(sly.Lexer):
    tokens = {NUMBER, PLUS, TIMES, LPAREN, RPAREN}
    ignore = " \t"

    # Tokens
    NUMBER = r"\d+"

    # Special symbols
    PLUS = r"\+"
    TIMES = r"\*"
    LPAREN = r"\("
    RPAREN = r"\)"

    # Ignored pattern
    ignore_newline = r"\n+"

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class CalcParserP1(sly.Parser):
    tokens = CalcLexer.tokens

    precedence = (("left", PLUS, TIMES),)

    def __init__(self):
        self.names = {}

    @_("expr")
    def statement(self, p):
        return p.expr

    @_("expr PLUS expr")
    def expr(self, p):
        return p.expr0 + p.expr1

    @_("expr TIMES expr")
    def expr(self, p):
        return p.expr0 * p.expr1

    @_("LPAREN expr RPAREN")
    def expr(self, p):
        return p.expr

    @_("NUMBER")
    def expr(self, p):
        return int(p.NUMBER)


class CalcParserP2(CalcParserP1):
    tokens = CalcLexer.tokens

    precedence = (("left", TIMES), ("left", PLUS))

    def __init__(self):
        self.names = {}

    @_("expr")
    def statement(self, p):
        return p.expr

    @_("expr PLUS expr")
    def expr(self, p):
        return p.expr0 + p.expr1

    @_("expr TIMES expr")
    def expr(self, p):
        return p.expr0 * p.expr1

    @_("LPAREN expr RPAREN")
    def expr(self, p):
        return p.expr

    @_("NUMBER")
    def expr(self, p):
        return int(p.NUMBER)


lexer = CalcLexer()
parser_p1 = CalcParserP1()
parser_p2 = CalcParserP2()


def evaluate_code_p1(text: str) -> int:
    return parser_p1.parse(lexer.tokenize(text))


def evaluate_code_p2(text: str) -> int:
    return parser_p2.parse(lexer.tokenize(text))


def main() -> None:
    input_raw = utils.get_input(__file__)

    # part 1:
    total = sum([evaluate_code_p1(line) for line in input_raw.strip().split("\n")])
    print(f"part 1: {total}")

    # part 2:
    total = sum([evaluate_code_p2(line) for line in input_raw.strip().split("\n")])
    print(f"part 2: {total}")


if __name__ == "__main__":
    main()
