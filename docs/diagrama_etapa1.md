# Diagrama de Classes — Etapa 1
**Rotina Inteligente — Gerenciador da Camila**

## Classes

```
Atividade
─────────────────────────────────
+ nome: str
+ categoria: str
+ duracao_horas: float
+ prioridade: int   (1–5)
+ prazo: date | None
+ concluida: bool
─────────────────────────────────
+ concluir()
+ esta_atrasada() → bool
+ exibir()
─────────────────────────────────
(classe) total_atividades: int


DiaSemana
─────────────────────────────────
+ nome: str
+ atividades: list[Atividade]
─────────────────────────────────
+ adicionar(atividade)
+ carga_total() → float
+ esta_sobrecarregado() → bool
+ exibir()


Rotina
─────────────────────────────────
+ semana: dict[str, DiaSemana]
─────────────────────────────────
+ adicionar(dia, atividade)
+ carga_semanal() → float
+ atividades_urgentes() → list
+ atividades_atrasadas() → list
+ relatorio_semanal()
+ exibir_semana()


Camila
─────────────────────────────────
+ nome: str
+ curso: str
+ semestre: int
+ idade: int
+ rotina: Rotina
─────────────────────────────────
+ exibir_perfil()
+ adicionar_atividade(...) → Atividade
```

## Relacionamentos

```
Camila ──possui──▶ Rotina
Rotina ──contém──▶ DiaSemana (7 dias)
DiaSemana ──agrega──▶ Atividade (0..*)
```
