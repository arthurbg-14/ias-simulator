from instrucoes import Instrucoes
from compilar import compilar
from utils import *
import sys

class IAS(Instrucoes):

	memory = []
	
	AC = '00000000000000000000'
	MQ = '00000000000000000000'
	PC = '00000000000000000000'
	MBR = '00000000000000000000'
	MAR = '00000000000000000000'
	IR = '00000000000000000000'

	def __init__(self, PC, debug=False):
		super().__init__()
		self.PC = PC
		self.isDebug = debug

	def busca(self):
		self.MAR = self.PC
		self.MBR = self.memory[binToInt(self.MAR)]

	def decodifica(self):
		self.IR = self.MBR[0:8]
		self.MAR = self.MBR[9:20]

	def buscaOperandos(self):
		self.MBR = self.memory[binToInt(self.MAR)]

	def executa(self):		
		self.instructions[self.IR]()

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

		self.PC = intToBin(binToInt(self.PC) + 1, 20)

		if (binToInt(self.PC) >= len(self.memory)):
			print('Execução do programa finalizada!')

			print('Memoria:')
			for index, linha in enumerate(ias.memory):
				print(str(index) + ': ' + linha, '(' + str(binToInt(linha)) + ')')
			print('')
			print('AC: ', ias.AC, '(' + str(binToInt(ias.AC)) + ')')
			print('MQ: ', ias.MQ, '(' + str(binToInt(ias.MQ)) + ')')
			print('PC: ', ias.PC, '(' + str(binToInt(ias.PC)) + ')')
			print('MBR: ', ias.MBR, '(' + str(binToInt(ias.MBR)) + ')')
			print('MAR: ', ias.MAR, '(' + str(binToInt(ias.MAR)) + ')')
			print('IR: ', ias.IR, '(' + str(binToInt(ias.IR)) + ')')
			return

		self.executePC()

# INICIO
# 
# python3 ias.py <nome do arquivo de entrada> <endereco de inicio das instrucoes>
# --debug para mostrar a execução detalhada do programa
ias = IAS(intToBin(int(sys.argv[2]), 20), '--debug' in sys.argv)
ias.carga_memoria(sys.argv[1])
ias.executePC()