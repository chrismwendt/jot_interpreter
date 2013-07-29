import copy
import types
from string import ascii_lowercase
import sys
import requests
import re

# ''    -> I
# '0ab' -> (ab)
# '1'   -> SK

S = lambda x: lambda y: lambda z: x(copy.deepcopy(z))(y(copy.deepcopy(z)))
K = lambda x: lambda y: x
I = lambda x: x

def jot(s, v=I):
    if len(s) == 0:
        return v
    else:
        if s[0] == '1':
            return jot(s[1:], v(S)(K))
        else:
            return jot(s[1:], lambda f: lambda a: v(f(a)))

asciiargs = list(ascii_lowercase)
class Variable:
    def __init__(self, name=None):
        self.name = name
        if self.name == None:
            self.name = id(self)
    def toString(self, memo={}):
        global asciiargs
        n = self.name
        if len(memo) == 0:
            memo[n] = 0
        if not n in memo:
            memo[n] = max(memo.values()) + 1
        return asciiargs[memo[n]]
    def __deepcopy__(self, memo):
        return Variable(name=self.name)
class Application:
    def __init__(self, function, argument):
        self.function, self.argument = function, argument
    def toString(self, memo={}):
        if isinstance(self.argument, Application):
            return '{} ({})'.format(self.function.toString(memo=memo), self.argument.toString(memo=memo))
        else:
            return '{} {}'.format(self.function.toString(memo=memo), self.argument.toString(memo=memo))
class Abstraction:
    def __init__(self, parameter, body):
        self.parameter, self.body = parameter, body
    def toString(self, memo={}, enclosed_by_abstraction=False):
        p = self.parameter.toString(memo=memo)
        b = ''
        #return '(\{}.{})'.format(p, self.body.toString(memo=memo))
        if enclosed_by_abstraction:
            if isinstance(self.body, Abstraction):
                return '{}'.format(self.body.toString(memo=memo, enclosed_by_abstraction=True))
            else:
                return '{}'.format(self.body.toString(memo=memo))
        if isinstance(self.body, Abstraction):
            ps = [p]
            e = self.body
            while isinstance(e, Abstraction):
                ps.append(e.parameter.toString(memo=memo))
                e = e.body
            b = self.body.toString(memo=memo, enclosed_by_abstraction=True)
            return '(\{}.{})'.format(''.join(ps), b)
        else:
            b = self.body.toString(memo=memo)
            return '(\{}.{})'.format(p, b)

class inspector:
    def __init__(self, memo=None):
        self.memo = memo if memo else Variable()
    def __call__(self, argument):
        if not isinstance(argument, inspector):
            v1 = Variable()
            v2 = Variable(v1.name)
            argument = inspector(Abstraction(v1, inspector()(argument(inspector(v2))).memo.argument))
        self.memo = Application(self.memo, argument.memo)
        return self
    def toString(self, memo={}):
        return self.memo.toString(memo=memo)

def lambdaToString(expression):
    return inspector()(expression).memo.argument.toString({})

arguments = list(ascii_lowercase)
def _expand(terms, new):
    global arguments
    if new == '':
        terms += arguments.pop(0)
        return ''
    if new[0] in 'SK':
        terms.append(new[0])
        return new[1:]
    if new[0] == '0':
        new = new[1:]
        l = []
        new = _expand(l, new)
        r = []
        new = _expand(r, new)
        if type(l[0]) == list:
            terms.append(l[0]+r)
        else:
            terms.append(l+r)
        return new
    return new[1:]
def expand(s):
    global arguments
    arguments = list(ascii_lowercase)
    s = s.replace('1', 'SK')
    terms = []
    s = _expand(terms, s)
    while s:
        s = _expand(terms, s)
    def construct(terms):
        if type(terms) is list:
            return '('+' '.join([construct(term) for term in terms])+')'
        return terms
    return construct(terms)

print '================'

n = 10
programs = [bin(program)[2:] if program != 0 else '' for program in range(n)]
#programs = ['1', '10', '11', '100', '101', '110', '111', '1000', '1110011', '1111001', '1111000000111']
programs = [bin(7687)[2:]]
#programs = ['11111111000111111000111001111110001110011111110001111111110000011111111100000']
#programs = ['10']
for program in programs:
    #r = requests.post('http://188.178.232.233/cgi-bin/lamreduce', data={'expression':expand(program), 'action':'normalize', 'evalorder':'normal order'})
    print int(program if program != '' else '0', 2), '\''+program+'\'', expand(program)
    e = jot(program)
    print lambdaToString(e)
    print lambdaToString(e(I))
    print lambdaToString(e(I)(I))
    print lambdaToString(e(I)(I)(I))
    print lambdaToString(e(I)(I)(I)(I))
    #print re.match('.*</P>(.*)<BR>', r.content).group(1)
    print
    sys.stdout.flush()

