def intToBin(number, size):
	return format(number, 'b').zfill(size).replace('-', '1')

def binToInt(binary):
	if binary[0] == '1':
		binary = '-' + binary[1:]
		
	return int(binary, 2)

def negativeBin(binary):
	if binary[0] == '1':
		return '0' + binary[1:]
	return '1' + binary[1:]

def absoluteBin(binary):
	return '0' + binary[1:]

def addBin(bin1, bin2):	
  return intToBin((binToInt(bin1) + binToInt(bin2)), len(bin1))

def subBin(bin1, bin2):
  return addBin(bin1, negativeBin(bin2))

def mulBin(bin1, bin2):
  return intToBin((binToInt(bin1) * binToInt(bin2)), len(bin1) * 2)

def divBin(bin1, bin2):
	int1 = binToInt(bin1)
	int2 = binToInt(bin2)

	return intToBin(int1 // int2, 40), intToBin(int1 % int2, 40)