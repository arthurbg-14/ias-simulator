from utils import intToBin

def compilar(programa):
    compilado = []

    removerComentarios(programa)

    for linha in programa:
        opcode = encontrarOpcode(linha)

        if not opcode:
            compilado.append(intToBin(int(linha), 20))
            continue

        operando = encontrarOperando(linha)
        compilado.append(opcode + operando)

    return compilado

def removerComentarios(programa):
    for i in range(len(programa)):
        programa[i] = programa[i].split('//')[0]

def encontrarOpcode(linha):
    if linha.startswith('LOAD MQ,M('): return '00001001'
    elif linha.startswith('LOAD MQ'): return '00001010'
    elif linha.startswith('STOR M'): return '00100001'
    elif linha.startswith('STOR OP'): return '00010010'
    elif linha.startswith('LOAD M('): return '00000001'
    elif linha.startswith('LOAD -M('): return '00000010'
    elif linha.startswith('LOAD |M('): return '00000011'
    elif linha.startswith('LOAD -|M('): return '00000100'
    elif linha.startswith('JUMP M('): return '00001101'
    elif linha.startswith('JUMP + M('): return '00001111'
    elif linha.startswith('ADD M('): return '00000101'
    elif linha.startswith('ADD |M('): return '00000111'
    elif linha.startswith('SUB M('): return '00000110'
    elif linha.startswith('SUB |M('): return '00001000'
    elif linha.startswith('MUL M('): return '00001011'
    elif linha.startswith('DIV M('): return '00001100'
    elif linha.startswith('LSH'): return '00010100'
    elif linha.startswith('RSH'): return '00010101'
    elif linha.startswith('EXIT'): return '11111111'

    else: return False

def encontrarOperando(linha):
	l = linha.find('(')
	r = linha.find(')')
	
	if (l == -1 or r == -1): return intToBin(0, 12)

	return intToBin(int(linha[(l + 1):r]), 12)
