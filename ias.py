from instrucoes import Instrucoes
from compilar import compilar
from utils import *
import sys

class IAS(Instrucoes):

	memory = []
	
	AC = '0000000000000000000000000000000000000000'
	MQ = '0000000000000000000000000000000000000000'
	PC = '0000000000000000000000000000000000000000'
	MBR = '0000000000000000000000000000000000000000'
	MAR = '0000000000000000000000000000000000000000'
	IR = '00000000000000000000'
	IBR = '00000000000000000000'

	def __init__(self, PC, debug=False):
		super().__init__()
		self.PC = PC
		self.isDebug = debug

	def busca(self):
		self.MAR = self.PC
		self.MBR = self.memory[binToInt(self.MAR)]

	def decodifica(self):
		if self.IBR != '00000000000000000000':
			self.IR = self.IBR[0:8]
			self.MAR = self.IBR[9:20]
			self.IBR = '00000000000000000000'
		else:
			self.IR = self.MBR[0:8]
			self.MAR = self.MBR[9:20]
			self.IBR = self.MBR[20:40]

	def buscaOperandos(self):
		self.MBR = self.memory[binToInt(self.MAR)]

	def executa(self):
		self.instructions[self.IR]()
		if self.IBR != '00000000000000000000':
			self.decodifica()
			self.executa()

	def carga_memoria(self, nome_arquivo):
			with open(nome_arquivo, "r") as fin:
					programa = fin.readlines()

			is_compiled = not any(('M' in linha or 'S' in linha) for linha in programa)
			
			if not is_compiled:
				programa = compilar(programa)

			self.memory = [linha.replace("\n", "") for linha in programa]

	def loadProgram(self):
		for line in programa:
			self.memory.append(line)

	def debug(self, mensagem):
		if (not self.isDebug): return
		print(mensagem)

	def executePC(self):
		self.busca()
		self.decodifica()
		self.executa()

		self.PC = intToBin(binToInt(self.PC) + 1, 40)

		if (binToInt(self.PC) >= len(self.memory)):
			print('Execução do programa finalizada!')

			print('Memoria:')
			for index, linha in enumerate(self.memory):
				print(str(index) + ': ' + linha, '(' + str(binToInt(linha)) + ')')
			print('')
			print('AC: ', self.AC, '(' + str(binToInt(self.AC)) + ')')
			print('MQ: ', self.MQ, '(' + str(binToInt(self.MQ)) + ')')
			print('PC: ', self.PC, '(' + str(binToInt(self.PC)) + ')')
			print('MBR: ', self.MBR, '(' + str(binToInt(self.MBR)) + ')')
			print('MAR: ', self.MAR, '(' + str(binToInt(self.MAR)) + ')')
			print('IR: ', self.IR, '(' + str(binToInt(self.IR)) + ')')
			return

		self.executePC()

# INICIO
# 
# python3 ias.py <nome do arquivo de entrada> <endereco de inicio das instrucoes>
# --debug para mostrar a execução detalhada do programa
ias = IAS(intToBin(int(sys.argv[2]), 20), '--debug' in sys.argv)
ias.carga_memoria(sys.argv[1])
ias.executePC()