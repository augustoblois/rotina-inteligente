"""
Rotina Inteligente — Gerenciador de Atividades da Camila
Etapa 1: Classes e Objetos
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from datetime import date


class Atividade:
    """Representa uma atividade na rotina de Camila."""

    total_atividades = 0

    def __init__(self, nome, categoria, duracao_horas, prioridade, prazo=None):
        self.nome = nome
        self.categoria = categoria
        self.duracao_horas = duracao_horas
        self.prioridade = prioridade        # 1 (baixa) a 5 (urgente)
        self.prazo = prazo                  # objeto date ou None
        self.concluida = False
        Atividade.total_atividades += 1

    def concluir(self):
        if self.concluida:
            print(f"  '{self.nome}' já foi concluída.")
        else:
            self.concluida = True
            print(f"  ✔ '{self.nome}' marcada como concluída!")

    def esta_atrasada(self):
        if self.prazo and not self.concluida:
            return date.today() > self.prazo
        return False

    def exibir(self):
        status = "✔" if self.concluida else ("⚠ ATRASADA" if self.esta_atrasada() else "○")
        prazo_str = self.prazo.strftime("%d/%m") if self.prazo else "—"
        print(f"  [{status}] {self.nome}")
        print(f"       Categoria : {self.categoria}")
        print(f"       Prioridade: {'★' * self.prioridade}{'☆' * (5 - self.prioridade)} ({self.prioridade}/5)")
        print(f"       Duração   : {self.duracao_horas}h | Prazo: {prazo_str}")


class DiaSemana:
    """Representa um dia da semana com suas atividades."""

    def __init__(self, nome):
        self.nome = nome
        self.atividades = []

    def adicionar(self, atividade):
        self.atividades.append(atividade)

    def carga_total(self):
        return sum(a.duracao_horas for a in self.atividades if not a.concluida)

    def esta_sobrecarregado(self):
        return self.carga_total() > 8

    def exibir(self):
        print(f"\n  {'='*40}")
        carga = self.carga_total()
        alerta = " ⚠ SOBRECARREGADA" if self.esta_sobrecarregado() else ""
        print(f"  {self.nome.upper()} — {carga}h de atividades{alerta}")
        print(f"  {'='*40}")
        if not self.atividades:
            print("  (dia livre)")
        for a in sorted(self.atividades, key=lambda x: -x.prioridade):
            a.exibir()


class Rotina:
    """Representa a rotina semanal de Camila."""

    DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

    def __init__(self):
        self.semana = {dia: DiaSemana(dia) for dia in self.DIAS}

    def adicionar(self, dia, atividade):
        if dia not in self.semana:
            print(f"  Dia '{dia}' inválido.")
            return
        self.semana[dia].adicionar(atividade)

    def carga_semanal(self):
        return sum(d.carga_total() for d in self.semana.values())

    def atividades_urgentes(self):
        urgentes = []
        for dia in self.semana.values():
            for a in dia.atividades:
                if a.prioridade >= 4 and not a.concluida:
                    urgentes.append(a)
        return sorted(urgentes, key=lambda x: -x.prioridade)

    def atividades_atrasadas(self):
        return [a for dia in self.semana.values()
                for a in dia.atividades if a.esta_atrasada()]

    def relatorio_semanal(self):
        print(f"\n{'='*45}")
        print("  RELATÓRIO SEMANAL — CAMILA")
        print(f"{'='*45}")
        total = self.carga_semanal()
        concluidas = sum(1 for d in self.semana.values()
                         for a in d.atividades if a.concluida)
        total_ativ = sum(len(d.atividades) for d in self.semana.values())
        print(f"  Carga total     : {total}h")
        print(f"  Atividades      : {total_ativ} ({concluidas} concluídas)")
        dias_pesados = [d for d in self.semana.values() if d.esta_sobrecarregado()]
        if dias_pesados:
            print(f"  Dias pesados    : {', '.join(d.nome for d in dias_pesados)}")
        else:
            print("  Nenhum dia sobrecarregado")
        urgentes = self.atividades_urgentes()
        if urgentes:
            print(f"\n  Urgentes ({len(urgentes)}):")
            for a in urgentes:
                print(f"    - {a.nome} (prioridade {a.prioridade})")
        atrasadas = self.atividades_atrasadas()
        if atrasadas:
            print(f"\n  Atrasadas ({len(atrasadas)}):")
            for a in atrasadas:
                print(f"    - {a.nome} (prazo: {a.prazo.strftime('%d/%m')})")

    def exibir_semana(self):
        for dia in self.semana.values():
            dia.exibir()


class Camila:
    """Perfil da Camila com sua rotina personalizada."""

    def __init__(self):
        self.nome = "Camila Ferreira"
        self.curso = "Psicologia"
        self.semestre = 3
        self.idade = 20
        self.rotina = Rotina()

    def exibir_perfil(self):
        print(f"\n{'='*45}")
        print(f"  {self.nome}")
        print(f"  Curso: {self.curso} | {self.semestre}º semestre | {self.idade} anos")
        print(f"  Carga semanal: {self.rotina.carga_semanal()}h")
        print(f"{'='*45}")

    def adicionar_atividade(self, dia, nome, categoria, duracao, prioridade, prazo=None):
        atividade = Atividade(nome, categoria, duracao, prioridade, prazo)
        self.rotina.adicionar(dia, atividade)
        return atividade


# ── Demonstração ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    camila = Camila()

    # Atividades fixas da semana
    camila.adicionar_atividade("Segunda", "Estágio na clínica", "Estágio", 4, 5)
    camila.adicionar_atividade("Segunda", "Aulas de Psicologia", "Faculdade", 3, 4)
    camila.adicionar_atividade("Segunda", "Academia", "Saúde", 1, 3)

    camila.adicionar_atividade("Terça", "Estágio na clínica", "Estágio", 4, 5)
    camila.adicionar_atividade("Terça", "Aulas de Psicologia", "Faculdade", 3, 4)
    camila.adicionar_atividade("Terça", "Grupo de pesquisa", "Pesquisa", 2, 4,
                               prazo=date(2026, 5, 27))

    camila.adicionar_atividade("Quarta", "Estágio na clínica", "Estágio", 4, 5)
    camila.adicionar_atividade("Quarta", "Aulas de Psicologia", "Faculdade", 3, 4)
    camila.adicionar_atividade("Quarta", "Tarefas domésticas", "Casa", 2, 2)

    camila.adicionar_atividade("Quinta", "Estágio na clínica", "Estágio", 4, 5)
    camila.adicionar_atividade("Quinta", "Aulas de Psicologia", "Faculdade", 3, 4)
    camila.adicionar_atividade("Quinta", "Academia", "Saúde", 1, 3)
    camila.adicionar_atividade("Quinta", "Trabalho de Psicologia Social", "Faculdade", 3, 5,
                               prazo=date(2026, 5, 22))

    camila.adicionar_atividade("Sexta", "Estágio na clínica", "Estágio", 4, 5)
    camila.adicionar_atividade("Sexta", "Reunião do grupo de pesquisa", "Pesquisa", 2, 4)
    camila.adicionar_atividade("Sexta", "Academia", "Saúde", 1, 3)

    camila.adicionar_atividade("Sábado", "Revisão de conteúdo", "Faculdade", 2, 3)
    camila.adicionar_atividade("Sábado", "Tempo pessoal", "Bem-estar", 3, 2)

    camila.adicionar_atividade("Domingo", "Planejamento da semana", "Organização", 1, 4)
    camila.adicionar_atividade("Domingo", "Tempo em família", "Bem-estar", 2, 2)

    # Exibe perfil e semana
    camila.exibir_perfil()
    camila.rotina.exibir_semana()

    # Simula conclusão de algumas atividades
    print("\n\n--- Concluindo atividades ---")
    seg = camila.rotina.semana["Segunda"]
    seg.atividades[0].concluir()   # estágio
    seg.atividades[1].concluir()   # aulas

    # Relatório final
    camila.rotina.relatorio_semanal()

    print(f"\n  Total de atividades criadas: {Atividade.total_atividades}")
