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
			'00001101': self.jumpMX,
			'00001111': self.jumpNNMX,
			'00000101': self.addMX,
			'00000111': self.addAMX,
			'00000110': self.subMX,
			'00001000': self.subAMX,
			'00001011': self.mulMX,
			'00001100': self.divMX,
			'00010100': self.lsh,
			'00010101': self.rsh,
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

	def jumpMX(self):
		self.PC = intToBin(binToInt(self.MAR) - 1, 20)

		self.debug(f'  Jumping to {binToInt(self.MAR)}')

	#Jump NonNegative M(X)
	def jumpNNMX(self):
		if (self.AC[0] == '1'):
			self.debug(f'  Not jumping')
			return

		self.PC = intToBin(binToInt(self.MAR) - 1, 20)

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
		self.AC = resultado[:20]
		self.MQ = resultado[20:]
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

	def rsh(self):
		self.AC = '0' + self.AC[:-1]