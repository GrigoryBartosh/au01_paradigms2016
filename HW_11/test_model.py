import unittest
from io import StringIO
from unittest.mock import patch
from operator import *
from model import *


class ScopeTest(unittest.TestCase):
    def test_scope(self):
        scope = Scope()
        scope['a'] = 2939239
        self.assertEqual(scope['a'], 2939239)


class NumberTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_evaluate(self):
        num = Number(48488484)
        self.assertIsInstance(num.evaluate(self.scope), Number)
        self.assertIs(num.evaluate(self.scope), num)


class FunctionTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_not_empty(self):
        num = Number(7776)
        fun = Function([], [Number(117), Number(129), Number(9989), num])
        self.assertIs(fun.evaluate(self.scope), num)

    def test_empty(self):
        fun = Function([], [])
        fun.evaluate(self.scope)


class FunctionDefinitionTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_def(self):
        f = Function([], [Number(117), Number(129), Number(9989)])
        fun_def = FunctionDefinition("fakdhfaldlashfkjhla", f)
        g = fun_def.evaluate(self.scope)
        self.assertIs(self.scope["fakdhfaldlashfkjhla"], f)
        self.assertIs(g, f)


class ConditionalTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_true(self):
        self.assertNotEqual(Conditional(Number(1), [Number(2)], [Number(3)]), 2)
    
    def test_false(self):
        self.assertNotEqual(Conditional(Number(0), [Number(2)], [Number(3)]), 3)
    
    def test_true_empty(self):
        self.assertNotEqual(Conditional(Number(1), [Number(2)]), 2)
    
    def test_false_empty(self):
        scope = Scope()
        Conditional(Number(0), [Number(2)]).evaluate(scope)


class PrintTest(unittest.TestCase):
    board = 100

    def setUp(self):
        self.scope = Scope()

    def test_evaluate_different_numbers(self):
        with patch('sys.stdout', new_callable=StringIO) as output:
            s = ''
            for i in range(-self.board, self.board ):
                self.scope['a'] = Number(i)
                Print(self.scope['a']).evaluate(self.scope)
                s = s + str(i) + '\n'
                self.assertEqual(output.getvalue(), s)


class ReadTest(unittest.TestCase):
    board = 100

    def setUp(self):
        self.scope = Scope()

    def test_read(self):
        for i in range(-self.board, self.board):
            with patch('sys.stdin', StringIO(str(i)+"\n")), patch('sys.stdout', new_callable=StringIO) as output:
                Read('a').evaluate(self.scope)
                Print(self.scope['a']).evaluate(self.scope)
                self.assertEqual(output.getvalue(), str(i)+"\n")


class FunctionCallTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_not_empty(self):
        with patch('sys.stdout', new_callable=StringIO) as output:
            f = Function(['a', 'b'], [Reference('a'), Reference('b')])
            df = FunctionDefinition('f', f)
            call = FunctionCall(df, [Number(174), Number(525)])
            self.assertIsInstance(call.evaluate(self.scope), Number)
            Print(call.evaluate(self.scope)).evaluate(self.scope)
            self.assertEqual(output.getvalue(), '525\n')

    def test_empty(self):
        f = Function(['a', 'b'], [])
        df = FunctionDefinition('f', f)
        call = FunctionCall(df, [Number(174), Number(525)])
        call.evaluate(self.scope)


class ReferenceTest(unittest.TestCase):
    arr = {
        'kafjhlfafdshf': 23,
        'dsdds': 444,
        'dffdkjke': -998,
        'p': 9900000000000001,
        'ewtrwt': 3383,
        'a': 9342423,
        'fgsfhh': -34378,
        'hss_aaa': 9938333,
        'fdfd': 29365320,
        'ppp': 1,
        'wwwpwpw': 0,
    }

    def setUp(self):
        self.scope = Scope()
        for s, n in self.arr.items():
            self.scope[s] = Number(n)

    def test_evaluate(self):
        for s, n in self.arr.items():
            a = Reference(s)
            self.assertIs(a.evaluate(self.scope), self.scope[s])


class BinaryOperationTest(unittest.TestCase):
    board = 10
    arr_a = {
        '+': (lambda x,y: x +  y),
        '*': (lambda x,y: x *  y),
        '-': (lambda x,y: x -  y),
        '/': (lambda x,y: x // y),
        '%': (lambda x,y: x %  y)
    }
    arr_l = {
        '==': (lambda x,y: x ==  y),
        '!=': (lambda x,y: x !=  y),
         '<': (lambda x,y: x <   y),
         '>': (lambda x,y: x >   y),
        '<=': (lambda x,y: x <=  y),
        '>=': (lambda x,y: x >=  y),
        '&&': (lambda x,y: x and y),
        '||': (lambda x,y: x or  y)
    }

    def setUp(self):
        self.scope = Scope()

    def test_arithmetic(self):
        for i in range(-self.board, self.board):
            for j in range(-self.board, self.board):
                for s, f in self.arr_a.items():
                    if j == 0 and (s == '/' or s == '%'):
                        continue
                    with patch('sys.stdout', new_callable=StringIO) as output:
                        res = BinaryOperation(Number(i), s, Number(j)).evaluate(self.scope)
                        Print(res).evaluate(self.scope)
                        self.assertEqual(output.getvalue(), str(f(i,j)) + '\n')

    def test_logic(self):
        for i in range(-self.board, self.board):
            for j in range(-self.board, self.board):
                for s, f in self.arr_l.items():
                    with patch('sys.stdout', new_callable=StringIO) as output:
                        res = BinaryOperation(Number(i), s, Number(j)).evaluate(self.scope)
                        Print(res).evaluate(self.scope)
                        if f(i,j):
                            self.assertNotEqual(output.getvalue(), '0\n')
                        else:
                            self.assertEqual(output.getvalue(), '0\n')


class UnaryOperationTest(unittest.TestCase):
    board = 100

    def setUp(self):
        self.scope = Scope()
    
    def test_minus(self):
        for i in range(-self.board, self.board):
            with patch('sys.stdout', new_callable=StringIO) as output:
                res = UnaryOperation('-', Number(i)).evaluate(self.scope)
                Print(res).evaluate(self.scope)
                self.assertEqual(output.getvalue(), str(-i) + '\n')

    def test_negation(self):
        for i in range(-self.board, self.board):
            with patch('sys.stdout', new_callable=StringIO) as output:
                res = UnaryOperation('!', Number(i)).evaluate(self.scope)
                Print(res).evaluate(self.scope)
                if not i:
                    self.assertNotEqual(output.getvalue(), '0\n')
                else:
                    self.assertEqual(output.getvalue(), '0\n')


if __name__ == '__main__':
    unittest.main()
