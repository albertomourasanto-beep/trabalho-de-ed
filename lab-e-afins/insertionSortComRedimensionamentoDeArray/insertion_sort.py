from array_dinamico import ArrayDinamico


def insertionSort(array, callback=None):
    """
    Ordena uma cópia do ArrayDinamico recebido usando Insertion Sort.

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
    novo = ArrayDinamico(max(n, 2))

    for i in range(n):
        novo.inserir(array.getValue(i))

    for i in range(1, n):
        chave = novo.getValue(i)
        j = i - 1
        while j >= 0 and novo.getValue(j).lower() > chave.lower():
            novo.setValue(j + 1, novo.getValue(j))
            j -= 1
        novo.setValue(j + 1, chave)

        if callback:
            callback(i, n - 1)   # i de 1 até n-1  →  0 % … 100 %

    return novo