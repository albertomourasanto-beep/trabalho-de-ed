from array_dinamico import ArrayDinamico
def selectionsort(array, callback=None):
    """
    Ordena uma cópia do ArrayDinamico recebido usando Selection Sort.

    Parâmetros
    ----------
    array    : ArrayDinamico  — array original (não é modificado)
    callback : callable | None
            Se fornecido, será chamado como callback(i, total)
            a cada passo, onde i vai de 1 até total (n-1).
            Usado para atualizar barras de progresso.

    Retorno
    -------
    novo : ArrayDinamico — cópia ordenada em ordem alfabética.
    """
    n = array.getQuantidade()
    novo = ArrayDinamico(max(n,2))
    
    for i in range(n):
        novo.inserir(array.getValue(i))
        
    for i in range(n):
        indice=i
        for j in range(i+1,n):
            if novo.getValue(j).lower()<novo.getValue(indice).lower():
                indice=j
        if indice!=i:
            chave=novo.getValue(indice)
            novo.setValue(indice,novo.getValue(i))
            novo.setValue(i,chave)
        if callback:
            callback(i, n-1)
    
    return novo