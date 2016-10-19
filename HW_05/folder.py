from yat.model import *
from yat.printer import *

class ConstantFolder:

	def visit(self, tree):
		name = tree.__class__.__name__
		function = getattr(self, "visit" + name)
		return function(tree)

	def visitNumber(self, number):
		return number

	def visitFunction(self, foo):
		if foo.body != None:
			for i in range(len(foo.body)):
				foo.body[i] = self.visit(foo.body[i])
		return foo

	def visitFunctionDefinition(self, foo):
		foo.function = self.visit(foo.function)
		return foo

	def visitConditional(self, conditional):
		conditional = self.visit(conditional.condtion)
		if conditional.if_true != None:
			for i in range(len(conditional.if_true)):
				conditional.if_true[i] = self.visit(conditional.if_true[i])
		if conditional.if_false != None:
			for i in range(len(conditional.if_false)):
				conditional.if_false[i] = self.visit(conditional.if_false[i])
		return conditional

	def visitPrint(self, prnt):
		prnt.expr = self.visit(prnt.expr)
		return prnt

	def visitRead(self, read):
		return read

	def visitFunctionCall(self, foo):
		for i in range(len(foo.args)):
			foo.args[i] = self.visit(foo.args[i])
		return foo

	def visitReference(self, reference):
		return reference

	def visitBinaryOperation(self, binary):
		binary.lhs = self.visit(binary.lhs)
		binary.rhs = self.visit(binary.rhs)
		if isinstance(binary.lhs, Number) and isinstance(binary.rhs, Number):
			return binary.evaluate(None)
		if isinstance(binary.lhs, Number) and isinstance(binary.rhs, Reference) and binary.lhs.value == 0 and binary.op == '*':
			return Number(0)
		if isinstance(binary.lhs, Reference) and isinstance(binary.rhs, Number) and binary.rhs.value == 0 and binary.op == '*':
			return Number(0)
		if isinstance(binary.lhs, Reference) and isinstance(binary.rhs, Reference) and binary.op == '-' and binary.lhs.name == binary.rhs.name:
			return Number(0)
		return binary

	def visitUnaryOperation(self, unary):
		unary.expr = self.visit(unary.expr)
		if isinstance(unary.expr, Number):
			return unary.evaluate(None)
		return unary
