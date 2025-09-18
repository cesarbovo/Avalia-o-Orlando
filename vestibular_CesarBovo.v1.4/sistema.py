# sistema.py

from estruturas import ListaEncadeada
from modelos import Vestibulando, Fiscal, Aprovado, Sala

class SistemaVestibular:
    """Gerencia todas as operações do vestibular."""
    def __init__(self):
        self.vestibulandos = ListaEncadeada()
        self.fiscais = ListaEncadeada()
        self.aprovados_ia = ListaEncadeada()
        self.aprovados_esg = ListaEncadeada()
        self.ano_vestibular = 2026
        self.contador_inscricao = 1
        
        self.carregar_dados()

    # --- MÉTODOS DE INSCRIÇÃO E EDIÇÃO ---
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

    # --- MÉTODOS DE ORGANIZAÇÃO DO VESTIBULAR ---
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

    def organizar_salas_e_alunos(self):
        print("\n--- Organização das Salas do Vestibular ---")
        num_salas = self.calcular_salas()
        if num_salas > self.fiscais.contar_elementos():
            print(f"ERRO: São necessárias {num_salas} salas, mas há apenas {self.fiscais.contar_elementos()} fiscais."); return
        if num_salas == 0: print("Não há candidatos aptos para alocar."); return
        print(f"Candidatos aptos: {self.contar_efetivados()} | Salas necessárias: {num_salas}")
        salas = [Sala(i + 1) for i in range(num_salas)]
        no_fiscal_atual = self.fiscais.cabeca
        for sala in salas:
            if no_fiscal_atual: sala.fiscal_responsavel = no_fiscal_atual.dado; no_fiscal_atual = no_fiscal_atual.proximo
        total_efetivados = self.contar_efetivados()
        base_por_sala = total_efetivados // num_salas
        alunos_extras = total_efetivados % num_salas
        no_aluno_atual = self.vestibulandos.cabeca
        sala_atual_index = 0
        while no_aluno_atual and sala_atual_index < num_salas:
            if no_aluno_atual.dado.efetivada:
                sala_alvo = salas[sala_atual_index]
                limite_sala = base_por_sala + (1 if sala_atual_index < alunos_extras else 0)
                sala_alvo.alunos.inserir_no_final(no_aluno_atual.dado)
                if sala_alvo.alunos.contar_elementos() == limite_sala:
                    sala_atual_index += 1
            no_aluno_atual = no_aluno_atual.proximo
        print("\n--- Distribuição Final de Candidatos e Fiscais por Sala ---")
        for sala in salas:
            print(sala); sala.alunos.exibir_lista()

    # --- MÉTODOS DE RELATÓRIO E EXIBIÇÃO ---
    def exibir_inscritos(self): print("\n--- Lista de Candidatos Inscritos ---"); self.vestibulandos.exibir_lista()
    def exibir_fiscais(self): print("\n--- Lista de Fiscais Cadastrados ---"); self.fiscais.exibir_lista()
    def exibir_candidatos_por_vaga(self):
        print("\n--- Relação de Candidatos por Vaga ---")
        VAGAS = 40.0; cursos = ["Inteligência Artificial", "Gestão ESG"]
        for curso in cursos:
            print(f"\nCurso: {curso}")
            total = self.contar_total_por_curso(curso)
            efetivados = self.contar_efetivados_por_curso(curso)
            print(f"  - Total de inscritos: {total} ({total/VAGAS:.2f} por vaga)")
            print(f"  - Inscrições efetivadas: {efetivados} ({efetivados/VAGAS:.2f} por vaga)")
    def exibir_aprovados(self):
        print("\n--- Lista de Aprovados em Inteligência Artificial ---"); self.aprovados_ia.exibir_lista()
        print("\n--- Lista de Aprovados em Gestão ESG ---"); self.aprovados_esg.exibir_lista()

    # --- MÉTODOS DE APROVAÇÃO ---
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

    # --- MÉTODOS DE PERSISTÊNCIA (SALVAR/CARREGAR) ---
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
            
    # --- MÉTODOS AUXILIARES / INTERNOS ---
    def _atualizar_contador_inscricao(self):
        no_atual = self.vestibulandos.cabeca; maior_inscricao = 0
        while no_atual:
            if no_atual.dado.num_inscricao > maior_inscricao: maior_inscricao = no_atual.dado.num_inscricao
            no_atual = no_atual.proximo
        if maior_inscricao > 0: self.contador_inscricao = (maior_inscricao % 10000) + 1
    def buscar_vestibulando_por_cpf(self, cpf):
        n=self.vestibulandos.cabeca;
        while n:
            if n.dado.cpf==cpf: return True
            n=n.proximo
        return False
    def buscar_fiscal_por_cpf(self, cpf):
        n=self.fiscais.cabeca
        while n:
            if n.dado.cpf==cpf: return n.dado
            n=n.proximo
        return None
    def buscar_vestibulando_por_inscricao(self, num):
        n=self.vestibulandos.cabeca
        while n:
            if n.dado.num_inscricao==num: return n.dado
            n=n.proximo
        return None
    def contar_efetivados(self):
        c=0; n=self.vestibulandos.cabeca
        while n:
            if n.dado.efetivada: c+=1
            n=n.proximo
        return c
    def calcular_salas(self):
        t=self.contar_efetivados(); s=t//30
        if t%30>0: s+=1
        return s
    def contar_total_por_curso(self, nc):
        c=0; n=self.vestibulandos.cabeca
        while n:
            if n.dado.opcao_curso==nc: c+=1
            n=n.proximo
        return c
    def contar_efetivados_por_curso(self, nc):
        c=0; n=self.vestibulandos.cabeca
        while n:
            if n.dado.opcao_curso==nc and n.dado.efetivada: c+=1
            n=n.proximo
        return c
    def _exibir_aptos_por_curso(self, nc):
        print(f"\n--- Candidatos aptos para {nc} ---")
        n=self.vestibulandos.cabeca; achou=False
        while n:
            if n.dado.opcao_curso==nc and n.dado.efetivada: print(n.dado); achou=True
            n=n.proximo
        if not achou: print("Nenhum candidato apto encontrado.")
        print("-" * 52); return achou
    def _ja_aprovado(self, num, la):
        n=la.cabeca
        while n:
            if n.dado.num_inscricao==num: return True
            n=n.proximo
        return False
        
    # --- MÉTODO PRINCIPAL DE EXECUÇÃO ---
    def executar(self):
        while True:
            print("\n" + "="*20 + " MENU PRINCIPAL " + "="*20)
            print("[1] Inscrever Candidato      [2] Exibir Inscritos")
            print("[3] Editar Inscrição         [4] Efetivar Inscrição")
            print("\n--- Organização ---")
            print("[5] Cadastrar Fiscal         [6] Exibir Fiscais")
            print("[7] Editar Fiscal            [8] Organizar Alunos/Salas")
            print("[9] Relatório Cand./Vaga")
            print("\n--- Aprovação ---")
            print("[10] Selecionar Aprovados    [11] Exibir Aprovados")
            print("[0] Salvar e Sair")
            print("="*62)
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1': self.inscrever_vestibulando()
            elif opcao == '2': self.exibir_inscritos()
            elif opcao == '3': self.editar_inscricao()
            elif opcao == '4': self.efetivar_inscricao()
            elif opcao == '5': self.cadastrar_fiscal()
            elif opcao == '6': self.exibir_fiscais()
            elif opcao == '7': self.editar_fiscal()
            elif opcao == '8': self.organizar_salas_e_alunos()
            elif opcao == '9': self.exibir_candidatos_por_vaga()
            elif opcao == '10': self.selecionar_aprovados()
            elif opcao == '11': self.exibir_aprovados()
            elif opcao == '0':
                self.salvar_dados()
                print("Saindo do sistema. Até logo!")
                break
            else:
                print("Opção inválida.")
            
            if opcao != '0':
                input("\nPressione Enter para voltar ao menu...")