
class GraficoProcedimento(object): 
    def __init__(self, processo, realizado, atrasado, impedimento): 
        self.__processo = processo
        self.__realizado = round(realizado,2)
        self.__atrasado = round(atrasado,2) 
        self.__impedimento = round(impedimento,2)

    def __repr__(self): 
        return "%s" % (self.__processo)

    def get_pontos(self): 
        total = self.__realizado + self.__atrasado + self.__impedimento
        return total

    def get_processo(self):
        processo = self.__processo
        return processo
    
    def get_realizado(self):
        return self.__realizado
    
    def get_atrasado(self):
        return self.__atrasado
    
    def get_impedimento(self):
        return self.__impedimento

    def addRealizado(self, pontos):
        self.__realizado += round(pontos,2)
        
    def addAtrasado(self, pontos):
        self.__atrasado += round(pontos,2)
    
    def addImpedimento(self, pontos):
        self.__impedimento += round(pontos,2)

class GraficoDemanda(object): 
    def __init__(self, processo, pontos, cor): 
        self.__processo = processo
        self.__pontos = round(pontos,2)
        self.__cor = cor

    def __repr__(self): 
        return "%s" % (self.__processo)

    def get_pontos(self): 
        return self.__pontos

    def get_processo(self):
        return self.__processo
    
    def get_cor(self):
        return self.__cor

    def addPontos(self, pontos):
        self.__pontos += round(pontos,2)
    

class GraficoCC(object): 
    def __init__(self, cc, pontos): 
        self.__cc = cc
        self.__pontos = round(pontos,2)

    def __repr__(self): 
        return "%s" % (self.__cc)

    def get_pontos(self): 
        return self.__pontos

    def get_cc(self):
        return self.__cc
    
    def addPontos(self, pontos):
        self.__pontos += round(pontos,2)
        