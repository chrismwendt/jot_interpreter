# TODO 0-based indices

# Jot
# '' -> I
# '0' -> `ab
# '1' -> SK

from pyparsing import *
import copy
import sys

def main():
    while True:
        try:
            string = input().rstrip()
        except:
            break
        debug = False
        lambda_ = False
        if len(string) > 0 and string[0] == 'd':
            debug = True
            string = string[1:]
        if len(string) > 0 and string[0] == 'l':
            lambda_ = True
            string = string[1:]
            expression = Expression.fromLambda(string)
        else:
            expression = Expression.fromJot(string)
        if debug:
            print('input     ', string)
            if not lambda_:
                print('lambda    ', expression)
        expression.normalized()
        if debug:
            print('normalized', expression.normalized())
            print('output    ', expression.toBinary())
        else:
            print(expression.toBinary())
        print()

def jot(program):
    return Expression.fromJot(program).normalized().toBinary()

class Expression:
    @staticmethod
    def fromLambda(s):
        l = lambda l: Literal(l).suppress()
        term = Forward()
        abstraction = (l('^')+term).setParseAction(lambda t: Abstraction(*t))
        application = (l('`')+term+term).setParseAction(lambda t: Application(*t))
        index = (Regex('[1-9]') | l('(')+Regex('[1-9][0-9]+')+l(')')).setParseAction(lambda t: Variable(int(*t)))
        term <<= (abstraction | application | index)
        expression = term + StringEnd()
        return expression.parseString(s).asList()[0]
    @staticmethod
    def fromJot(s):
        S = lambda: Expression.fromLambda('^^^``31`21')
        K = lambda: Expression.fromLambda('^^2')
        I = lambda: Expression.fromLambda('^1')
        s = s.lstrip('0')
        has = I()
        while len(s) > 0:
            if s[0] == '1':
                has = Application(Application(has, S()), K())
            else:
                has = Abstraction(Abstraction(Application(has, Application(Variable(2), Variable(1)))))
            s = s[1:]
        return has

class Variable(Expression):
    def __init__(self, value):
        self.value = value
    def normalized(self):
        return self
    def getVariables(self, offset=0, memo={}):
        memo.setdefault(self.value - offset, []).append(self)
        return memo
    def substitute(self, index, expression):
        pass
    def __str__(self):
        s = str(self.value)
        return s if len(s) == 1 else '({})'.format(s)
    def toBinary(self):
        return '{}0'.format('1'*self.value)

class Abstraction(Expression):
    def __init__(self, body):
        self.body = body
    def normalized(self):
        # eta reduction: if term "t" does not contain 1, ^`t1 -> t
        self.body = self.body.normalized()
        if (isinstance(self.body, Application) and
        isinstance(self.body.argument, Variable) and
        self.body.argument.value == 1 and
        1 not in self.body.function.getVariables(offset=0, memo={})):
            shiftExternals(self.body.function, -1)
            return self.body.function
        return self
    def getVariables(self, offset=0, memo={}):
        return self.body.getVariables(offset=offset+1, memo=memo)
    def substitute(self, index, expression):
        expression = copy.deepcopy(expression)
        index += 1
        shiftExternals(expression, 1)
        if isinstance(self.body, Variable):
            if self.body.value == index:
                self.body = expression
        else:
            self.body.substitute(index, expression)
    def __str__(self):
        return '^{}'.format(self.body)
    def toBinary(self):
        return '00{}'.format(self.body.toBinary())

class Application(Expression):
    def __init__(self, function, argument):
        self.function, self.argument = function, argument
    def normalized(self):
        # beta reduction: substitute 1s in t with u, incrementing externals in u as necessary, decrementing externals in t by 1, `^tu -> v
        if not isinstance(self.function, Abstraction):
            self.function = self.function.normalized()
        if not isinstance(self.function, Abstraction):
            self.argument = self.argument.normalized()
            return self
        self.function.substitute(0, self.argument)
        shiftExternals(self.function, -1)
        self.function.body = self.function.body.normalized()
        return self.function.body
    def getVariables(self, offset=0, memo={}):
        self.function.getVariables(offset=offset, memo=memo)
        return self.argument.getVariables(offset=offset, memo=memo)
    def substitute(self, index, expression):
        if isinstance(self.function, Variable):
            if self.function.value == index:
                self.function = copy.deepcopy(expression)
        else:
            self.function.substitute(index, expression)
        if isinstance(self.argument, Variable):
            if self.argument.value == index:
                self.argument = copy.deepcopy(expression)
        else:
            self.argument.substitute(index, expression)
    def __str__(self):
        return '`{}{}'.format(self.function, self.argument)
    def toBinary(self):
        return '01{}{}'.format(self.function.toBinary(), self.argument.toBinary())

def shiftExternals(expression, delta):
    external_lists = [_list for offset, _list in expression.getVariables(offset=0, memo={}).items() if offset > 0]
    for e in [item for sublist in external_lists for item in sublist]:
        e.value += delta

def naturalToBinary(n):
    return bin(n+1)[3:] if n != 0 else ''

def binaryToNatural(b):
    return int('1'+b, 2) - 1

if __name__ == '__main__':
    main()
