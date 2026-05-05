def carregarArquivo(caminho,array):
    try:
        with open(caminho , "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    array.inserir(linha)
            print(f"Arqivo com {array.getQuantidade()} palavras carregado com sucesso")
            return array
    except FileNotFoundError:
        print("Arquivo não encontrado, se ele existe, tente usar o caminho absoluto dele!")