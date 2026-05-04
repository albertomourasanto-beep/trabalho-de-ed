from array_dinamico import ArrayDinamico
from carregar_arquivo import carregarArquivo
from insertion_sort import insertionSort
def loop_principal():
    arrayPrincipal=ArrayDinamico()
    arrayOrdenado=0
    while True:
        print("=" * 40)
        print("  SISTEMA DE ORDENACAO — GRUPO 8")
        print("  Array com Redimensionamento")
        print("=" * 40)
        print("1. Carregar dados de arquivo")
        print("2. Executar Insertion Sort")
        print("3. Listar dados originais")
        print("4. Listar dados ordenados")
        print("5. Informacoes estatisticas")
        print("0. Sair")
        print("-" * 40)
        n=int(input("Digite que opção você deseja utilizar:"))
        match n:
            case 1:
                caminho = input("Digite o caminho do arquivo:\n")
                carregarArquivo(caminho, arrayPrincipal)
            case 2:
                if arrayPrincipal.getQuantidade() == 0:
                    print("Carregue dados primeiro! (opção 1)")
                else:
                    arrayOrdenado = insertionSort(arrayPrincipal)
                    print("Ordenação concluída!")
            case 3:
                if arrayPrincipal.getQuantidade() == 0:
                    print("Nenhum dado carregado.")
                else:
                    arrayPrincipal.listar()
            case 4:
                if arrayOrdenado is None:
                    print("Execute o Insertion Sort primeiro! (opção 2)")
                else:
                    arrayOrdenado.listar()
            case 5:
                print(f"Total de nomes: {arrayPrincipal.getQuantidade()}")
                print(f"Capacidade do array: {arrayPrincipal.getTamanho()}")
            case 0:
                print("Encerrando... Até logo!")
                break
            case _:
                print("Opção inválida!")
loop_principal()