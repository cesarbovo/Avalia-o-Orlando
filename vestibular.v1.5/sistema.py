# sistema.py

from estruturas import ListaEncadeada
from gerenciadores.dados_manager import GerenciadorDados
from gerenciadores.inscricao_manager import GerenciadorInscricoes
from gerenciadores.fiscal_manager import GerenciadorFiscais
from gerenciadores.organizacao_manager import GerenciadorOrganizacao
from gerenciadores.aprovacao_manager import GerenciadorAprovacao

class SistemaVestibular(
    GerenciadorDados,
    GerenciadorInscricoes,
    GerenciadorFiscais,
    GerenciadorOrganizacao,
    GerenciadorAprovacao
):
    """Orquestra todas as operações do vestibular, herdando funcionalidades dos gerenciadores."""
    def __init__(self):
        self.vestibulandos = ListaEncadeada()
        self.fiscais = ListaEncadeada()
        self.aprovados_ia = ListaEncadeada()
        self.aprovados_esg = ListaEncadeada()
        self.ano_vestibular = 2026
        self.contador_inscricao = 1
        
        self.carregar_dados()

    # --- MÉTODOS AUXILIARES / INTERNOS (Usados por vários gerenciadores) ---
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