"""
Rotina Inteligente — Gerenciador de Atividades da Camila
Etapa 3: Recursão, Tabelas Hash, Grafos, BFS + revisão SOLID
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from abc import ABC, abstractmethod
from collections import deque
from datetime import date


# ════════════════════════════════════════════════════════════
#  TABELA HASH (implementação própria — sem usar dict nativo)
# ════════════════════════════════════════════════════════════

class TabelaHash:
    """
    Tabela hash com encadeamento (chaining) para colisões.
    Armazena atividades pelo nome — busca O(1) amortizado.
    """

    def __init__(self, capacidade: int = 13):
        self._capacidade = capacidade
        self._baldes: list[list] = [[] for _ in range(capacidade)]
        self._tamanho = 0

    def _hash(self, chave: str) -> int:
        h = 0
        for i, c in enumerate(chave):
            h = (h * 31 + ord(c)) % self._capacidade
        return h

    def inserir(self, chave: str, valor) -> None:
        idx = self._hash(chave)
        for par in self._baldes[idx]:
            if par[0] == chave:
                par[1] = valor
                return
        self._baldes[idx].append([chave, valor])
        self._tamanho += 1

    def buscar(self, chave: str):
        idx = self._hash(chave)
        for par in self._baldes[idx]:
            if par[0] == chave:
                return par[1]
        return None

    def remover(self, chave: str) -> bool:
        idx = self._hash(chave)
        for i, par in enumerate(self._baldes[idx]):
            if par[0] == chave:
                self._baldes[idx].pop(i)
                self._tamanho -= 1
                return True
        return False

    def todas(self) -> list:
        return [par[1] for balde in self._baldes for par in balde]

    @property
    def tamanho(self) -> int:
        return self._tamanho

    def exibir_estrutura(self):
        print("\n  Estrutura interna da Tabela Hash:")
        for i, balde in enumerate(self._baldes):
            if balde:
                nomes = ", ".join(f"'{p[0]}'" for p in balde)
                col = " (COLISÃO)" if len(balde) > 1 else ""
                print(f"    [{i:02d}] → {nomes}{col}")


# ════════════════════════════════════════════════════════════
#  GRAFO DE DEPENDÊNCIAS
# ════════════════════════════════════════════════════════════

class GrafoDependencias:
    """
    Grafo dirigido: aresta A → B significa "A deve ser feita antes de B".
    Usado para descobrir a ordem de execução e o caminho crítico.
    """

    def __init__(self):
        self._adj: dict[str, list[str]] = {}

    def adicionar_atividade(self, nome: str) -> None:
        if nome not in self._adj:
            self._adj[nome] = []

    def adicionar_dependencia(self, antes: str, depois: str) -> None:
        """'antes' deve ser concluída antes de 'depois'."""
        self.adicionar_atividade(antes)
        self.adicionar_atividade(depois)
        if depois not in self._adj[antes]:
            self._adj[antes].append(depois)

    def dependencias_de(self, nome: str) -> list[str]:
        """Retorna atividades que precisam ocorrer antes de 'nome'."""
        return [a for a, deps in self._adj.items() if nome in deps]

    # ── BFS: todas atividades bloqueadas por uma ─────────────────────────────
    def bfs_bloqueadas(self, origem: str) -> list[str]:
        """
        BFS a partir de 'origem': encontra todas as atividades
        que dependem (direta ou indiretamente) de 'origem'.
        """
        if origem not in self._adj:
            return []
        visitados: set[str] = {origem}
        fila: deque[str] = deque([origem])
        bloqueadas: list[str] = []

        while fila:
            atual = fila.popleft()
            for vizinho in self._adj[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    bloqueadas.append(vizinho)
                    fila.append(vizinho)
        return bloqueadas

    # ── RECURSÃO: tempo total de uma cadeia de atividades ─────────────────────
    def tempo_total_recursivo(self, nome: str, tabela: "TabelaHash",
                              visitados: set | None = None) -> float:
        """
        Calcula recursivamente a soma de horas de 'nome' e de todas
        as atividades que dependem dela (cadeia de dependências).
        """
        if visitados is None:
            visitados = set()
        if nome in visitados:
            return 0.0
        visitados.add(nome)

        atividade = tabela.buscar(nome)
        horas_proprias = atividade.duracao_horas if atividade else 0.0

        horas_dependentes = sum(
            self.tempo_total_recursivo(dep, tabela, visitados)
            for dep in self._adj.get(nome, [])
        )
        return horas_proprias + horas_dependentes

    # ── RECURSÃO: caminho crítico (maior sequência de dependências) ───────────
    def caminho_critico(self, nome: str, tabela: "TabelaHash",
                         visitados: set | None = None) -> list[str]:
        """
        Encontra recursivamente o caminho mais longo (em horas)
        a partir de 'nome' pelas dependências.
        """
        if visitados is None:
            visitados = set()
        if nome in visitados or nome not in self._adj:
            return [nome]
        visitados.add(nome)

        if not self._adj[nome]:
            return [nome]

        melhor: list[str] = []
        melhor_horas = -1.0

        for dep in self._adj[nome]:
            sub = self.caminho_critico(dep, tabela, visitados.copy())
            horas = sum(
                (tabela.buscar(n).duracao_horas if tabela.buscar(n) else 0)
                for n in sub
            )
            if horas > melhor_horas:
                melhor_horas = horas
                melhor = sub

        return [nome] + melhor

    def exibir(self):
        print("\n  Grafo de Dependências:")
        for a, deps in sorted(self._adj.items()):
            if deps:
                print(f"    {a} → {', '.join(deps)}")
            else:
                print(f"    {a} (sem dependências)")


# ════════════════════════════════════════════════════════════
#  INTERFACES E DOMÍNIO (Etapa 2 revisada — SOLID mantido)
# ════════════════════════════════════════════════════════════

class IExibivel(ABC):
    @abstractmethod
    def exibir(self): pass

class IAvaliavel(ABC):
    @abstractmethod
    def esta_urgente(self) -> bool: pass
    @abstractmethod
    def esta_atrasada(self) -> bool: pass


class Atividade(IExibivel, IAvaliavel, ABC):
    _total = 0

    def __init__(self, nome: str, duracao_horas: float, prioridade: int):
        self._nome = nome
        self._duracao_horas = duracao_horas
        self._prioridade = prioridade
        self._concluida = False
        Atividade._total += 1

    @property
    def nome(self) -> str: return self._nome
    @property
    def duracao_horas(self) -> float: return self._duracao_horas
    @duracao_horas.setter
    def duracao_horas(self, v: float):
        if v <= 0: raise ValueError("Duração deve ser positiva.")
        self._duracao_horas = v
    @property
    def prioridade(self) -> int: return self._prioridade
    @property
    def concluida(self) -> bool: return self._concluida
    @property
    @abstractmethod
    def tipo(self) -> str: pass

    def concluir(self):
        self._concluida = True
        print(f"  ✔ '{self._nome}' concluída!")

    def esta_urgente(self) -> bool:
        return self._prioridade >= 4 and not self._concluida

    def exibir(self):
        status = "✔" if self._concluida else ("⚠" if self.esta_atrasada() else "○")
        print(f"  [{status}] [{self.tipo}] {self._nome}  "
              f"{'★'*self._prioridade}{'☆'*(5-self._prioridade)}  {self._duracao_horas}h")
        self._exibir_extras()

    def _exibir_extras(self): pass

    @classmethod
    def total(cls) -> int: return cls._total


class Tarefa(Atividade):
    def __init__(self, nome, duracao_horas, prioridade, prazo: date):
        super().__init__(nome, duracao_horas, prioridade)
        self._prazo = prazo
    @property
    def tipo(self) -> str: return "TAREFA"
    @property
    def prazo(self) -> date: return self._prazo
    def esta_atrasada(self) -> bool:
        return date.today() > self._prazo and not self._concluida
    def _exibir_extras(self):
        dias = (self._prazo - date.today()).days
        msg = "HOJE!" if dias == 0 else (f"{abs(dias)}d ATRASADA" if dias < 0 else f"{dias}d restantes")
        print(f"       Prazo: {self._prazo.strftime('%d/%m')} — {msg}")

class Compromisso(Atividade):
    def __init__(self, nome, duracao_horas, prioridade, horario, local):
        super().__init__(nome, duracao_horas, prioridade)
        self._horario = horario
        self._local = local
    @property
    def tipo(self) -> str: return "COMPROMISSO"
    def esta_atrasada(self) -> bool: return False
    def _exibir_extras(self):
        print(f"       {self._horario} | {self._local}")

class HabitoSaude(Atividade):
    def __init__(self, nome, duracao_horas, prioridade, frequencia_semanal):
        super().__init__(nome, duracao_horas, prioridade)
        self._frequencia = frequencia_semanal
        self._realizacoes = 0
    @property
    def tipo(self) -> str: return "HÁBITO"
    def esta_atrasada(self) -> bool: return False
    def registrar(self):
        self._realizacoes += 1
    def meta_atingida(self) -> bool:
        return self._realizacoes >= self._frequencia
    def _exibir_extras(self):
        meta = "✔ meta!" if self.meta_atingida() else f"{self._realizacoes}/{self._frequencia}x"
        print(f"       Frequência: {self._frequencia}x/semana — {meta}")


# ════════════════════════════════════════════════════════════
#  SISTEMA PRINCIPAL — integra Tabela Hash + Grafo
# ════════════════════════════════════════════════════════════

class SistemaRotina:
    """
    Integra TabelaHash (busca O(1)) e GrafoDependencias (BFS + recursão).
    Princípio D do SOLID: depende de Atividade abstrata.
    """

    def __init__(self, dono: str):
        self._dono = dono
        self._tabela = TabelaHash()
        self._grafo = GrafoDependencias()

    def adicionar(self, atividade: Atividade) -> None:
        self._tabela.inserir(atividade.nome, atividade)
        self._grafo.adicionar_atividade(atividade.nome)
        print(f"  + '{atividade.nome}' adicionada [{atividade.tipo}]")

    def definir_dependencia(self, antes: str, depois: str) -> None:
        """'antes' deve ser concluída antes de 'depois'."""
        self._grafo.adicionar_dependencia(antes, depois)

    def buscar(self, nome: str) -> Atividade | None:
        return self._tabela.buscar(nome)

    # ── BFS ───────────────────────────────────────────────────────────────────
    def o_que_depende_de(self, nome: str) -> None:
        bloqueadas = self._grafo.bfs_bloqueadas(nome)
        print(f"\n  BFS — atividades que dependem de '{nome}':")
        if bloqueadas:
            for b in bloqueadas:
                print(f"    → {b}")
        else:
            print("    (nenhuma)")

    # ── Recursão: tempo de cadeia ─────────────────────────────────────────────
    def tempo_cadeia(self, nome: str) -> None:
        total = self._grafo.tempo_total_recursivo(nome, self._tabela)
        print(f"\n  Recursão — tempo total da cadeia a partir de '{nome}': {total:.1f}h")

    # ── Recursão: caminho crítico ─────────────────────────────────────────────
    def caminho_critico(self, nome: str) -> None:
        caminho = self._grafo.caminho_critico(nome, self._tabela)
        horas = sum(
            (self._tabela.buscar(n).duracao_horas if self._tabela.buscar(n) else 0)
            for n in caminho
        )
        print(f"\n  Caminho crítico a partir de '{nome}':")
        print("    " + " → ".join(caminho))
        print(f"    Total: {horas:.1f}h")

    def urgentes(self) -> list[Atividade]:
        return sorted([a for a in self._tabela.todas() if a.esta_urgente()],
                      key=lambda a: -a.prioridade)

    def atrasadas(self) -> list[Atividade]:
        return [a for a in self._tabela.todas() if a.esta_atrasada()]

    def listar_todas(self):
        print(f"\n  Atividades de {self._dono}:")
        for a in sorted(self._tabela.todas(), key=lambda x: -x.prioridade):
            a.exibir()

    def exibir_grafo(self):
        self._grafo.exibir()

    def exibir_tabela_hash(self):
        self._tabela.exibir_estrutura()

    def estatisticas(self):
        todas = self._tabela.todas()
        total = len(todas)
        concluidas = sum(1 for a in todas if a.concluida)
        carga = sum(a.duracao_horas for a in todas if not a.concluida)
        print(f"\n{'='*45}")
        print(f"  ESTATÍSTICAS — {self._dono}")
        print(f"{'='*45}")
        print(f"  Atividades : {total} ({concluidas} concluídas)")
        print(f"  Carga total: {carga:.1f}h restantes")
        print(f"  Hash slots : {self._tabela.tamanho} entradas")
        urgentes = self.urgentes()
        atrasadas = self.atrasadas()
        if urgentes:
            print(f"  Urgentes   : {len(urgentes)}")
        if atrasadas:
            print(f"  Atrasadas  : {len(atrasadas)}")


# ════════════════════════════════════════════════════════════
#  DEMONSTRAÇÃO
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":

    sistema = SistemaRotina("Camila Ferreira")

    # Adicionando atividades
    print("--- Adicionando atividades ---")
    estagio    = Compromisso("Estágio na clínica",      4, 5, "08h–12h", "Clínica Norte")
    aulas      = Compromisso("Aulas de Psicologia",     3, 4, "14h–17h", "Faculdade")
    pesquisa   = Compromisso("Reunião de pesquisa",     2, 4, "18h–20h", "Online")
    academia   = HabitoSaude("Academia",                1, 3, 3)
    relatorio  = Tarefa("Relatório de estágio",         2, 4, date(2026, 5, 27))
    trabalho   = Tarefa("Trabalho Psicologia Social",   3, 5, date(2026, 5, 22))
    revisao    = Tarefa("Revisão para prova",           3, 4, date(2026, 5, 30))
    prova      = Tarefa("Prova de Psicologia Social",   2, 5, date(2026, 6, 2))

    for a in [estagio, aulas, pesquisa, academia, relatorio, trabalho, revisao, prova]:
        sistema.adicionar(a)

    # Definindo dependências (grafo dirigido)
    print("\n--- Definindo dependências ---")
    sistema.definir_dependencia("Estágio na clínica",    "Relatório de estágio")
    sistema.definir_dependencia("Aulas de Psicologia",   "Revisão para prova")
    sistema.definir_dependencia("Revisão para prova",    "Prova de Psicologia Social")
    sistema.definir_dependencia("Trabalho Psicologia Social", "Prova de Psicologia Social")

    # Listagem
    sistema.listar_todas()

    # ── Algoritmos ────────────────────────────────────────────────────────────
    print("\n" + "="*50)
    print("  ALGORITMOS")
    print("="*50)

    # BFS
    sistema.o_que_depende_de("Aulas de Psicologia")
    sistema.o_que_depende_de("Estágio na clínica")

    # Recursão: tempo da cadeia
    sistema.tempo_cadeia("Estágio na clínica")
    sistema.tempo_cadeia("Aulas de Psicologia")

    # Recursão: caminho crítico
    sistema.caminho_critico("Aulas de Psicologia")

    # Grafo e Hash
    sistema.exibir_grafo()
    sistema.exibir_tabela_hash()

    # Busca O(1)
    print("\n  Busca na tabela hash:")
    encontrada = sistema.buscar("Revisão para prova")
    print(f"    buscar('Revisão para prova') → {encontrada.nome} [{encontrada.tipo}]")
    print(f"    buscar('inexistente')        → {sistema.buscar('inexistente')}")

    # Conclusão e estatísticas
    print("\n--- Concluindo atividades ---")
    estagio.concluir()
    academia.registrar()
    academia.registrar()
    academia.registrar()

    sistema.estatisticas()
    print(f"\n  Total de atividades criadas: {Atividade.total()}")
