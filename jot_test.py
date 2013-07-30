import py_lambda
import unittest
import pyparsing
from time import time

class Unit(unittest.TestCase):
    def setUp(self):
        self.longMessage = True

    def testFromJot(self):
        cases = [
	    ['', '^1'],
	    ['0', '^1'],
	    ['00', '^1'],
	    ['1', '``^1^^^``31`21^^2'],
	    ['01', '``^1^^^``31`21^^2'],
	    ['10', '^^```^1^^^``31`21^^2`21'],
	    ['11', '````^1^^^``31`21^^2^^^``31`21^^2']
	]

        cases = [{'input': c[0], 'output': c[1]} for c in cases]

        for case in cases:
            self.assertEqual(str(py_lambda.Expression.fromJot(case['input'])), case['output'], msg=case['input'])
	
    def testToBinary(self):
        cases = [
	    ['^1', '0010'],
	    ['^^^``132', '0000000101101110110'],
	    ['^^2', '0000110']
	]

        cases = [{'input': c[0], 'output': c[1]} for c in cases]

        for case in cases:
            self.assertEqual(py_lambda.Expression.fromLambda(case['input']).toBinary(), case['output'], msg=case['input'])

    def testDecodeEncodeEquality(self):
        cases = [
            '^1',
            '^^1',
            '^^^1',
            '`^1^1',
            '`^^1^1',
            '`^^2^1',
            '^^^``31`21',
            '`^^^``31`21^^2',
            '^^```^^^``31`21^^221',
            '`^^```^^^``31`21^^221^^2',
            '`^^```^^^``(10)1`21^^221^^2',
            '`^^```^^^``(10)1`21^^(25)(8408)1^^2'
        ]

        for case in cases:
            self.assertEqual(str(py_lambda.Expression.fromLambda(case)), case)

    def testTrueNegatives(self):
        cases = [
            '',
            '^',
            '`',
            '`1',
            '^^^',
            '^11',
            '^```223^'
        ]

        for case in cases:
            self.assertRaises(Exception, lambda: py_lambda.Expression.fromLambda(case))

    def testNormalized(self):
        casesIrreducible = [
            '^1',
            '^^1',
            '^^^1',
            '^^2',
            '^^^2',
            '^^^3',
            '^`11',
            '^``111',
            '^`1^1',
            '^^`12',
            '^`1^^2'
        ]
        casesEta = [
            ['^`^11', '^1'],
            ['^`^^11', '^^1'],
            ['^`^^21', '^^2'],
            ['^`^^^``31`211', '^^^``31`21'],
            ['^^``^121', '^1'],
            ['^^``^^^``31`2121', '^^^``31`21']
        ]
        casesBeta = [
            ['`^1^1', '^1'],
            ['`^1^^1', '^^1'],
            ['`^1^^^1', '^^^1'],
            ['`^1^^2', '^^2'],
            ['`^`11^1', '^1'],
            ['^`^`211', '^`11'],
            ['^`^^`12^2', '^^`1^3'],
            ['^`^^^`13^2', '^^^`1^4']
        ]
        casesMixed = [
            ['^1', '^1'],
            ['^^1', '^^1'],
            ['^^2', '^^2'],
            ['^^`21', '^1'],
            ['`^1^1', '^1'],
            ['^`^1^1', '^^1'],
            ['^`1^1', '^`1^1'],
            ['^`^11', '^1'],
            ['^`^21', '^1'],
            ['`^1^^1', '^^1'],
            ['^`11', '^`11'],
            ['`^^2^1', '^^1'],
            ['``^^2^1^1', '^1'],
            ['`^^1^1', '^1'],
            ['``^^2^1`^`11^`11', '^1'],
            ['`^^`21^^`2`21', '^^`2`21'],
            ['`^^`2`21^^`2`21', '^^`2`2`2`21'],
            ['`^^`2`2`21^^`2`21', '^^`2`2`2`2`2`2`2`21'],
            ['^`11', '^`11'],
            ['^`^11', '^1'],
            ['^`^21', '^1'],
            ['^^^``31`21', '^^^``31`21'],
            ['^^2', '^^2'],
            ['`^^2^1', '^^1'],
            ['``^^2^1^1', '^1'],
            ['`^^^``31`21^1', '^^`1`21'],
            ['^^``^^21`21', '^^1'],
            ['`^^^``31`21^^2', '^^1'],
            ['^^```^^^``31`21^^221', '^^1'],
            ['`^1^1', '^1'],
            ['`^^^`2``321^^1', '^1'],
            ['`^^^`2``321^1', '^^`2`21'],
            ['`^^^`2``321^^`2`21', '^^`2`2`21'],
            ['``^^^^``42``321^^`2`2`21^^`2`21', '^^`2`2`2`2`21']
        ]
        cases = [[c, c] for c in casesIrreducible] + casesEta + casesBeta + casesMixed

        cases = [{'input': c[0], 'output': c[1]} for c in cases]

        for case in cases:
            self.assertEqual(str(py_lambda.Expression.fromLambda(case['input']).normalized()), case['output'], msg='input was {}'.format(case['input']))

    def testNaturalToBinary(self):
        cases = [
            [0, ''],
            [1, '0'],
            [2, '1'],
            [3, '00'],
            [4, '01'],
            [5, '10'],
            [6, '11'],
            [7, '000'],
            [8, '001'],
            [9, '010'],
            [10, '011']
        ]

        cases = [{'input': c[0], 'output': c[1]} for c in cases]
        
        for case in cases:
            self.assertEqual(py_lambda.naturalToBinary(case['input']), case['output'])

    def testBinaryToNatural(self):
        cases = [
            ['', 0],
            ['0', 1],
            ['1', 2],
            ['00', 3],
            ['01', 4],
            ['10', 5],
            ['11', 6],
            ['000', 7],
            ['001', 8],
            ['010', 9],
            ['011', 10]
        ]

        cases = [{'input': c[0], 'output': c[1]} for c in cases]
        
        for case in cases:
            self.assertEqual(py_lambda.binaryToNatural(case['input']), case['output'])

def main():
    unittest.main()

if __name__ == '__main__':
    main()
