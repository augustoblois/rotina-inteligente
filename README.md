# Rotina Inteligente

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Stdlib only](https://img.shields.io/badge/deps-stdlib%20only-success)

Projeto acadêmico de **Princípios de Programação** (UFPB).

Tema: **Rotina Inteligente** — gerenciador de atividades para a persona **Camila**, estudante de Psicologia. O domínio (a rotina e as atividades da Camila) é o mesmo nas duas etapas, mas cada etapa o **reimplementa do zero** num nível maior de sofisticação de POO.

## Etapas

Cada etapa é um arquivo **standalone e auto-contido** — a etapa 2 não importa a etapa 1. São versões progressivamente mais avançadas do mesmo domínio.

| Etapa | Arquivo | Foco | Classes principais |
|-------|---------|------|--------------------|
| 1 | `src/rotina_etapa1.py` | Classes e objetos básicos | `Atividade`, `DiaSemana`, `Rotina`, `Camila` |
| 2 | `src/rotina_etapa2.py` | POO avançada + SOLID | `Atividade` (ABC), `Tarefa`, `Compromisso`, `HabitoSaude`, `DiaSemana`, `Rotina`, `Camila` |

### Etapa 1 — fundamentos
Uma única classe `Atividade` (o tipo é um campo de texto `categoria`), atributos públicos, sem validação. Agrupamento em `DiaSemana` → `Rotina` → `Camila`.

### Etapa 2 — POO avançada
`Atividade` vira **classe abstrata** (`ABC`) que implementa as interfaces `IExibivel` e `IAvaliavel`, com 3 subclasses concretas:

- **`Tarefa`** — tem prazo
- **`Compromisso`** — tem horário e local
- **`HabitoSaude`** — tem frequência

Conceitos demonstrados:
- **Encapsulamento** — `@property` + setters com validação (`_nome`, `_prioridade`)
- **Polimorfismo** — `tipo`, `esta_atrasada()`, `_exibir_extras()` sobrescritos por subclasse
- **Abstração / herança / interfaces** — `ABC`, `IExibivel`, `IAvaliavel`
- Os **5 princípios SOLID** são o eixo do design

## Como rodar

Requer **Python 3.11+** (testado em 3.13). Sem build system, sem dependências externas — só a stdlib. Cada arquivo tem um bloco `if __name__ == "__main__"` com uma demonstração que imprime no terminal.

```bash
python src/rotina_etapa1.py   # etapa 1
python src/rotina_etapa2.py   # etapa 2
```

> **Datas da demo são hardcoded** (`date(2026, ...)`). Como `esta_atrasada()` compara com `date.today()`, o output muda conforme o dia em que roda.

## Estrutura

```
.
├── src/                    # código por etapa
│   ├── rotina_etapa1.py
│   └── rotina_etapa2.py
└── docs/                   # diagramas de classe + slides
    ├── diagrama_etapa1.md
    ├── diagrama_etapa2.md
    ├── slides-etapa1.pdf
    └── slides-etapa2.pdf
```

Os diagramas de classe (Mermaid) de cada etapa estão em `docs/`.
