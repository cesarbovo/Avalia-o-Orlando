# modelos.py

from estruturas import ListaEncadeada

class Vestibulando:
    """Representa a 'ficha de inscrição' de um candidato."""
    def __init__(self, num_inscricao, nome, cpf, curso, efetivada=False):
        self.num_inscricao = num_inscricao
        self.nome = nome
        self.cpf = cpf
        self.opcao_curso = curso
        self.efetivada = efetivada

    def __str__(self):
        status = "Efetivada" if self.efetivada else "Pendente"
        return (f"Inscrição: {self.num_inscricao} | "
                f"Nome: {self.nome} | "
                f"CPF: {self.cpf} | "
                f"Curso: {self.opcao_curso} | "
                f"Status: {status}")

class Fiscal:
    """Representa a 'ficha' de um fiscal aplicador da prova."""
    def __init__(self, nome, cargo, cpf):
        self.nome = nome
        self.cargo = cargo
        self.cpf = cpf

    def __str__(self):
        return f"Nome: {self.nome} | Cargo: {self.cargo} | CPF: {self.cpf}"

class Aprovado:
    """Representa a 'ficha' de um aluno aprovado."""
    def __init__(self, num_inscricao, nome, cpf):
        self.num_inscricao = num_inscricao
        self.nome = nome
        self.cpf = cpf

    def __str__(self):
        return (f"Inscrição: {self.num_inscricao} | "
                f"Nome: {self.nome} | "
                f"CPF: {self.cpf}")

class Sala:
    """Representa uma sala de aplicação de prova."""
    def __init__(self, numero_sala):
        self.numero = numero_sala
        self.fiscal_responsavel = None
        self.alunos = ListaEncadeada()

    def __str__(self):
        nome_fiscal = self.fiscal_responsavel.nome if self.fiscal_responsavel else "Ainda não definido"
        total_alunos = self.alunos.contar_elementos()
        
        cabecalho = (f"\n--- SALA {self.numero} ({total_alunos} candidatos) ---\n"
                     f"Fiscal Responsável: {nome_fiscal}\n"
                     "------------------------------------------")
        return cabecalho