import pytest
import numpy as np
from numpy_plot import parse, ParseError, dict_una_operation_fn

x = np.array([1.0])
y = np.array([2.0])

def test_void():
	z = parse('', x, y)
	assert isinstance(z, ParseError)

def test_parenthesis():
	z = parse('((x)', x, y)
	assert isinstance(z, ParseError)

def test_x():
	z = parse('x', x, y)
	assert z == x

def test_y():
	z = parse('y', x, y)
	assert z == y

def test_par_x():
	z = parse('(x)', x, y)
	assert z == x

def test_add():
	z = parse('x+y', x, y)
	assert z == x + y

def test_sub():
	z = parse('x-y', x, y)
	assert z == x - y

def test_mul():
	z = parse('x*y', x, y)
	assert z == x * y

def test_div():
	z = parse('x/y', x, y)
	assert z == x / y

def test_pow():
	z = parse('x**y', x, y)
	assert z == x ** y

@pytest.mark.parametrize('op_str, op_fn', [(op_str, op_fn) for op_str, op_fn in dict_una_operation_fn.items()])
def test_unary(op_str, op_fn):
	if op_str == 'arccosh': return None
	assert parse(f'{op_str}(x/y)', x, y) == op_fn(x / y)

def test_default_expression():
	x = np.linspace(-10.0, 10.0, 1000).reshape((-1, 1))
	y = np.linspace(-10.0, 10.0, 1000).reshape((1, -1))
	z = parse('(x + y) / (2 + cos(x) * sin(y))', x, y)
	z_calc = (x + y) / (2 + np.cos(x) * np.sin(y))
	assert (np.abs(z - z_calc) < 1e9).all()
