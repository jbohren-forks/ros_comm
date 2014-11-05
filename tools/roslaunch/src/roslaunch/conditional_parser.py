
# Basic conditional expression parser based on:
# https://gist.github.com/cynici/5865326#file-afisparser-py

import sys
import traceback
import logging

from pyparsing import ParserElement, Word, CaselessKeyword, CaselessLiteral,\
    Combine, Optional,\
    quotedString, removeQuotes, operatorPrecedence, opAssoc,\
    oneOf,\
    alphas, alphanums, nums


ParserElement.enablePackrat()


def _operatorOperands(tokenlist):
    "generator to extract operators and operands in pairs"
    it = iter(tokenlist)
    while 1:
        try:
            o1 = next(it)
            o2 = next(it)
            yield (o1, o2)
        except StopIteration:
            break


def eval_sign_op(s, l, t):
    "Evaluate expressions with a leading + or - sign"
    sign, value = t[0]
    mult = {'+': 1, '-': -1}[sign]
    res = mult * value
    logging.debug("SIGN: t=%s res=%s" % (t, res))
    return res


def eval_mult_op(s, l, t):
    "Evaluate multiplication and division expressions"
    prod = t[0][0]
    for op, val in _operatorOperands(t[0][1:]):
        if op == '*':
            prod *= val
        if op == '**':
            prod **= val
        if op == '/':
            prod /= val
        if op == '//':
            prod //= val
        if op == '%':
            prod %= val
    logging.debug("MULT: t=%s res=%s" % (t, prod))
    return prod


def eval_add_op(s, l, t):
    "Evaluate addition and subtraction expressions"
    sum = t[0][0]
    for op, val in _operatorOperands(t[0][1:]):
        if op == '+':
            sum += val
        if op == '-':
            sum -= val
    logging.debug("ADD: t=%s res=%s" % (t, sum))
    return sum


def eval_comp_op(s, l, t):
    "Evaluate comparison expressions"
    opMap = {
        "<": lambda a, b: a < b,
        "<=": lambda a, b: a <= b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "==": lambda a, b: a == b,
        "is": lambda a, b: a is b,
        "!=": lambda a, b: a != b,
        }
    res = False
    val1 = t[0][0]
    for op, val2 in _operatorOperands(t[0][1:]):
        fn = opMap[op]
        if not fn(val1, val2):
            break
        val1 = val2
    else:
        res = True
    logging.debug("COMP: t=%s res=%s\n" % (t, res))
    return res


def eval_and(s, l, t):
    bool1, op, bool2 = t[0]
    res = bool1 and bool2
    logging.debug("%s %s %s res=%s" % (bool1, op, bool2, res))
    return res


def eval_or(s, l, t):
    bool1, op, bool2 = t[0]
    res = bool1 or bool2
    logging.debug("%s %s %s res=%s" % (bool1, op, bool2, res))
    return res


def eval_not(s, l, t):
    op, bool1 = t[0]
    res = not bool1
    logging.debug("%s %s res=%s" % (op, t[0], res))
    return res

Param = Word(alphas+"_", alphanums+"_")
Qstring = quotedString(r".*").setParseAction(removeQuotes)
PosBool = (CaselessLiteral('true') | CaselessLiteral('false')
           ).setParseAction(lambda s, l, t: [t[0].lower() == 'true'])
PosInt = Word(nums).setParseAction(lambda s, l, t: [int(t[0])])
PosReal = (Combine(Word(nums) + Optional("." + Word(nums)) + oneOf("E e") +
                   Optional(oneOf('+ -')) + Word(nums))
           | Combine(Word(nums) + "." + Word(nums))
           ).setParseAction(lambda s, l, t: [float(t[0])])

signop = oneOf('+ -')
multop = oneOf('* ** / // %')
addop = oneOf('+ -')
compop = oneOf("is < <= > >= == !=")
andop = CaselessKeyword("and")
orop = CaselessKeyword("or")
notop = CaselessKeyword("not")


class ConditionalParser(object):
    def __init__(self, param_dic={}):
        self.param_dic = param_dic

    def set_param(self, s, l, t):
        "Replace keywords with actual values using param_dic mapping"
        param = t[0]
        return self.param_dic.get(param, '')

    def eval_conditional(self, filter_expr):
        keyword = Param.copy()
        atom = PosBool | PosReal | PosInt | Qstring | keyword.setParseAction(self.set_param)
        expr = operatorPrecedence(atom, [
            (signop, 1, opAssoc.RIGHT, eval_sign_op),
            (multop, 2, opAssoc.LEFT, eval_mult_op),
            (addop, 2, opAssoc.LEFT, eval_add_op),
            (compop, 2, opAssoc.LEFT, eval_comp_op),
            (notop, 1, opAssoc.RIGHT, eval_not),
            (andop, 2, opAssoc.LEFT, eval_and),
            (orop, 2, opAssoc.LEFT, eval_or),
        ])
        return expr.parseString(filter_expr, parseAll=True)[0]


def main():
    parameters = {
        'FRP': 100,
        'satellite': 'A',
    }
    tests = [
        # ( Filter_string, Expected_result )
        ("not 1", False),
        ("not True", False),
        ("not False", True),
        ("199 / 2 > FRP", False),
        ("5 + 45 * 2 > FRP", False),
        ("-5+5 < FRP", True),
        ("satellite is 'N'", False),
        ("satellite is 'A'", True),
        ("FRP - 100 == 0", True),
        ("FRP == 1 and satellite == 'T'", False),
        ("FRP != 1 and not satellite == 'T'", True),
        # packrat speeds up nested expressions tremendously
        ("(FRP == 1) and ((satellite == 'T') or (satellite is 'A'))", False),
    ]

    logging.basicConfig(level=logging.DEBUG)
    got_error = 0
    ap = ConditionalParser(parameters)
    for filter_expr, expected in tests:
        try:
            result = ap.eval_conditional(filter_expr)
            if result != expected:
                raise AssertionError("yields %s" % (result))
        except Exception, err:
            traceback.print_exc(file=sys.stderr)
            print "%s: %s" % (filter_expr, err)
            got_error += 1
    return got_error

if __name__ == "__main__":
    sys.exit(main())
