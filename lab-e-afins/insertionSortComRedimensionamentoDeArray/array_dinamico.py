class ArrayDinamico:#classe designada para ser o ArrayDinamico
    def __init__(self,tamanhoInicial=2):
        self._array = [None]*tamanhoInicial
        self._quantidade = 0#quantidade de espaços preenchidos
        self._tamanho = tamanhoInicial#variavel usada para designar o tamanho real do Array
    def inserir(self,valor):
        if self._quantidade == self._tamanho:
            aux=[None]*(self._tamanho*2)
            for i,n in enumerate(self._array):
                aux[i]=n
            self._array=aux
            self._tamanho*=2
        self._array[self._quantidade] = valor
        self._quantidade +=1
    def removerPorNome(self,valor):
        aux=None
        for n,i in enumerate(self._array):
            if i is not None and valor.lower()==i.lower():
                aux=n
                break
        if aux is not None:
            straux=input(f"Deseja realmente apagar esse elemento?Digite sim ou não.\n{self._array[aux]}\n")
            if straux.lower()=="sim":
                i=0
                vetaux=[None]*self._tamanho
                for n in range(self._quantidade):
                    if n==aux:
                        continue
                    vetaux[i]=self._array[n]
                    i+=1
                self._quantidade-=1
                self._array=vetaux
                if self._quantidade<(self._tamanho/4):
                    self._tamanho=self._tamanho//2
                    self._array=self._array[:self._tamanho]
            else:
                print("Ok!Elemeto não apagado.")
        else:
            print("Nome não encontrado")
    def listar(self):
        i=0
        print("[",end="")
        while i<self._quantidade:
            if i>0:
                print(",",end='')
            print(f"\"{self._array[i]}\"", end='')
            i+=1
        print("]",end="")
    def setValue(self,indice,valor):
        if 0 <=indice < self._quantidade:
            self._array[indice]=valor
    def getValue(self,indice):
        indice=int(indice)
        try:
            if self._array[indice] is not None:
                return self._array[indice]
            else:
                print("Não existe esse indice, por favor, tente novamente quando houver mais nomes, ou escreva um indice válido.")
        except:
            print("Não existe esse indice, por favor, tente novamente quando houver mais nomes, ou escreva um indice válido.")
    def getTamanho(self):
        return self._tamanho
    def getQuantidade(self):
        return self._quantidade