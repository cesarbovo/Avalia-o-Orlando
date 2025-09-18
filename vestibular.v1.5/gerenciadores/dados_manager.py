# gerenciadores/dados_manager.py

from modelos import Vestibulando, Fiscal, Aprovado

class GerenciadorDados:
    def salvar_dados(self, nome_arquivo="vestibular.dat"):
        print(f"\nSalvando dados em {nome_arquivo}...")
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write("[VESTIBULANDOS]\n")
                no_atual = self.vestibulandos.cabeca
                while no_atual:
                    c = no_atual.dado; arquivo.write(f"{c.num_inscricao}|{c.nome}|{c.cpf}|{c.opcao_curso}|{c.efetivada}\n"); no_atual = no_atual.proximo
                arquivo.write("[FISCAIS]\n")
                no_atual = self.fiscais.cabeca
                while no_atual:
                    f = no_atual.dado; arquivo.write(f"{f.nome}|{f.cargo}|{f.cpf}\n"); no_atual = no_atual.proximo
                arquivo.write("[APROVADOS_IA]\n")
                no_atual = self.aprovados_ia.cabeca
                while no_atual:
                    a = no_atual.dado; arquivo.write(f"{a.num_inscricao}|{a.nome}|{a.cpf}\n"); no_atual = no_atual.proximo
                arquivo.write("[APROVADOS_ESG]\n")
                no_atual = self.aprovados_esg.cabeca
                while no_atual:
                    a = no_atual.dado; arquivo.write(f"{a.num_inscricao}|{a.nome}|{a.cpf}\n"); no_atual = no_atual.proximo
            print("Dados salvos com sucesso!")
        except IOError as e:
            print(f"Erro ao salvar o arquivo: {e}")

    def carregar_dados(self, nome_arquivo="vestibular.dat"):
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                secao_atual = None
                for linha in arquivo:
                    linha = linha.strip()
                    if not linha: continue
                    if linha.startswith('[') and linha.endswith(']'):
                        secao_atual = linha; continue
                    partes = linha.split('|')
                    if secao_atual == "[VESTIBULANDOS]": self.vestibulandos.inserir_no_final(Vestibulando(int(partes[0]), partes[1], partes[2], partes[3], partes[4] == 'True'))
                    elif secao_atual == "[FISCAIS]": self.fiscais.inserir_no_final(Fiscal(partes[0], partes[1], partes[2]))
                    elif secao_atual == "[APROVADOS_IA]": self.aprovados_ia.inserir_no_final(Aprovado(int(partes[0]), partes[1], partes[2]))
                    elif secao_atual == "[APROVADOS_ESG]": self.aprovados_esg.inserir_no_final(Aprovado(int(partes[0]), partes[1], partes[2]))
            self._atualizar_contador_inscricao()
            print(f"Dados carregados de {nome_arquivo}.")
        except FileNotFoundError:
            print("Arquivo de dados não encontrado. Iniciando novo sistema.")
        except Exception as e:
            print(f"Ocorreu um erro ao carregar os dados: {e}")