from numpy import (
	sin, 
	cos, 
	tan, 
	
	arcsin, 
	arccos, 
	arctan, 
	
	sinh,
	cosh,
	tanh,
	
	arcsinh,
	arccosh,
	arctanh,
	
	round,
	floor,
	ceil,
	trunc,
	cumsum,

	exp,
	log,
	log10,
	log2,

	max,
	min,

	sqrt,
	abs
)

dict_bin_operation_fn = {
	'+'			: lambda z_1, z_2 : z_1 + z_2,
	'-'			: lambda z_1, z_2 : z_1 - z_2,
	'*'			: lambda z_1, z_2 : z_1 * z_2,
	'/'			: lambda z_1, z_2 : z_1 / z_2,
	'**'		: lambda z_1, z_2 : z_1 ** z_2,
}

dict_una_operation_fn = {
	'id'		: lambda x : x,

	'sin' 		: sin, 
	'cos' 		: cos, 
	'tan' 		: tan, 
	
	'arcsin' 	: arcsin, 
	'arccos' 	: arccos, 
	'arctan' 	: arctan, 
	
	'sinh' 		: sinh,
	'cosh' 		: cosh,
	'tanh' 		: tanh,
	
	'arcsinh' 	: arcsinh,
	'arccosh' 	: arccosh,
	'arctanh' 	: arctanh,
	
	'round' 	: round,
	'floor' 	: floor,
	'ceil' 		: ceil,
	'trunc' 	: trunc,
	'cumsum' 	: cumsum,

	'exp' 		: exp,
	'log' 		: log,
	'log10' 	: log10,
	'log2' 		: log2,

	'max' 		: max,
	'min' 		: min,
	
	'sqrt' 		: sqrt,
	'abs' 		: abs
}

dict_operation_fn = dict_bin_operation_fn | dict_una_operation_fn
