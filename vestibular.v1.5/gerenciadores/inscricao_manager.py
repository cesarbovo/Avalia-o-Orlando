# gerenciadores/inscricao_manager.py

from modelos import Vestibulando

class GerenciadorInscricoes:
    def inscrever_vestibulando(self):
        print("\n--- Nova Inscrição ---")
        while True:
            nome = input("Digite o nome do candidato: ")
            if nome.strip() and nome.replace(' ', '').isalpha(): break
            else: print("ERRO: Nome inválido. Use apenas letras e espaços.")
        while True:
            cpf = input("Digite o CPF do candidato (apenas 11 números): ")
            if not cpf.isdigit() or len(cpf) != 11:
                print("ERRO: O CPF deve conter apenas 11 números."); continue
            if self.buscar_vestibulando_por_cpf(cpf):
                print("ERRO: Este CPF já foi cadastrado como vestibulando.")
                if input("Tentar com outro CPF? (s/n): ").lower() != 's': return
                else: continue
            if self.buscar_fiscal_por_cpf(cpf):
                print("ERRO: Este CPF pertence a um fiscal.")
                if input("Tentar com outro CPF? (s/n): ").lower() != 's': return
                else: continue
            break
        while True:
            opcao = input("Curso: [1] Inteligência Artificial, [2] Gestão ESG: ")
            if opcao == '1': curso = "Inteligência Artificial"; break
            elif opcao == '2': curso = "Gestão ESG"; break
            else: print("Opção inválida.")
        num_inscricao = int(f"{self.ano_vestibular}{self.contador_inscricao:04d}")
        self.contador_inscricao += 1
        self.vestibulandos.inserir_no_final(Vestibulando(num_inscricao, nome, cpf, curso))
        print(f"\nInscrição realizada! O número de {nome} é: {num_inscricao}")

    def editar_inscricao(self):
        print("\n--- Editar Inscrição ---")
        try: num_inscricao = int(input("Digite o número da inscrição a ser editada: "))
        except ValueError: print("Número inválido."); return
        vestibulando = self.buscar_vestibulando_por_inscricao(num_inscricao)
        if not vestibulando: print(f"Inscrição {num_inscricao} não encontrada."); return
        print("\nDados atuais:", vestibulando)
        while True:
            opcao = input("\nEditar: [1] Nome [2] CPF [3] Curso [0] Voltar: ")
            if opcao == '1': vestibulando.nome = input("Novo nome: "); print("Atualizado!")
            elif opcao == '2':
                while True:
                    novo_cpf = input("Novo CPF (11 números): ")
                    if not novo_cpf.isdigit() or len(novo_cpf) != 11: print("ERRO: Formato inválido."); continue
                    if novo_cpf != vestibulando.cpf and self.buscar_vestibulando_por_cpf(novo_cpf): print("ERRO: CPF já pertence a outro candidato."); continue
                    vestibulando.cpf = novo_cpf; print("Atualizado!"); break
            elif opcao == '3':
                esc = input("Novo curso: [1] IA [2] ESG: ")
                if esc == '1': vestibulando.opcao_curso = "Inteligência Artificial"; print("Atualizado!")
                elif esc == '2': vestibulando.opcao_curso = "Gestão ESG"; print("Atualizado!")
                else: print("Opção inválida.")
            elif opcao == '0': break
            else: print("Opção inválida.")
            print("Dados atualizados:", vestibulando)

    def efetivar_inscricao(self):
        print("\n--- Efetivar Inscrição ---")
        try: num_inscricao = int(input("Digite o número da inscrição a ser efetivada: "))
        except ValueError: print("Número inválido."); return
        vestibulando = self.buscar_vestibulando_por_inscricao(num_inscricao)
        if not vestibulando: print(f"Inscrição {num_inscricao} não encontrada."); return
        if vestibulando.efetivada: print(f"A inscrição de {vestibulando.nome} já estava efetivada.")
        else: vestibulando.efetivada = True; print(f"Inscrição de {vestibulando.nome} efetivada!")

    def exibir_inscritos(self): print("\n--- Lista de Candidatos Inscritos ---"); self.vestibulandos.exibir_lista()