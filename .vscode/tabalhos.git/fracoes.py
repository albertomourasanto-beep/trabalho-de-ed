from math import gcd,lcm
def insirafracao():#função criada para a inserção de frações no código
  while True:      
    n=input("digite sua fracao")
    n=n.strip().replace(" ","").split("/")
    x,y=n
    x=int(x)
    y=int(y)
    if y==0: continue
    fracaonovinha=Fraction(x,y)
    return fracaonovinha
def multiplicaca_cruzada(fraction1,fraction2):
  result1=fraction1._numerador*fraction2._denominador
  result2=fraction2._numerador*fraction1._denominador
  return result1,result2  

def igualando_denominador(fraction1,fraction2):#função utilizada para deixar as frações no ponto de somarem ou subtrairem
  mmc=lcm(fraction1._denominador,fraction2._denominador)
  den=mmc
  num1=fraction1._numerador*(mmc//fraction1._denominador)
  num2=fraction2._numerador*(mmc//fraction2._denominador)
  return num1,num2,den

class Fraction:
    def __init__(self,numerador,denominador): #construtor 
      self._numerador = numerador
      self._denominador = denominador
      self.simplicaFracao()

    @property
    def valorNumDen(self): #funçao usada para obter o valor
      return self._numerador, self._denominador
    
    def __eq__(self, value): #metodo de igualdade para saber se as frações sao iguais(simplificadas tbm entram na verificação)
      comp1,comp2=multiplicaca_cruzada(self,value)
      return comp1==comp2
    
    def __ne__(self, value):
      comp1,comp2=multiplicaca_cruzada(self,value)
      return comp1!=comp2
    
    def __ge__(self, value):
      comp1,comp2=multiplicaca_cruzada(self,value)
      return comp1>=comp2
    
    def __gt__(self, value):
      comp1,comp2=multiplicaca_cruzada(self,value)
      return comp1>comp2
    
    def __le__(self, value):
      comp1,comp2=multiplicaca_cruzada(self,value)
      return comp1<=comp2
    
    def __lt__(self, value):
      comp1,comp2=multiplicaca_cruzada(self,value)
      return comp1<comp2
    
    def __add__(self, value): #tentativa de criação de uma função que retorne a soma entre duas frações
        num1,num2,den=igualando_denominador(self,value)
        numsum=num1+num2
        minhaFracaonova=Fraction(numsum,den)
        return minhaFracaonova
    
    def __sub__(self, value):#subtração
        num1,num2,den=igualando_denominador(self,value)
        numsub=num1-num2
        minhaFracaonova=Fraction(numsub,den)
        return minhaFracaonova
    
    def __mul__(self, value):#multiplicação
      nummul=self._numerador*value._numerador
      denmul=self._denominador*value._denominador
      minhafracaonova=Fraction(nummul,denmul)
      return minhafracaonova
    
    def __truediv__(self, value):
      numdiv,dendiv=multiplicaca_cruzada(self,value)
      minhafracaonova=Fraction(numdiv,dendiv)
      return minhafracaonova
    
    def __str__(self):#definindo o retorno da função
      if self._numerador%self._denominador==0:
        return (f"{self._numerador//self._denominador}")
      return(f"{self._numerador}/{self._denominador}")
    
    def mudarNumDen(self,novo_num,novo_den): #funçao usada para alterar o valor
        if novo_den == 0:
          print("Denominador zero não é aceitável.")
          return
        fracao_criada = Fraction(novo_num,novo_den)
        if self == fracao_criada:
          print("Fração já existente.")
        else:
          self._numerador = novo_num
          self._denominador = novo_den

    def simplicaFracao(self):
      mdc = gcd(self._numerador, self._denominador)
      self._numerador//=mdc
      self._denominador//=mdc

def menu():
 while True:
  print("1- Adição")
  print("2- Subtração")
  print("3- Multiplicação")
  print("4- Divisão")
  print("5- Encerrar o programa")
  op = int(input("Escolha a operação desejada: "))
  match op :
    case 1 :
      x=insirafracao()
      y=insirafracao()
      print(f"{x+y}")

    case 5:
      break
menu()