"""
Rotina Inteligente — Gerenciador de Atividades da Camila
Etapa 2: Encapsulamento, Herança, Polimorfismo, Interfaces, SOLID
"""

from datetime import date
from abc import ABC, abstractmethod
import sys
sys.stdout.reconfigure(encoding='utf-8')


# ── INTERFACES (Princípio I do SOLID: Interface Segregation) ──────────────────

class IExibivel(ABC):
    """Contrato para objetos que podem se exibir na tela."""
    @abstractmethod
    def exibir(self): pass


class IAvaliavel(ABC):
    """Contrato para atividades que podem ser avaliadas como urgentes."""
    @abstractmethod
    def esta_urgente(self) -> bool: pass

    @abstractmethod
    def esta_atrasada(self) -> bool: pass


# ── CLASSE BASE ABSTRATA: Atividade ───────────────────────────────────────────
# (Princípio O do SOLID: aberta para extensão, fechada para modificação)

class Atividade(IExibivel, IAvaliavel, ABC):
    """Base para todos os tipos de atividade de Camila."""

    _total = 0

    def __init__(self, nome: str, duracao_horas: float, prioridade: int):
        self._nome = nome
        self._duracao_horas = duracao_horas
        self._prioridade = prioridade
        self._concluida = False
        Atividade._total += 1

    # ── Properties (Encapsulamento) ───────────────────────────────────────────

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def duracao_horas(self) -> float:
        return self._duracao_horas

    @duracao_horas.setter
    def duracao_horas(self, valor: float):
        if valor <= 0:
            raise ValueError("Duração deve ser positiva.")
        self._duracao_horas = valor

    @property
    def prioridade(self) -> int:
        return self._prioridade

    @prioridade.setter
    def prioridade(self, valor: int):
        if not (1 <= valor <= 5):
            raise ValueError("Prioridade deve ser entre 1 e 5.")
        self._prioridade = valor

    @property
    def concluida(self) -> bool:
        return self._concluida

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Cada subclasse declara seu tipo (polimorfismo)."""
        pass

    # ── Comportamentos comuns ─────────────────────────────────────────────────

    def concluir(self):
        if self._concluida:
            print(f"  '{self._nome}' já concluída.")
        else:
            self._concluida = True
            print(f"  ✔ '{self._nome}' concluída!")

    def esta_urgente(self) -> bool:
        return self._prioridade >= 4 and not self._concluida

    def exibir(self):
        status = "✔" if self._concluida else (
            "⚠" if self.esta_atrasada() else "○")
        print(f"  [{status}] [{self.tipo}] {self._nome}")
        print(f"       Prioridade: {'★' * self._prioridade}{'☆' * (5 - self._prioridade)}"
              f" | Duração: {self._duracao_horas}h")
        self._exibir_extras()

    def _exibir_extras(self):
        """Hook para subclasses adicionarem informações extras."""
        pass

    @classmethod
    def total(cls) -> int:
        return cls._total


# ── SUBCLASSES (Herança + Polimorfismo) ───────────────────────────────────────

class Tarefa(Atividade):
    """Tarefa acadêmica com prazo obrigatório (ex.: trabalho, prova)."""

    def __init__(self, nome: str, duracao_horas: float, prioridade: int, prazo: date):
        super().__init__(nome, duracao_horas, prioridade)
        self._prazo = prazo

    @property
    def tipo(self) -> str:
        return "TAREFA"

    @property
    def prazo(self) -> date:
        return self._prazo

    def esta_atrasada(self) -> bool:
        return date.today() > self._prazo and not self._concluida

    def dias_restantes(self) -> int:
        return (self._prazo - date.today()).days

    def _exibir_extras(self):
        dias = self.dias_restantes()
        if dias < 0:
            print(
                f"       Prazo: {self._prazo.strftime('%d/%m')} — ATRASADA {abs(dias)} dia(s)")
        elif dias == 0:
            print(f"       Prazo: {self._prazo.strftime('%d/%m')} — HOJE!")
        else:
            print(
                f"       Prazo: {self._prazo.strftime('%d/%m')} — {dias} dia(s) restante(s)")


class Compromisso(Atividade):
    """Compromisso fixo no horário (estágio, aula, reunião)."""

    def __init__(self, nome: str, duracao_horas: float, prioridade: int,
                 horario: str, local: str):
        super().__init__(nome, duracao_horas, prioridade)
        self._horario = horario
        self._local = local

    @property
    def tipo(self) -> str:
        return "COMPROMISSO"

    def esta_atrasada(self) -> bool:
        return False   # compromisso não tem prazo, só horário

    def _exibir_extras(self):
        print(f"       Horário: {self._horario} | Local: {self._local}")


class HabitoSaude(Atividade):
    """Hábito de saúde recorrente (academia, meditação, sono)."""

    def __init__(self, nome: str, duracao_horas: float, prioridade: int,
                 frequencia_semanal: int):
        super().__init__(nome, duracao_horas, prioridade)
        self._frequencia = frequencia_semanal
        self._realizacoes = 0

    @property
    def tipo(self) -> str:
        return "HÁBITO"

    def esta_atrasada(self) -> bool:
        return False

    def registrar_realizacao(self):
        self._realizacoes += 1
        print(
            f"  ✔ '{self._nome}' realizada ({self._realizacoes}/{self._frequencia}x na semana).")

    def meta_atingida(self) -> bool:
        return self._realizacoes >= self._frequencia

    def _exibir_extras(self):
        meta = "✔ meta!" if self.meta_atingida(
        ) else f"{self._realizacoes}/{self._frequencia}x"
        print(f"       Frequência: {self._frequencia}x/semana — {meta}")


# ── DIA DA SEMANA ─────────────────────────────────────────────────────────────

class DiaSemana(IExibivel):
    """Agrupa atividades de um dia."""

    def __init__(self, nome: str):
        self._nome = nome
        self._atividades: list[Atividade] = []

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def atividades(self) -> list[Atividade]:
        return list(self._atividades)

    def adicionar(self, atividade: Atividade):
        self._atividades.append(atividade)

    def carga_total(self) -> float:
        return sum(a.duracao_horas for a in self._atividades if not a.concluida)

    def esta_sobrecarregado(self) -> bool:
        return self.carga_total() > 8

    def urgentes(self) -> list[Atividade]:
        return [a for a in self._atividades if a.esta_urgente()]

    def exibir(self):
        alerta = " ⚠ SOBRECARREGADA" if self.esta_sobrecarregado() else ""
        print(f"\n  {'='*42}")
        print(f"  {self._nome.upper()} — {self.carga_total():.1f}h{alerta}")
        print(f"  {'='*42}")
        if not self._atividades:
            print("  (dia livre)")
            return
        for a in sorted(self._atividades, key=lambda x: -x.prioridade):
            a.exibir()


# ── ROTINA SEMANAL ─────────────────────────────────────────────────────────────
# (Princípio D do SOLID: depende de Atividade abstrata, não de tipos concretos)

class Rotina:
    """Rotina semanal de Camila."""

    DIAS = ["Segunda", "Terça", "Quarta",
            "Quinta", "Sexta", "Sábado", "Domingo"]

    def __init__(self):
        self._semana: dict[str, DiaSemana] = {
            d: DiaSemana(d) for d in self.DIAS}

    def adicionar(self, dia: str, atividade: Atividade):
        if dia not in self._semana:
            print(f"  Dia '{dia}' inválido.")
            return
        self._semana[dia].adicionar(atividade)

    def carga_semanal(self) -> float:
        return sum(d.carga_total() for d in self._semana.values())

    def urgentes(self) -> list[Atividade]:
        result = []
        for dia in self._semana.values():
            result.extend(dia.urgentes())
        return sorted(result, key=lambda a: -a.prioridade)

    def atrasadas(self) -> list[Atividade]:
        return [a for d in self._semana.values()
                for a in d.atividades if a.esta_atrasada()]

    def exibir_semana(self):
        for dia in self._semana.values():
            dia.exibir()

    def relatorio(self):
        total_ativ = sum(len(d.atividades) for d in self._semana.values())
        concluidas = sum(1 for d in self._semana.values()
                         for a in d.atividades if a.concluida)
        print(f"\n{'='*45}")
        print("  RELATÓRIO SEMANAL — CAMILA")
        print(f"{'='*45}")
        print(f"  Carga total   : {self.carga_semanal():.1f}h")
        print(f"  Atividades    : {total_ativ} | Concluídas: {concluidas}")

        tipos: dict[str, int] = {}
        for d in self._semana.values():
            for a in d.atividades:
                tipos[a.tipo] = tipos.get(a.tipo, 0) + 1
        print(f"\n  Por tipo (polimorfismo):")
        for t, n in tipos.items():
            print(f"    {t:12}: {n}")

        urgentes = self.urgentes()
        if urgentes:
            print(f"\n  Urgentes ({len(urgentes)}):")
            for a in urgentes:
                print(f"    ! {a.nome}")

        atrasadas = self.atrasadas()
        if atrasadas:
            print(f"\n  Atrasadas ({len(atrasadas)}):")
            for a in atrasadas:
                print(f"    ⚠ {a.nome}")


# ── PERFIL DA CAMILA ──────────────────────────────────────────────────────────
# (Princípio S do SOLID: Camila apenas mantém perfil, Rotina gerencia atividades)

class Camila:
    """Perfil da Camila com sua rotina personalizada."""

    def __init__(self):
        self._nome = "Camila Ferreira"
        self._curso = "Psicologia"
        self._semestre = 3
        self._idade = 20
        self._rotina = Rotina()

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def rotina(self) -> Rotina:
        return self._rotina

    def exibir_perfil(self):
        print(f"\n{'='*45}")
        print(f"  {self._nome}")
        print(f"  {self._curso} | {self._semestre}º semestre | {self._idade} anos")
        print(f"  Carga semanal: {self._rotina.carga_semanal():.1f}h")
        print(f"{'='*45}")


# ── Demonstração ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    camila = Camila()
    r = camila.rotina

    # Compromissos fixos
    r.adicionar("Segunda",  Compromisso(
        "Estágio na clínica",    4, 5, "08h–12h", "Clínica Norte"))
    r.adicionar("Segunda",  Compromisso(
        "Aulas de Psicologia",   3, 4, "14h–17h", "Faculdade"))
    r.adicionar("Terça",    Compromisso(
        "Estágio na clínica",    4, 5, "08h–12h", "Clínica Norte"))
    r.adicionar("Terça",    Compromisso(
        "Aulas de Psicologia",   3, 4, "14h–17h", "Faculdade"))
    r.adicionar("Quarta",   Compromisso(
        "Estágio na clínica",    4, 5, "08h–12h", "Clínica Norte"))
    r.adicionar("Quarta",   Compromisso(
        "Aulas de Psicologia",   3, 4, "14h–17h", "Faculdade"))
    r.adicionar("Quinta",   Compromisso(
        "Estágio na clínica",    4, 5, "08h–12h", "Clínica Norte"))
    r.adicionar("Quinta",   Compromisso(
        "Aulas de Psicologia",   3, 4, "14h–17h", "Faculdade"))
    r.adicionar("Sexta",    Compromisso(
        "Estágio na clínica",    4, 5, "08h–12h", "Clínica Norte"))
    r.adicionar("Sexta",    Compromisso(
        "Reunião de pesquisa",   2, 4, "18h–20h", "Online"))

    # Tarefas com prazo
    r.adicionar("Quinta",   Tarefa(
        "Trabalho Psicologia Social", 3, 5, date(2026, 5, 22)))
    r.adicionar("Terça",    Tarefa(
        "Relatório de estágio",       2, 4, date(2026, 5, 27)))
    r.adicionar("Sábado",   Tarefa(
        "Revisão para prova",         3, 4, date(2026, 5, 30)))

    # Hábitos de saúde
    academia = HabitoSaude("Academia", 1, 3, frequencia_semanal=3)
    r.adicionar("Segunda", academia)
    r.adicionar("Quarta",  academia)
    r.adicionar("Sexta",   academia)

    r.adicionar("Domingo",  HabitoSaude("Tempo pessoal",          2, 2, 1))

    # Exibe perfil e semana
    camila.exibir_perfil()
    camila.rotina.exibir_semana()

    # Simula conclusões e hábitos
    print("\n\n--- Ações da semana ---")
    r._semana["Segunda"].atividades[0].concluir()
    academia.registrar_realizacao()
    academia.registrar_realizacao()
    academia.registrar_realizacao()

    # Relatório final
    camila.rotina.relatorio()

    print(f"\n  Total de atividades criadas: {Atividade.total()}")
