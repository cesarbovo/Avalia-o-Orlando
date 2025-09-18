# gerenciadores/fiscal_manager.py

from modelos import Fiscal

class GerenciadorFiscais:
    def cadastrar_fiscal(self):
        print("\n--- Cadastro de Novo Fiscal ---")
        while True:
            nome = input("Digite o nome do fiscal: ")
            if nome.strip() and nome.replace(' ', '').isalpha(): break
            else: print("ERRO: Nome inválido. Use apenas letras e espaços.")
        cargo = input("Digite o cargo do fiscal: ")
        while True:
            cpf = input("Digite o CPF do fiscal (apenas 11 números): ")
            if not cpf.isdigit() or len(cpf) != 11:
                print("ERRO: O CPF deve conter apenas 11 números."); continue
            if self.buscar_fiscal_por_cpf(cpf):
                print("ERRO: Este CPF já foi cadastrado para outro fiscal."); continue
            if self.buscar_vestibulando_por_cpf(cpf):
                print("ERRO: Este CPF pertence a um vestibulando."); continue
            break
        self.fiscais.inserir_no_final(Fiscal(nome, cargo, cpf))
        print(f"\nFiscal {nome} cadastrado!")

    def editar_fiscal(self):
        print("\n--- Editar Cadastro de Fiscal ---")
        cpf_fiscal = input("Digite o CPF do fiscal que deseja editar (11 números): ")
        fiscal = self.buscar_fiscal_por_cpf(cpf_fiscal)
        if not fiscal: print(f"Nenhum fiscal encontrado com o CPF '{cpf_fiscal}'."); return
        print("\nDados atuais:", fiscal)
        while True:
            opcao = input("\nEditar: [1] Nome [2] Cargo [0] Voltar: ")
            if opcao == '1': fiscal.nome = input("Novo nome: "); print("Atualizado!")
            elif opcao == '2': fiscal.cargo = input("Novo cargo: "); print("Atualizado!")
            elif opcao == '0': break
            else: print("Opção inválida.")
            print("\nDados atualizados:", fiscal)

    def exibir_fiscais(self): print("\n--- Lista de Fiscais Cadastrados ---"); self.fiscais.exibir_lista()