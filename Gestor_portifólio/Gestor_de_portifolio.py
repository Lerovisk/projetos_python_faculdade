import json

def salvar(lista_cadastros):
    try:
        with open("livros.json", 'w', encoding='utf-8') as arquivo:
            json.dump(lista_cadastros, arquivo, ensure_ascii=False, indent=4)
            print("Lista salva com sucesso!")
    except IOError:
        print("Erro ao salvar o arquivo.")

def processar():
    try:
        with open("livros.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def procurar_livro(livro_procurado, lista_cadastros):
    for livro in lista_cadastros:
        if livro["nome"].upper() == livro_procurado.upper():
            return livro
    return None


def adicionar_livro(lista_cadastros):
    try:
        quantidade = int(input("Digite a quantidade de livros que deseja adicionar: "))
        if quantidade <= 0:
            print("Inválido.")
            return False
        else:
            for i in range(quantidade):
                nome_input = input(f"Nome do {i + 1}o livro: ").strip()
                if not nome_input:
                    print("Nome não pode ser vazio. Livro ignorado.")
                    continue
                autor_input = input("Autor: ")
                resumo_input = input("Resumo: ")
                concluido_input = input("Concluído (S/N): ").upper()
                if concluido_input == "S":
                    concluido_input = True
                else:
                    concluido_input = False

                cadastro_livros = {
                    "nome": nome_input,
                    "autor": autor_input,
                    "resumo": resumo_input,
                    "concluido": concluido_input,
                    "historico": []
                }
                lista_cadastros.append(cadastro_livros)  # Adicionamos um novo dicionário à lista de livros
                print(f"Livro {nome_input} adicionado\n")
                salvar(lista_cadastros)
    except ValueError:  # Se o usuário digitar um string ou der Enter vazio e não digitar um número, ele vai cair aqui:
        print("ERRO: Por favor, digite apenas números inteiros.")
        return False


def about():
    print("- - - Lista dos livros favoritos de Leticia Messias - - -")


def alteracao(livro, alter):
    mudar = alter
    backup = (livro["nome"], livro["autor"], livro["resumo"], livro["concluido"])  # Tupla (imutavel)
    livro["historico"].append(backup)  # A lista historico recebe o que entrar na tupla

    if mudar == "Nome":
        novo_nome = input("Novo nome: ").strip()
        if not novo_nome:
            print("Nome inválido, nenhuma alteração feita.")
        else:
            livro["nome"] = novo_nome

    elif mudar == "Autor":
        livro["autor"] = input("Novo autor: ")

    elif mudar == "Resumo":
        livro["resumo"] = input("Novo resumo: ")

    elif mudar == "Status":
        status = input("Digite 'S' para concluído ou 'N' para não concluído: ").upper()
        if status == "S":
            livro["concluido"] = True
        else:
            livro["concluido"] = False
    print("\nLivro atualizado com sucesso!")

def deletar(lista_cadastros):
    livro_procurado = input("Digite o nome do livro que deseja remover: ")
    livro = procurar_livro(livro_procurado, lista_cadastros)
    if livro is None:
        print("Erro: Livro não encontrado.")
    else:
        try:
            lista_cadastros.remove(livro)
            print("Livro removido!")
            salvar(lista_cadastros)
        except ValueError:
            print("Erro: Livro não encontrado.")


def lista(lista_cadastros):
    print("\n-----LISTA DOS MEUS LIVROS FAVORITOS-----")
    for livro in lista_cadastros:
        print(f"\nLivro: {livro['nome']}")
        print(f"Autor: {livro['autor']}")
        print(f"Resumo: {livro['resumo']}")
        print(f"Concluido: {'Sim' if livro['concluido'] else 'Não'}")
        # Fiz esse if para que o historico seja aprensentado de forma organizada
        if livro["historico"]:
            print("Histórico de alterações")
            for i, versao in enumerate(livro["historico"]):
                nome, autor, resumo, status = versao
                print(f"  VERSÃO {i + 1}:")
                print(f"        Nome:  {nome}")
                print(f"        Autor: {autor}")
                print(f"        Resumo: {resumo}")
                print(f"        Concluído: {'Sim' if status else 'Não'}")
            print(f"  VERSÃO ATUAL:")
            print(f"        Nome: {livro['nome']}")
            print(f"        Autor: {livro['autor']}")
            print(f"        Resumo: {livro['resumo']}")
            print(f"        Concluído: {'Sim' if livro['concluido'] else 'Não'}")

        print("-" * 41)

def atualizar(lista_cadastros):
    livro_procurado = input("Digite o nome do livro que deseja atualizar: ")
    livro = procurar_livro(livro_procurado,
                           lista_cadastros)  # Se o nome procurado for igual a algum nome de livro ja cadastrado
    if livro is None:  # Se o projeto for NONE, então ele não foi encontrado
        print("Erro, livro não encontrado.")
    else:
        alter = input("O que deseja atualizar (Nome, Autor, Resumo, Status)? ").capitalize()
        validos = {"Nome", "Autor", "Resumo", "Status"}
        if alter not in validos:
            print("Opção inválida! Nada foi alterado.")
        else:
            alteracao(livro, alter)
            salvar(lista_cadastros)

def estatisticas(lista_cadastros):
    print("\n--- STATUS PORTFÓLIO ---")
    total_livros = len(lista_cadastros)
    if total_livros == 0:
        print("Nenhum livro foi cadastrado ainda.")
        return
    concluidos = 0
    em_andamento = 0
    for livro in lista_cadastros:
        if livro["concluido"]:
            concluidos += 1
        else:
            em_andamento += 1
    print(f"Total de livros {total_livros}")
    print(f"Concluídos: {concluidos}")
    print(f"Em andamento: {em_andamento}")
    print(f"Taxa de conclusão: {concluidos * 100/total_livros:.2f}%")


lista_cadastros = processar() #A variável precisa ser declarada fora do While True para estar sempre vazia ao iniciar.
lista_de_comandos ={
"ABOUT" : "Informações",
"QUIT" : "Sair",
"ADD" : "Adicionar",
"LIST" : "Listar",
"UPDATE" : "Atualizar",
"DELETE" : "Deletar",
"STATS" : "Mostra os status do portfólio",
}

print("Bem vindo(a)!\n")
print("--- LISTA DE COMANDOS --- ")
for chave, valor in lista_de_comandos.items():
    print(f"{chave} : {valor}")

while True:
    comando = input("\nDigite um comando (ABOUT, QUIT, ADD, LIST, UPDATE, DELETE, STATS): ").upper()

    #Encerra o programa.
    if comando == "QUIT":
        print("Saindo da lista.")
        salvar(lista_cadastros)
        break

    #Apresenta informações sobre o criador.
    elif comando == "ABOUT":
        about()

    #Adiciona novos livros à lista.
    elif comando == "ADD":
        adicionar_livro(lista_cadastros)

    #Apresenta o que já há na lista.
    elif comando == "LIST":
        if not lista_cadastros:
            print("\nLista vazia, adicione um novo livro.")
        else:
            lista(lista_cadastros)

    #Atualiza os dados sobre o livro.
    elif comando == "UPDATE":
        atualizar(lista_cadastros)


    #Deleta o livro digitado pelo usuário.
    elif comando == "DELETE":
        deletar(lista_cadastros)

    elif comando ==  "STATS":
        estatisticas(lista_cadastros)
    else:
        print("ERRO: Comando não reconhecido.")
print("Programa encerrado, até logo!\n")
