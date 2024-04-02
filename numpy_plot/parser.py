import numpy as np
from numpy_plot import dict_bin_operation_fn, dict_una_operation_fn, dict_operation_fn

def check_parenthesis(expr: str):
	parenthesis_count = 0
	for char in expr:
		if char == '(': parenthesis_count += 1
		if char == ')': parenthesis_count -= 1
		if parenthesis_count < 0: return False
	return True

class ParseError(ValueError):
	def __init__(self, message: str):
		super().__init__(message)
		self.message = message

class Parser:
	def __init__(self, expr: str, x: np.ndarray, y: np.ndarray):
		self.x = x
		self.y = y
		self.expr = (
			expr
			# TODO: Do this replaces only once.
			.replace(' ',  '')
			.replace('\n', '')
			.replace('\t', '')
		)
		self.operation, self.children = self.parse_step()
		if not isinstance(self.children, ParseError): 
			self.z = dict_operation_fn[self.operation](*[child for child in self.children])
		else:
			self.z = self.children

	def sub_value(self, expr):
		return Parser(expr, self.x, self.y).z

	def parse_step(self) -> tuple[str, list[np.ndarray] | ParseError]:
		# Errors
		operation, children = self.check_void()
		if isinstance(children, ParseError): return operation, children
		operation, children = self.check_parenthesis()
		if isinstance(children, ParseError): return operation, children
		
		# Base case.
		if   self.expr == 'x':
			return 'id', [self.x]
		elif self.expr == 'y':
			return 'id', [self.y]
		elif self.expr.isnumeric():
			return 'id', [float(self.expr)]
		
		# Parenthesis.
		elif self.expr[0] == '(' and self.expr[-1] == ')' and check_parenthesis(self.expr[1:-1]):
			return 'id', [self.sub_value(self.expr[1:-1])]

		# Parse binary operations.
		operation, children = self.parse_step_binary()
		if operation != None: return operation, children

		# Parse unary operations.
		operation, children = self.parse_step_unary()
		if operation != None: return operation, children
	
		# Final error:
		return None, ParseError('Invalid expression.')

	def check_void(self) -> tuple[str, list[np.ndarray] | ParseError]:
		if self.expr == '':	return None, ParseError('Invalid expression.')
		return None, None
					
	def check_parenthesis(self) -> tuple[str, list[np.ndarray] | ParseError]:
		# TODO: Check this only once.
		parenthesis_count = 0
		for char in self.expr:
			if char == '(': parenthesis_count += 1
			if char == ')': parenthesis_count -= 1
			if parenthesis_count < 0: return None, ParseError('Parenthesis error.')
		if parenthesis_count != 0: return None, ParseError('Parenthesis error.')
		return None, None

	def parse_step_binary(self) -> tuple[str, list[np.ndarray] | ParseError]:
		for operation in dict_bin_operation_fn.keys():
			parenthesis_count = 0
			len_op = len(operation)
			
			for index_char, char in enumerate(self.expr):
				if char == '(': parenthesis_count += 1
				if char == ')': parenthesis_count -= 1
				char = self.expr[index_char : index_char + len_op]
				
				if char == operation and parenthesis_count == 0:
					return operation, [
						self.sub_value(self.expr[:index_char]),
						self.sub_value(self.expr[index_char+len_op:])
					]

		return None, None	

	def parse_step_unary(self) -> tuple[str, list[np.ndarray] | ParseError]:
		for operation in dict_una_operation_fn.keys():
			len_op = len(operation)
			
			is_operation = self.expr[:len_op] == operation
			parenthesis_open = self.expr[len_op] == '('
			parenthesis_close = self.expr[-1] == ')'

			if is_operation and parenthesis_open and parenthesis_close:
				return operation, [self.sub_value(self.expr[len_op + 1 : -1])]

		return None, None

def parse(expr: str, x: np.ndarray, y: np.ndarray) -> np.ndarray | ParseError:
	return Parser(expr, x, y).z
