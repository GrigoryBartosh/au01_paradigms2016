from yat.model import *

class PrettyPrinter:
	
	def __init__(self):
		self.flag = False

	def visit(self, tree, sp_cnt=0):
		flag = self.flag
		self.flag = True
		name = tree.__class__.__name__
		function = getattr(self, 'visit'+name)
		function(tree, sp_cnt)
		self.flag = flag
		if (not flag):
			print(";")

	def visitNumber(self, number, sp_cnt):
		print("    "*sp_cnt + str(number.value), end="")

	def visitFunctionDefinition(self, foo, sp_cnt):
		print("    "*sp_cnt + "def " + foo.name + " (" + ", ".join(foo.function.args) + ") {")
		for cmnd in foo.function.body:
			self.visit(cmnd, sp_cnt+1)
			print(";")
		print("    "*sp_cnt+"}", end="")

	def visitConditional(self, conditional, sp_cnt):
		print("    "*sp_cnt + "if (", end="")
		self.visit(conditional.condtion, 0)
		print(") {")
		for x in conditional.if_true:
			self.visit(x, sp_cnt+1)
			print(";")
		if conditional.if_false != None:
			print("    "*sp_cnt + "} else {")
			for x in conditional.if_false:
				self.visit(x, sp_cnt+1)
				print(";")
		else:
			print(conditional.if_false)
		print("    "*sp_cnt+"}", end="")

	def visitPrint(self, prnt, sp_cnt):
		print("    "*sp_cnt + "print(", end="")
		self.visit(prnt.expr, 0)
		print(")", end="")

	def visitRead(self, read, sp_cnt):
		print("    "*sp_cnt + "read(" + read.name + ")", end="")

	def visitFunctionCall(self, foo, sp_cnt):
		self.visit(foo.fun_expr, sp_cnt)
		print("(", end="")
		if len(foo.args):
			for x in foo.args[:-1]:
				self.visit(x, 0)
				print(", ", end="")
			self.visit(foo.args[-1], 0)
		print(")", end="")

	def visitReference(self, reference, sp_cnt):
		print("    "*sp_cnt + reference.name, end="")

	def visitBinaryOperation(self, binary, sp_cnt):
		print("    "*sp_cnt + "(", end="")
		self.visit(binary.lhs, 0)
		print(") " + binary.op + " (", end="")
		self.visit(binary.rhs, 0)
		print(")", end="")

	def visitUnaryOperation(self, unary, sp_cnt):
		print(unary.op + "(", end="")
		self.visit(unary.expr, 0)
		print(")", end="")
