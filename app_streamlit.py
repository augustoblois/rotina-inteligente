"""
Rotina Inteligente — Interface Streamlit
Etapa 3: Visualização da Rotina da Camila
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import date
from rotina_etapa3 import (
    SistemaRotina, Compromisso, Tarefa, HabitoSaude, Atividade
)


# ── Dados iniciais ─────────────────────────────────────────────────────────────

@st.cache_resource
def criar_sistema():
    s = SistemaRotina("Camila Ferreira")

    estagio   = Compromisso("Estágio na clínica",      4, 5, "08h–12h", "Clínica Norte")
    aulas     = Compromisso("Aulas de Psicologia",     3, 4, "14h–17h", "Faculdade")
    pesquisa  = Compromisso("Reunião de pesquisa",     2, 4, "18h–20h", "Online")
    academia  = HabitoSaude("Academia",                1, 3, 3)
    relatorio = Tarefa("Relatório de estágio",         2, 4, date(2026, 5, 27))
    trabalho  = Tarefa("Trabalho Psicologia Social",   3, 5, date(2026, 5, 22))
    revisao   = Tarefa("Revisão para prova",           3, 4, date(2026, 5, 30))
    prova     = Tarefa("Prova de Psicologia Social",   2, 5, date(2026, 6, 2))

    for a in [estagio, aulas, pesquisa, academia, relatorio, trabalho, revisao, prova]:
        s.adicionar(a)

    s.definir_dependencia("Estágio na clínica",         "Relatório de estágio")
    s.definir_dependencia("Aulas de Psicologia",        "Revisão para prova")
    s.definir_dependencia("Revisão para prova",         "Prova de Psicologia Social")
    s.definir_dependencia("Trabalho Psicologia Social", "Prova de Psicologia Social")

    return s


# ── Visualização do grafo ──────────────────────────────────────────────────────

CORES_TIPO = {
    "COMPROMISSO": "#4C9BE8",
    "TAREFA":      "#E8874C",
    "HÁBITO":      "#6DC46D",
}

def desenhar_grafo(sistema, destaque=None):
    G = nx.DiGraph()
    atividades = sistema._tabela.todas()
    for a in atividades:
        G.add_node(a.nome)
    for nome, deps in sistema._grafo._adj.items():
        for dep in deps:
            G.add_edge(nome, dep)

    fig, ax = plt.subplots(figsize=(9, 5))
    pos = nx.spring_layout(G, seed=7, k=2.0)

    node_colors = []
    node_sizes = []
    for n in G.nodes():
        a = sistema.buscar(n)
        cor = CORES_TIPO.get(a.tipo if a else "", "#AAAAAA")
        node_colors.append(cor)
        node_sizes.append(1200 if n == destaque else 800)

    edge_colors = [
        "#FF4B4B" if destaque and (u == destaque or v == destaque) else "#AAAAAA"
        for u, v in G.edges()
    ]

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True,
                           arrowsize=20, width=2, ax=ax,
                           connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_labels(G, pos, font_size=7, font_color="white",
                            font_weight="bold", ax=ax)

    legend = [mpatches.Patch(color=c, label=t) for t, c in CORES_TIPO.items()]
    ax.legend(handles=legend, loc="lower left", fontsize=8)
    ax.set_title("Grafo de Dependências — Rotina da Camila", fontsize=12)
    ax.axis("off")
    fig.tight_layout()
    return fig


# ── Layout Streamlit ───────────────────────────────────────────────────────────

st.set_page_config(page_title="Rotina da Camila", page_icon="📅", layout="wide")

sistema = criar_sistema()
nomes = [a.nome for a in sorted(sistema._tabela.todas(), key=lambda x: -x.prioridade)]

st.title("📅 Rotina Inteligente — Camila Ferreira")
st.caption("Etapa 3 | Tabela Hash · Grafos · BFS · Recursão · Streamlit")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Atividades", "🔗 Dependências & Algoritmos",
                                   "🗂️ Tabela Hash", "📊 Estatísticas"])


# ════════════════════════════════════════════════════════════
# TAB 1 — Atividades
# ════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Todas as atividades da Camila")

    tipo_filtro = st.selectbox("Filtrar por tipo", ["Todos", "COMPROMISSO", "TAREFA", "HÁBITO"])
    atividades = sistema._tabela.todas()
    if tipo_filtro != "Todos":
        atividades = [a for a in atividades if a.tipo == tipo_filtro]
    atividades = sorted(atividades, key=lambda a: -a.prioridade)

    for a in atividades:
        cor = CORES_TIPO.get(a.tipo, "#AAAAAA")
        status = "✔ Concluída" if a.concluida else ("⚠ Atrasada" if a.esta_atrasada() else "○ Pendente")
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            c1.markdown(f"**{a.nome}**  `{a.tipo}`")
            c2.markdown(f"{'★' * a.prioridade}{'☆' * (5 - a.prioridade)}")
            c3.markdown(f"⏱ {a.duracao_horas}h")
            c4.markdown(status)
            if isinstance(a, Tarefa):
                dias = (a.prazo - date.today()).days
                msg = f"Prazo: {a.prazo.strftime('%d/%m')} "
                msg += "— HOJE!" if dias == 0 else (f"— {abs(dias)}d atrasada" if dias < 0 else f"— {dias}d restantes")
                st.caption(msg)
            elif isinstance(a, Compromisso):
                st.caption(f"{a._horario} | {a._local}")
            elif isinstance(a, HabitoSaude):
                st.caption(f"Meta: {a._frequencia}x/semana — {'✔ atingida' if a.meta_atingida() else f'{a._realizacoes}/{a._frequencia}x'}")

    urgentes = sistema.urgentes()
    if urgentes:
        st.warning(f"⚠ {len(urgentes)} atividade(s) urgente(s): " +
                   ", ".join(a.nome for a in urgentes))

    atrasadas = sistema.atrasadas()
    if atrasadas:
        st.error(f"🔴 {len(atrasadas)} atividade(s) atrasada(s): " +
                 ", ".join(a.nome for a in atrasadas))


# ════════════════════════════════════════════════════════════
# TAB 2 — Dependências & Algoritmos
# ════════════════════════════════════════════════════════════
with tab2:
    col_g, col_alg = st.columns([3, 2])

    with col_g:
        st.subheader("Grafo de Dependências")
        destaque = st.selectbox("Destacar atividade", ["(nenhuma)"] + nomes, key="dest_graf")
        dest = destaque if destaque != "(nenhuma)" else None
        st.pyplot(desenhar_grafo(sistema, destaque=dest))

    with col_alg:
        st.subheader("Algoritmos")

        st.markdown("#### 📡 BFS — o que depende de?")
        origem_bfs = st.selectbox("Atividade:", nomes, key="bfs_orig")
        if st.button("Executar BFS"):
            bloqueadas = sistema._grafo.bfs_bloqueadas(origem_bfs)
            if bloqueadas:
                st.success("Dependem de '" + origem_bfs + "':")
                for b in bloqueadas:
                    st.markdown(f"  → {b}")
            else:
                st.info("Nenhuma atividade depende desta.")

        st.markdown("---")
        st.markdown("#### 🔁 Recursão — tempo da cadeia")
        origem_rec = st.selectbox("Atividade:", nomes, key="rec_orig")
        if st.button("Calcular tempo"):
            total = sistema._grafo.tempo_total_recursivo(origem_rec, sistema._tabela)
            st.success(f"Tempo total da cadeia: **{total:.1f}h**")

        st.markdown("---")
        st.markdown("#### 🎯 Caminho crítico (recursão)")
        origem_cc = st.selectbox("A partir de:", nomes, key="cc_orig")
        if st.button("Calcular caminho"):
            caminho = sistema._grafo.caminho_critico(origem_cc, sistema._tabela)
            horas = sum(
                (sistema.buscar(n).duracao_horas if sistema.buscar(n) else 0)
                for n in caminho
            )
            st.success(" → ".join(caminho))
            st.info(f"Total: **{horas:.1f}h**")


# ════════════════════════════════════════════════════════════
# TAB 3 — Tabela Hash
# ════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Tabela Hash de Atividades")
    tabela = sistema._tabela
    st.markdown(f"Capacidade: **{tabela._capacidade} slots** | Entradas: **{tabela.tamanho}**")
    st.markdown("Colisões resolvidas por **encadeamento (chaining)**.")

    dados = []
    for i, balde in enumerate(tabela._baldes):
        if balde:
            dados.append({
                "Slot": i,
                "hash(chave)": i,
                "Atividades no balde": ", ".join(p[0] for p in balde),
                "Colisão?": "Sim" if len(balde) > 1 else "Não",
            })
    if dados:
        st.table(dados)

    st.markdown("---")
    st.markdown("#### 🔎 Busca direta")
    busca = st.text_input("Nome da atividade:", placeholder="ex: Academia")
    if st.button("Buscar"):
        resultado = tabela.buscar(busca)
        if resultado:
            slot = tabela._hash(busca)
            st.success(f"✔ Encontrada no slot **{slot}** | Tipo: {resultado.tipo} | {resultado.duracao_horas}h | Prioridade: {resultado.prioridade}/5")
        else:
            st.error("Atividade não encontrada na tabela hash.")


# ════════════════════════════════════════════════════════════
# TAB 4 — Estatísticas
# ════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Estatísticas da Rotina")

    todas = sistema._tabela.todas()
    total = len(todas)
    concluidas = sum(1 for a in todas if a.concluida)
    carga = sum(a.duracao_horas for a in todas if not a.concluida)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total de atividades", total)
    c2.metric("Concluídas", concluidas)
    c3.metric("Horas restantes", f"{carga:.0f}h")

    st.markdown("---")
    st.subheader("Por tipo")
    tipos: dict[str, int] = {}
    for a in todas:
        tipos[a.tipo] = tipos.get(a.tipo, 0) + 1
    for t, n in tipos.items():
        icon = {"COMPROMISSO": "📅", "TAREFA": "📝", "HÁBITO": "💪"}.get(t, "")
        st.markdown(f"- {icon} **{t}**: {n}")

    st.markdown("---")
    st.subheader("Ranking por prioridade")
    ranking = sorted(todas, key=lambda a: -a.prioridade)
    dados_rank = [
        {"Atividade": a.nome, "Tipo": a.tipo, "Prioridade": a.prioridade,
         "Duração (h)": a.duracao_horas, "Status": "✔" if a.concluida else ("⚠" if a.esta_atrasada() else "○")}
        for a in ranking
    ]
    st.table(dados_rank)
