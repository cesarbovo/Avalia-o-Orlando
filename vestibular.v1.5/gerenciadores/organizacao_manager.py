# gerenciadores/organizacao_manager.py

from modelos import Sala

class GerenciadorOrganizacao:
    def organizar_salas_e_alunos(self):
        print('\n---Organização das Salas do Vestibular---')
        num_salas=self.calcular_salas()
        if num_salas>self.fiscais.contar_elementos():
            print(f'ERRO: São necessárias {num_salas} salas, mas há apenas  {self.fiscais.contar_elementos()} fiscais');return
        if num_salas==0:
            print('Não há candidatos aptos para alocar.')
            return
        print(f'Candidatos aptos: {self.contar_efetivados()} | Salas necessárias {num_salas}')
        salas=[Sala (i+1) for i in range(num_salas)]
        no_fiscal_atual=self.fiscais.cabeca
        for sala in salas:
            if no_fiscal_atual: sala.fiscal_responsavel=no_fiscal_atual.dado;no_fiscal_atual=no_fiscal_atual.proximo
        total_efetivados=self.contar_efetivados()
        base_por_sala=total_efetivados//num_salas
        alunos_extras=total_efetivados%num_salas
        no_aluno_atual=self.vestibulandos.cabeca
        sala_atual_index=0
        while no_aluno_atual and sala_atual_index<num_salas:
            if no_aluno_atual.dado.efetivada:
                sala_alvo=salas[sala_atual_index]
                limite_sala=base_por_sala + (1 if sala_atual_index<alunos_extras else 0)
                sala_alvo.alunos.inserir_no_final(no_aluno_atual.dado)
                if sala_alvo.alunos.contar_elementos()== limite_sala:
                    sala_atual_index +=1
            no_aluno_atual=no_aluno_atual.proximo
        print('\n---Distribuição Final de Candidatos e Fiscais por Sala---' )
        for sala in salas:
            print(sala); sala.alunos.exibir_lista()
    
    def exibir_candidatos_por_vaga(self):
        print('\n---Relação de Candidatos por Vaga---')
        VAGAS=40.0; cursos=['Inteligência Artificial', 'Gestão ESG']
        for curso in cursos:
            print(f'\nCurso: {curso}')
            total=self.contar_total_por_curso(curso)
            efetivados=self.contar_efetivados_por_curso(curso)
            print(f'-Total de Inscritos: {total} ({total/VAGAS:.2f} por vaga)')
            print(f'Inscrições Efetivadas: {efetivados} ({efetivados/VAGAS:.2f} por vaga)')
