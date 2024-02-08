from utils import *

class Instrucoes: 

	def __init__(self):
		self.instructions = {
			'00000001': self.loadMX,
			'00001001': self.loadMQMX,
			'00100001': self.storMX,
			'00001010': self.loadMQ,
			'00000010': self.loadNMX,
			'00000011': self.loadAMX,
			'00000100': self.loadANMX,
			'00001101': self.jumpMXL,
			'00001110': self.jumpMXR,
			'00001111': self.jumpNNMXL,
			'00010000': self.jumpNNMXR,
			'00000101': self.addMX,
			'00000111': self.addAMX,
			'00000110': self.subMX,
			'00001000': self.subAMX,
			'00001011': self.mulMX,
			'00001100': self.divMX,
			'00010100': self.lsh,
			'00010101': self.rsh,
			'00010010': self.storMXL,
			'00010011': self.storMXR
		}

	def loadMQ(self):
		self.AC = self.MQ

		self.debug(f'  AC <- {binToInt(self.MQ)}')

	def loadMQMX(self):
		self.buscaOperandos()
		self.MQ = self.MBR

		self.debug(f'  MQ <- {binToInt(self.MBR)}')

	def storMX(self):
		endereco = binToInt(self.MAR)

		if (endereco >= len(self.memory)):
			raise Exception(f'O endereço {endereco} não está na memoria!')
		
		self.debug(f'  M({endereco}) <- {binToInt(self.AC)}')

		self.memory[endereco] = self.AC

	def loadMX(self):
		self.buscaOperandos()
		self.AC = self.MBR

		self.debug(f'  AC <- {binToInt(self.AC)}')

	#Load Negative M(X)
	def loadNMX(self):
		self.buscaOperandos()
		self.AC = negativeBin(self.MBR)

		self.debug(f'  AC <- {binToInt(self.AC)}')
		
	#Load Absolute M(X)
	def loadAMX(self):
		self.buscaOperandos()
		self.AC = absoluteBin(self.MBR)

		self.debug(f'  AC <- {binToInt(self.AC)}')

	#Load Absolute Negative M(X)
	def loadANMX(self):
		self.buscaOperandos()
		self.AC = negativeBin(absoluteBin(self.MBR))

		self.debug(f'  AC <- {binToInt(self.AC)}')

	def jumpMXL(self):
		self.IBR = '00000000000000000000'
		self.PC = intToBin(binToInt(self.MAR) - 1, 40)

		if binToInt(self.MAR) >= len(self.memory):
			self.debug('Jumping outside memory')
			return

		self.debug(f'  Jumping to {binToInt(self.MAR)}')

	def jumpMXR(self):
		self.IBR = '00000000000000000000'
		self.PC = self.MAR

		if binToInt(self.PC) >= len(self.memory):
			self.debug('Jumping outside memory')
			return

		self.debug(f'  Jumping to {binToInt(self.MAR)}')

		self.busca()
		self.decodifica()

	#Jump NonNegative M(X) left
	def jumpNNMXL(self):
		if (self.AC[0] == '1'):
			self.debug(f'  Not jumping')
			return

		self.IBR = '00000000000000000000'
		self.PC = intToBin(binToInt(self.MAR) - 1, 40)

		if binToInt(self.MAR) >= len(self.memory):
			self.debug('Jumping outside memory')
			return

		self.debug(f'  Jumping to {binToInt(self.MAR)}')

	#Jump NonNegative M(X) right
	def jumpNNMXR(self):
		if (self.AC[0] == '1'):
			self.debug(f'  Not jumping')
			return

		self.IBR = '00000000000000000000'
		self.PC = self.MAR

		if binToInt(self.PC) >= len(self.memory):
			self.debug('Jumping outside memory')
			return

		self.busca()
		self.decodifica()

		self.debug(f'  Jumping to {binToInt(self.MAR)}')

	def addMX(self):
		self.buscaOperandos()

		self.debug(f'  AC <- {binToInt(self.AC)} + {binToInt(self.MBR)}')
		self.AC = addBin(self.AC, self.MBR)
		self.debug(f'  AC: {binToInt(self.AC)}')

	#Add Absolute M(X)
	def addAMX(self):
		self.buscaOperandos()

		self.debug(f'  AC <- {binToInt(self.AC)} + {binToInt(absoluteBin(self.MBR))}')
		self.AC = addBin(self.AC, absoluteBin(self.MBR))
		self.debug(f'  AC: {binToInt(self.AC)}')

	def subMX(self):
		self.buscaOperandos()

		self.debug(f'  AC <- {binToInt(self.AC)} - {binToInt(self.MBR)}')
		self.AC = subBin(self.AC, self.MBR)
		self.debug(f'  AC: {binToInt(self.AC)}')

	#Sub Absolute M(X)
	def subAMX(self):
		self.buscaOperandos()

		self.debug(f'  AC <- {binToInt(self.AC)} - {binToInt(absoluteBin(self.MBR))}')
		self.AC = subBin(self.AC, absoluteBin(self.MBR))
		self.debug(f'  AC: {binToInt(self.AC)}')

	def mulMX(self):
		self.buscaOperandos()

		resultado = mulBin(self.MQ, self.MBR)

		self.debug(f'  Multiplicando: {binToInt(self.MQ)} * {binToInt(self.MBR)}')
		self.debug(f'  Resultado: {binToInt(resultado)}')
		self.AC = resultado[:40]
		self.MQ = resultado[40:]
		self.debug(f'  AC: {binToInt(self.AC)} MQ: {binToInt(self.MQ)}')

	def divMX(self):
		self.buscaOperandos()

		quociente, resto = divBin(self.AC, self.MBR)

		self.debug(f'  Dividindo: {binToInt(self.AC)} / {binToInt(self.MBR)}')
		self.debug(f'  Quociente: {binToInt(quociente)}, Resto: {binToInt(resto)}')
		self.AC = resto
		self.MQ = quociente

	def lsh(self):
		self.AC = self.AC[1:] + '0'

		self.debug(f'  AC <- AC * 2')

	def rsh(self):
		self.AC = '0' + self.AC[:-1]

		self.debug(f'  AC <- AC / 2')

	def storMXL(self):			
			address = binToInt(self.MAR)
			new_operand = self.AC[-12:]

			self.memory[address] = self.memory[address][0:8] + new_operand + self.memory[address][20:40]

			self.debug(f'  {address}: Pointer changed to {binToInt(new_operand)}')

	def storMXR(self):
			address = binToInt(self.MAR)
			new_operand = self.AC[-12:]

			if address == binToInt(self.PC):
				self.IBR = self.IBR[0:8] + new_operand

			self.memory[address] = self.memory[address][0:28] + new_operand

			self.debug(f'  {address}: Pointer changed to {binToInt(new_operand)}')