#1111000000111
#S K S K S K S K (S K S K S K a)

#1110011
#SKSKSK(SKS)KSKabc
#KSKIKSKabc
#SIKSKabc
#IS(KS)Kabc
#KSa(Ka)bc
#S(Ka)bc
#Kac(bc)
#a(bc)
#-------------
#lambdaToString(jot('1110011'))
#lambdaToString(SKSKSK(SKS)KSK)
#inspector()(SKSKSK(SKS)KSK).memo.argument.toString({})
#idk, skip a few steps
#SKSKSK(SKS)KSK
#S(\p.S)K
#(\x.\y.\z.xz(yz))(\p.(\l.\m.\n.ln(mn)))(\f.\g.f)
#(\y.\z.(\p.(\l.\m.\n.ln(mn)))z(yz))(\f.\g.f)
#(\z.(\p.(\l.\m.\n.ln(mn)))z((\f.\g.f)z))
#(\z.(\p.(\l.\m.\n.ln(mn)))z((\f.\g.f)z))a
#(\m.\n.(\g.a)n(mn))b
#(\n.(\g.a)n(bn))
#(\n.(\g.a)n(bn))c
#(\g.a)c(bc)
#a(bc)

#[0,1,2]->(02(12))
#[f,a]->([0,1,2]->(02(12)) (fa))xy
#[0,1,2]->(02(12)) (xy)
#[1,2]->(xy2(12)) (xy)

#[0]->(0) 1110011
#[0,1]->(1) 110011
#[0,1]->(0) 10011
#[0,1,2]->(02(12)) 0011
#[0,1,2,3]->((01)3(23)) 011
#[0,1,2,3,4]->((01)2)4(34) 11
#[0,1,2,3,4]->((01)2)4(34) ([a,b,c]->(ac(bc)))([d,e]->(d))1
#[1,2,3,4]->((([a,b,c]->(ac(bc)))1)2)4(34) ([d,e]->(d))1
#[1,2,3,4]->(([b,c]->(1c(bc)))2)4(34) ([d,e]->(d))1
#[1,2,3,4]->([c]->(1c(2c)))4(34) ([d,e]->(d))1
#[1,2,3,4]->(14(24))(34) ([d,e]->(d))1
#[2,3,4]->(([d,e]->(d))4(24))(34) 1
#[2,3,4]->4(34) 1
#[2,3,4]->4(34) ([f,g,g]->(fh(gh)))([i,j]->(i))
#[3,4]->4(34) ([i,j]->(i))
#[4]->4(([i,j]->(i))4) 
#[4]->4([j]->(4)) 
#[0]->0([1]->(0)) 

#1110011
#SKSKSK(SKS)K

#1111000000111
#SKSKSKSK(SKSKSKa)b
#KSKSK(SKSKSKa)b
#SSK(SKSKSKa)b
#SSK(KSKa)b
#SSK(Sa)b
#S(Sa)(K(Sa))b
#Sab(Sa)
#a(Sa)(b(Sa))
#a(\yz.az(yz))(b(\mn.an(mn)))
#[a, b] -> a ([c d] -> a d (c d)) (b ([m n] -> a n (m n)))

# v = variable, ab = abstraction, ap = application
# ''    I         0 -> 0                   0 -> 0
# ab(v0, v0)
# '1'   SK01      0 -> 1 -> 1              0,1 -> 1
# ab(v0, ab(v1, v1))
# '10'  SK(01)2   0 -> 1 -> 2 -> 2         0,1,2 -> 2
# ab(v0, ab(v1, ab(v2, v2)))
# '11'  SKSK01    0 -> 1 -> 0              0,1 -> 0
# ab(v0, ab(v1, v0))
# '100' SK(012)3  0 -> 1 -> 2 -> 3 -> 3    0,1,2,3 -> 3
# ab(v0, ab(v1, ab(v2, ab(v3, v3))))
# '101' SK(SK)0   0 -> 0                   0 -> 0
# ab(v0, v0)
# '110' SKSK(01)2 0 -> 1 -> 2 -> 0 1       0,1,2 -> 0 1
# ab(v0, ab(v1, ab(v2, ap(v0, v1))))
# '111' SKSKSK012 0 -> 1 -> 2 -> 0 2 (1 2) 0,1,2 -> 0 2 (1 2)
# ab(v0, ab(v1, ab(v2, ap(ap(v0, v2), ap(v1, v2)))))
# ...
# 10101110011   SK(SK)(SK)SKSK(SKS)K0    0 -> 0 (1 -> 0)   0 -> 0 (1 -> 0)
# ab(v0, ap(v0, ab(v1, v0)))
