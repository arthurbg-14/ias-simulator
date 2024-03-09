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
            '00010010': self.storOPX,
            '11111111': self.exit
        }
    
    def exit(self):
        self.running = False

    def loadMQ(self):
        self.AC = self.MQ

        self.debug(f'{binToInt(self.PC)}:  AC <- {binToInt(self.MQ)}')

    def loadMQMX(self):
        self.MQ = self.MBR

        self.debug(f'{binToInt(self.PC)}:  MQ <- {binToInt(self.MBR)}')

    def storMX(self):
        endereco = binToInt(self.MAR)

        self.debug(f'{binToInt(self.PC)}:  M({endereco}) <- {binToInt(self.AC)}')

        self.memory[endereco] = self.AC

    def loadMX(self):
        self.AC = self.MBR

        self.debug(f'{binToInt(self.PC)}:  AC <- {binToInt(self.AC)}')

#Load Negative M(X)
    def loadNMX(self):
        self.AC = negativeBin(self.MBR)

        self.debug(f'{binToInt(self.PC)}:  AC <- {binToInt(self.AC)}')
        
#Load Absolute M(X)
    def loadAMX(self):
        self.AC = absoluteBin(self.MBR)

        self.debug(f'{binToInt(self.PC)}:  AC <- {binToInt(self.AC)}')

#Load Absolute Negative M(X)
    def loadANMX(self):
        self.AC = negativeBin(absoluteBin(self.MBR))

        self.debug(f'{binToInt(self.PC)}:  AC <- {binToInt(self.AC)}')

    def jumpMX(self):
        self.PC = self.MAR
        self.debug(f'{binToInt(self.PC)}:  Salto para {binToInt(self.MAR)}')

#Jump NonNegative M(X)
    def jumpNNMX(self):
        if (self.AC[0] == '1' and binToInt(self.AC) != 0):
            self.PC = incrementBin(self.PC)
            self.debug(f'{binToInt(self.PC)}:  Não saltou')
        else:
            self.PC = self.MAR
            self.debug(f'{binToInt(self.PC)}:  Salto para {binToInt(self.MAR)}')

    def addMX(self):
        self.debug(f'{binToInt(self.PC)}:  AC <- ({binToInt(self.AC)} + {binToInt(self.MBR)} = ', end='')
        self.AC = addBinSignal(self.AC, self.MBR)
        self.debug(f'{binToInt(self.AC)})')

#Add Absolute M(X)
    def addAMX(self):
        self.debug(f'{binToInt(self.PC)}:  AC <- ({binToInt(self.AC)} + {binToInt(absoluteBin(self.MBR))} = ', end='')
        self.AC = addBinSignal(self.AC, absoluteBin(self.MBR))
        self.debug(f'{binToInt(self.AC)})')

    def subMX(self):
        self.debug(f'{binToInt(self.PC)}:  AC <- ({binToInt(self.AC)} - {binToInt(self.MBR)} = ', end='')
        self.AC = subBinSignal(self.AC, self.MBR)
        self.debug(f'{binToInt(self.AC)})')

#Sub Absolute M(X)
    def subAMX(self):
        self.debug(f'{binToInt(self.PC)}:  AC <- ({binToInt(self.AC)} - {binToInt(absoluteBin(self.MBR))} = ', end='')
        self.AC = subBinSignal(self.AC, absoluteBin(self.MBR))
        self.debug(f'{binToInt(self.AC)})')

    def mulMX(self):
        self.debug(f'{binToInt(self.PC)}:  Multiplicando: {binToInt(self.MQ)} * {binToInt(self.MBR)}', end='')

        resultado = mulBin(self.MQ, self.MBR)

        self.debug(f' Resultado: {binToInt(resultado)}')
        self.AC = resultado[:20]
        self.MQ = resultado[20:]

    def divMX(self):
        quociente, resto = divBin(self.AC, self.MBR)

        self.debug(f'{binToInt(self.PC)}:  Dividindo: {binToInt(self.AC)} / {binToInt(self.MBR)}', end='')
        self.debug(f' Quociente: {binToInt(quociente)}, Resto: {binToInt(resto)}')
        self.AC = resto
        self.MQ = quociente

    def lsh(self):
        self.AC = self.AC[1:] + '0'

    def rsh(self):
        self.AC = '0' + self.AC[:-1]

    def storOPX(self):
        endereco = binToInt(self.MAR)

        self.debug(f'{binToInt(self.PC)}:  OP({endereco}) <- {binToInt(self.AC)}')

        self.memory[endereco] = self.memory[endereco][:8] + self.AC[-12:]

