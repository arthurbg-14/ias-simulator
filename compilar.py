from utils import intToBin, binToInt
import math

def compilar(programa):
	compilado = []
	labels = {}

	programa = removerComentarios(programa)
	programa = removerEspacos(programa)

	compiled_address = 0

	#save labels address
	for address, linha in enumerate(programa):
		if ':' in  linha:
			i = linha.find(':')
			labels[linha[:i]] = compiled_address
			programa[address] = linha[i + 1:]
			if programa[address].strip('-').isnumeric():
				labels[linha[:i]] = '$' + str(labels[linha[:i]])
			
		isInstruction = not programa[address].isnumeric()

		if (isInstruction):
			compiled_address += 0.5
		else:
			compiled_address += 1
	
	#substitui labels pelo endereço
	for address, linha in enumerate(programa):
		l = linha.find('(')
		r = linha.find(')')
		
		if (l == -1 or r == -1): continue
	
		operando = linha[(l + 1):r].split(',')[0]

		if not operando.isnumeric():
			labelAddress = str(labels[operando])
			operando = str(math.floor(float(labelAddress.replace('$', ''))))
			if not '$' in labelAddress:
				if float(labelAddress).is_integer():
					operando += ',L'
				else:
					operando += ',R'
				
			programa[address] = linha[:l + 1] + operando + linha[r]
	
	print('programa: ')
	for l in programa:
		print(l)

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

	for index, linha in enumerate(compilado):
		a, b, c, d = hex(binToInt(linha[0:8]))[2:].zfill(2), hex(binToInt(linha[9:20]))[2:].zfill(3), hex(binToInt(linha[21:28]))[2:].zfill(2), hex(binToInt(linha[29:40]))[2:].zfill(3)

		print(hex(index + 1)[2:].zfill(3), a, b, c, d)

	return compilado

def removerEspacos(programa):
	semEspacos = []
	
	for linha in programa:
		if linha != '\n' and linha != '':
			semEspacos.append(linha)

	return semEspacos

def removerComentarios(programa):
	semComentarios = []

	for linha in programa:
		if '//' in linha:
			comment = linha.find('//')
			linha = linha[:comment]
		semComentarios.append(linha.replace('\n', '').strip())

	return semComentarios

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
		if linha.endswith(',L)'): return '00010010'
		if linha.endswith(',R)'): return '00010011'
		return '00100001'
	elif linha.startswith('LOAD M('): return '00000001'
	elif linha.startswith('LOAD –M('): return '00000010'
	elif linha.startswith('LOAD |M('): return '00000011'
	elif linha.startswith('LOAD –|M('): return '00000100'
	elif linha.startswith('JUMP M('):
		if linha.endswith(',L)'): return '00001101'
		elif linha.endswith(',R)'): return '00001110'
		return 'JUMP M('
	elif linha.startswith('JUMP + M('):
		if linha.endswith(',L)'): return '00001111'
		elif linha.endswith(',R)'): return '00010000'
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
