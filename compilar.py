from utils import intToBin

def compilar(programa):
	compilado = []

	for linha in programa:
		if linha == '\n':
			programa.remove(linha)

	for i in range(len(programa)):
		if '//' in programa[i]:
			comment = programa[i].find('//')
			programa[i] = programa[i][:comment]
		programa[i] = programa[i].replace('\n', '').strip()

	i = 0
	while i < len(programa):
		linha = compilarLinha(programa[i])

		if len(linha) == 40:
			compilado.append(linha)
			i += 1
			continue

		if (i + 1) >= len(programa):
			compilado.append(linha + '00000000000000000000')
			i += 1
			continue
			
		linha2 = compilarLinha(programa[i + 1])
		compilado.append(linha + linha2)
		i += 2

	return compilado

def compilarLinha(linha):
	opcode = encontrarOpcode(linha)

	if not opcode:
		return intToBin(int(linha), 40)

	operando = encontrarOperando(linha)
	return opcode + operando

def encontrarOpcode(linha):

	if linha.startswith('LOAD MQ,M('): return '00001001'
	elif linha.startswith('LOAD MQ'): return '00001010'
	elif linha.startswith('STOR M('): 
		if linha.endswith(',8:19)'): return '00010010'
		if linha.endswith(',28:39)'): return '00010011'
		return '00100001'
	elif linha.startswith('LOAD M('): return '00000001'
	elif linha.startswith('LOAD –M('): return '00000010'
	elif linha.startswith('LOAD |M('): return '00000011'
	elif linha.startswith('LOAD –|M('): return '00000100'
	elif linha.startswith('JUMP M('):
		if linha.endswith(',0:19)'): return '00001101'
		elif linha.endswith(',20:39)'): return '00001110'
	elif linha.startswith('JUMP + M('):
		if linha.endswith(',0:19)'): return '00001111'
		elif linha.endswith(',20:39)'): return '00010000'
	elif linha.startswith('ADD M('): return '00000101'
	elif linha.startswith('ADD |M('): return '00000111'
	elif linha.startswith('SUB M('): return '00000110'
	elif linha.startswith('SUB |M('): return '00001000'
	elif linha.startswith('MUL M('): return '00001011'
	elif linha.startswith('DIV M('): return '00001100'
	elif linha.startswith('LSH'): return '00010100'
	elif linha.startswith('RSH'): return '00010101'
	else: return False

def encontrarOperando(linha):
	l = linha.find('(')
	r = linha.find(')')
	
	if (l == -1 or r == -1): return intToBin(0, 12)

	operando = linha[(l + 1):r].split(',')[0]

	return intToBin(int(operando), 12)
