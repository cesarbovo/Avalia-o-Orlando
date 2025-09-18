# gerenciadores/aprovacao_manager.py

from modelos import Aprovado

class GerenciadorAprovacao:
    def selecionar_aprovados(self):
        print("\n--- Seleção de Aprovados ---")
        opcao_curso = input("Para qual curso? [1] IA [2] ESG: ")
        if opcao_curso == '1': curso, lista_aprovados = "Inteligência Artificial", self.aprovados_ia
        elif opcao_curso == '2': curso, lista_aprovados = "Gestão ESG", self.aprovados_esg
        else: print("Opção inválida."); return
        VAGAS = 40
        if not self._exibir_aptos_por_curso(curso): return
        while True:
            if lista_aprovados.contar_elementos() >= VAGAS: print(f"\nAs {VAGAS} vagas foram preenchidas!"); break
            print(f"\n{lista_aprovados.contar_elementos()}/{VAGAS} vagas preenchidas.")
            op = input("Digite a INSCRIÇÃO do aprovado (ou '0' para sair): ")
            if op == '0': break
            try: num_inscricao = int(op)
            except ValueError: print("Entrada inválida."); continue
            candidato = self.buscar_vestibulando_por_inscricao(num_inscricao)
            if not candidato: print("ERRO: Candidato não encontrado.")
            elif candidato.opcao_curso != curso: print(f"ERRO: Candidato não é do curso de {curso}.")
            elif not candidato.efetivada: print("ERRO: Inscrição não efetivada.")
            elif self._ja_aprovado(num_inscricao, lista_aprovados): print("ERRO: Candidato já aprovado.")
            else:
                lista_aprovados.inserir_no_final(Aprovado(candidato.num_inscricao, candidato.nome, candidato.cpf))
                print(f"SUCESSO: {candidato.nome} aprovado(a)!")

    def exibir_aprovados(self):
        print("\n--- Lista de Aprovados em Inteligência Artificial ---"); self.aprovados_ia.exibir_lista()
        print("\n--- Lista de Aprovados em Gestão ESG ---"); self.aprovados_esg.exibir_lista()