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
    
    running = False

    def __init__(self, debug=False):
        super().__init__()
        self.isDebug = debug

    def busca(self):
        self.MAR = self.PC
        self.MBR = self.memory[binToInt(self.MAR)]

    def decodifica(self):
        self.IR = self.MBR[0:8]
        self.MAR = self.MBR[9:20]

        if self.IR  != '00001111':
            self.PC = incrementBin(self.PC)

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
        
        for index, linha in enumerate(self.memory):
            if linha[0:8] in self.instructions:
                self.PC = intToBin(index, 20)
                break

    def debug(self, mensagem, end='\n'):
        if (not self.isDebug): return
        print(mensagem, end=end)

    def run(self):
        self.running = True
        
        if self.isDebug:
            print('')
            print(' Execução '.center(40, '='))
            print('')

        while self.running:
            self.busca()
            self.decodifica()
            self.buscaOperandos()
            self.executa()

            if (binToInt(self.PC) >= len(self.memory)):
                self.running = False

        self.display()

    def display(self):
        print('\nExecução do programa finalizada!\n')
        print(' Memoria '.center(40, '='))
        print('')

        for index, linha in enumerate(ias.memory):
            print(str(index) + ':' + (' ' * (7 - len(str(index)))) + linha + ' ' * 3 + '(' + str(binToInt(linha)) + ')')

        print('')
        print(' Registradores '.center(40, '='))
        print('')
        print('AC:    ', ias.AC +  '   (' + str(binToInt(ias.AC)) + ')')
        print('MQ:    ', ias.MQ +  '   (' + str(binToInt(ias.MQ)) + ')')
        print('PC:    ', ias.PC.zfill(20) +  '   (' + str(binToInt(ias.PC)) + ')')
        print('MBR:   ', ias.MBR + '   (' + str(binToInt(ias.MBR)) + ')')
        print('MAR:   ', ias.MAR.zfill(20) + '   (' + str(binToInt(ias.MAR)) + ')')
        print('IR:    ', ias.IR.zfill(20) +  '   (' + str(binToInt(ias.IR)) + ')')

# INICIO
# 
# python3 ias.py <nome do arquivo de entrada> <endereco de inicio das instrucoes>
# --debug para mostrar a execução detalhada do programa
ias = IAS('--debug' in sys.argv)
ias.carga_memoria(sys.argv[1])

if '--compile' in sys.argv: 
    print('')
    print(' Compilado '.center(40, '='))
    print('')
    for l in ias.memory:
        print(l)

ias.run()
