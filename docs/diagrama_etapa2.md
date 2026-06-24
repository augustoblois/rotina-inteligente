# Diagrama de Classes — Etapa 2
**Rotina Inteligente (atualizado)**

## Interfaces (ABC)

```
«interface»          «interface»
IExibivel            IAvaliavel
─────────────        ─────────────────────────
+ exibir() [abs]     + esta_urgente() → bool [abs]
                     + esta_atrasada() → bool [abs]
```

## Hierarquia de Atividade

```
              «abstract»
              Atividade  ──implements──▶  IExibivel + IAvaliavel
          ──────────────────────────────────────
          # _nome: str
          # _duracao_horas: float  (setter com validação)
          # _prioridade: int       (setter 1–5)
          # _concluida: bool
          + nome (property)
          + duracao_horas (property + setter)
          + prioridade (property + setter)
          + concluida (property)
          + tipo: str [abs — polimorfismo]
          + concluir()
          + esta_urgente() → bool
          + exibir()
          # _exibir_extras() [hook]
          ──────────────────────────────────────
                △           △           △
                │           │           │
         ┌──────┘      ┌────┘      ┌────┘
         │             │           │
      Tarefa      Compromisso  HabitoSaude
     ──────────   ──────────   ───────────────
     _prazo       _horario     _frequencia
     prazo        _local       _realizacoes
     tipo→TAREFA  tipo→        registrar_realizacao()
     esta_        COMPROMISSO  meta_atingida() → bool
     atrasada()   esta_        tipo→HÁBITO
     dias_        atrasada()
     restantes()  →False
```

## Outras Classes

```
DiaSemana  ──implements──▶  IExibivel
──────────────────────────
# _nome: str
# _atividades: list[Atividade]
+ adicionar(a: Atividade)
+ carga_total() → float
+ esta_sobrecarregado() → bool
+ urgentes() → list[Atividade]
+ exibir()


Rotina
──────────────────────────────────────
# _semana: dict[str, DiaSemana]
+ adicionar(dia, atividade)
+ carga_semanal() → float
+ urgentes() → list[Atividade]
+ atrasadas() → list[Atividade]
+ exibir_semana()
+ relatorio()


Camila
──────────────────────────────────────
# _nome, _curso, _semestre, _idade
# _rotina: Rotina
+ nome, rotina (properties)
+ exibir_perfil()
```

## Princípios SOLID aplicados

| Princípio | Como está no código |
|---|---|
| **S** — Single Responsibility | `Camila` guarda perfil; `Rotina` gerencia atividades; `DiaSemana` agrupa por dia |
| **O** — Open/Closed | `Atividade` é abstrata — novos tipos não alteram a base |
| **L** — Liskov | `Tarefa`, `Compromisso`, `HabitoSaude` substituem `Atividade` sem quebrar o sistema |
| **I** — Interface Segregation | `IExibivel` e `IAvaliavel` separadas; quem precisa de cada contrato |
| **D** — Dependency Inversion | `Rotina` e `DiaSemana` recebem `Atividade` abstrata, não tipos concretos |
