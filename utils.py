def intToBin(number, size):
	return format(number, 'b').zfill(size).replace('-', '1')

def binToInt(binary):
    if binary[0] == '1':
        binary = '-' + binary[1:]
        
    return int(binary, 2)

def incrementBin(binary):
    if binary[-1] == '0':
        return binary[:-1] + '1'
    return incrementBin(binary[:-1]) + '0'

def decrementBin(binary):
    if binary[-1] == '1':
        return binary[:-1] + '0'
    return decrementBin(binary[:-1]) + '1'

def negativeBin(binary):
	if binary[0] == '1':
		return '0' + binary[1:]
	return '1' + binary[1:]

def absoluteBin(binary):
	return '0' + binary[1:]

def invertBin(bin):
    result = ''

    for n in bin:
        if n == '0':
            result += '1'
        else:
            result += '0'

    return result

def addBin(bin1, bin2):
    result = ''
    carry = 0

    if len(bin1) != len(bin2):
        raise Exception('Binarios de tamanho diferente: \n' + bin1 + '\n' + bin2)

    for i in range(len(bin1) - 1, -1, -1):
        r = carry
        r += 1 if bin1[i] == '1' else 0
        r += 1 if bin2[i] == '1' else 0
        result = str(r % 2) + result

        carry = 0 if r < 2 else 1

    if carry != 0:
        result = '1' + result

    return result

def subBin(bin1, bin2):
    result = ''
    borrow = 0

    # Subtrai os números bit a bit
    for i in range(len(bin1) - 1, -1, -1):
        temp = borrow
        temp += 1 if bin1[i] == '1' else 0
        temp -= 1 if bin2[i] == '1' else 0
        result = ('1' if temp % 2 == 1 else '0') + result
        borrow = 0 if temp >= 0 else -1       

    return result

def addBinSignal(num1, num2):
    # Verifica se os números são negativos
    is_num1_negative = num1[0] == '1'
    is_num2_negative = num2[0] == '1'

    # Se ambos os números forem negativos, o resultado será negativo
    if is_num1_negative == is_num2_negative:
        result = addBin(num1[1:], num2[1:])
        signal = '1' if is_num1_negative else '0'
        return signal + result

    # Se apenas um dos números for negativo, subtrai o menor do maior
    elif is_num1_negative != is_num2_negative:
        if binToInt(num1[1:]) > binToInt(num2[1:]):
            return num1[0] + subBin(num1[1:], num2[1:]) 
        else:
            return num2[0] + subBin(num2[1:], num1[1:]) 

def subBinSignal(bin1, bin2):
    return addBinSignal(bin1, negativeBin(bin2))

def mulBin(bin1, bin2):
    return intToBin((binToInt(bin1) * binToInt(bin2)), len(bin1) * 2)

def divBin(bin1, bin2):
	int1 = binToInt(bin1)
	int2 = binToInt(bin2)

	return intToBin(int1 // int2, 20), intToBin(int1 % int2, 20)
