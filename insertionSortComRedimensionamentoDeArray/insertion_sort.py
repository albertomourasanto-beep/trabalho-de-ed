from array_dinamico import ArrayDinamico
def insertionSort(array):
    novo=ArrayDinamico(array.getQuantidade())
    n=array.getQuantidade()
    for i in range(n):
        novo.inserir(array.getValue(i))
    for i in range(1,n):
        chave = novo.getValue(i)
        j=i-1
        while j >= 0 and novo.getValue(j).lower() > chave.lower():
            novo.setValue(j+1,novo.getValue(j))
            j-=1
        novo.setValue(j+1,chave)
    return novo
