# estruturas.py

class No:
    """Representa um nó (o 'vagão') em nossa lista encadeada."""
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class ListaEncadeada:
    """Representa a lista encadeada (o 'trem') que gerencia os nós."""
    def __init__(self):
        self.cabeca = None

    def inserir_no_final(self, dado):
        novo_no = No(dado)
        if self.cabeca is None:
            self.cabeca = novo_no
            return
        ultimo_no = self.cabeca
        while ultimo_no.proximo:
            ultimo_no = ultimo_no.proximo
        ultimo_no.proximo = novo_no

    def exibir_lista(self):
        if self.cabeca is None:
            print("A lista está vazia.")
            return
        no_atual = self.cabeca
        while no_atual:
            print(no_atual.dado)
            no_atual = no_atual.proximo

    def contar_elementos(self):
        contador = 0
        no_atual = self.cabeca
        while no_atual:
            contador += 1
            no_atual = no_atual.proximo
        return contador