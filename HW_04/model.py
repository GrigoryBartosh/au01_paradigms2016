class Scope:

    def __init__(self, parent=None):
        self.dct = {}
        self.parent = parent

    def __getitem__(self, item):
        if not item in self.dct:
            if self.parent != None:
                return self.parent[item]
            else:
                return None
        return self.dct[item]

    def __setitem__(self, item, x):
        self.dct[item] = x

class Number:

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        res = None
        for f in self.body:
            res = f.evaluate(scope)
        return res


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    def __init__(self, condtion, if_true, if_false=None):
        self.condtion = condtion
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        tmp = None
        res = None
        if self.condtion.evaluate(scope).value:
            tmp = self.if_true
        else:
            tmp = self.if_false
        for f in tmp:
            res = f.evaluate(scope)
        return res


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope).value
        print(res)
        return res


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        res = Number(int(input()))
        scope[self.name] = res
        return res


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for name, x in zip(function.args, self.args):
            call_scope[name] = x.evaluate(scope)
        return function.evaluate(call_scope)


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    oper = {
         '+': (lambda x,y: x +   y),
         '*': (lambda x,y: x *   y),
         '-': (lambda x,y: x -   y),
         '/': (lambda x,y: x //  y),
         '%': (lambda x,y: x %   y),
        '==': (lambda x,y: x ==  y),
        '!=': (lambda x,y: x !=  y),
         '<': (lambda x,y: x <   y),
         '>': (lambda x,y: x >   y),
        '<=': (lambda x,y: x <=  y),
        '>=': (lambda x,y: x >+  y),
        '&&': (lambda x,y: x and y),
        '||': (lambda x,y: x or  y)
    }

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        lhs = self.lhs.evaluate(scope)
        rhs = self.rhs.evaluate(scope)
        return Number(self.oper[self.op](lhs.value, rhs.value))


class UnaryOperation:

    oper = {
        '-': (lambda x: -x),
        '!': (lambda x: not x)
    }

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        expr = self.expr.evaluate(scope)
        return Number(self.oper[self.op](expr.value))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)

def my_tests():
    scope = Scope()
    
    a = Read('a').evaluate(scope)
    b = Read('b').evaluate(scope)
    Print(BinaryOperation(a, '*', b)).evaluate(scope)

    scope['zero'] = Number(0)
    cond = BinaryOperation(scope['a'], '>', scope['zero'])
    if_true = Print(scope['a'])
    if_false = Print(UnaryOperation('-', scope['a']))
    Conditional(cond, [if_true], [if_false]).evaluate(scope)

    Print(UnaryOperation('-', BinaryOperation(scope['b'], '/', scope['a']))).evaluate(scope)

    func =  Function(
                ('x', 'y'), [
                            Print(
                                BinaryOperation(
                                            Reference('x'), '*', Reference('y')
                                )
                            ), 
                            Print(
                                BinaryOperation(
                                            Reference('x'), '+', Reference('y')
                                )
                            )
                            ]
            )

    scope['n'] = Number(2)
    scope['m'] = Number(4)
    FunctionCall(FunctionDefinition("func", func), [scope['n'], scope['m']]).evaluate(scope)

if __name__ == '__main__':
    example()
    my_tests()
