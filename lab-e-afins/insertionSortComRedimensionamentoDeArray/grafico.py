import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# ─── Paleta (espelha o Cliente.py) ────────────────────────
BG      = "#1e1e2e"
PAINEL  = "#2a2a3e"
BORDA   = "#45475a"
ACENTO  = "#7c6af7"
TEXTO   = "#cdd6f4"
TEXTO2  = "#6c7086"
VERDE   = "#a6e3a1"
VERMELHO= "#f38ba8"


def mostrarGrafico(historico: list) -> None:
    """
    Exibe um gráfico de linha (tempo) + barras (elementos),
    com anotação do nome do arquivo em cada ponto.
    """
    plt.style.use("dark_background")
    fig, ax1 = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(BG)
    ax1.set_facecolor(PAINEL)

    execucoes = [h["execucao"]   for h in historico]
    tempos    = [h["tempo"]      for h in historico]
    qtds      = [h["quantidade"] for h in historico]
    arquivos  = [h["arquivo"]    for h in historico]

    # ── Eixo secundário: barras de nº de elementos ──────────
    ax2 = ax1.twinx()
    ax2.bar(execucoes, qtds, color=VERMELHO, alpha=0.18,
            zorder=2, width=0.55, label="Nº de elementos")
    ax2.set_ylabel("Nº de elementos", color=VERMELHO, fontsize=10)
    ax2.tick_params(axis="y", labelcolor=VERMELHO)
    ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    for sp in ax2.spines.values():
        sp.set_color(BORDA)

    # ── Eixo principal: linha de tempo ───────────────────────
    ax1.plot(execucoes, tempos,
             color=ACENTO, linewidth=2.5,
             marker="o", markersize=9,
             zorder=5, label="Tempo (s)")
    ax1.fill_between(execucoes, tempos,
                     alpha=0.08, color=ACENTO, zorder=3)

    # ── Anotações: nome do arquivo sobre cada ponto ──────────
    for x, y, arq in zip(execucoes, tempos, arquivos):
        ax1.annotate(
            arq,
            xy=(x, y),
            xytext=(0, 16),
            textcoords="offset points",
            ha="center",
            fontsize=7.5,
            color=TEXTO,
            alpha=0.90,
            bbox=dict(boxstyle="round,pad=0.35",
                      fc=PAINEL, ec=BORDA, lw=0.8)
        )

    # ── Estilo do eixo principal ─────────────────────────────
    ax1.set_xlabel("Execução nº", color=TEXTO, fontsize=10)
    ax1.set_ylabel("Tempo (s)",   color=ACENTO, fontsize=10)
    ax1.tick_params(colors=TEXTO, labelcolor=TEXTO)
    ax1.tick_params(axis="y", labelcolor=ACENTO)
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax1.grid(True, linestyle="--", alpha=0.22, color=BORDA, zorder=0)
    ax1.set_axisbelow(True)
    for sp in ax1.spines.values():
        sp.set_color(BORDA)

    # ── Legenda combinada ────────────────────────────────────
    handles = [
        Line2D([0], [0], color=ACENTO, lw=2.5,
               marker="o", markersize=8, label="Tempo (s)"),
        Patch(color=VERMELHO, alpha=0.4, label="Nº de elementos"),
    ]
    ax1.legend(handles=handles, loc="upper left",
               facecolor=PAINEL, edgecolor=BORDA,
               labelcolor=TEXTO, fontsize=9)

    plt.title("Histórico de Ordenações — Insertion Sort",
              color=TEXTO, fontsize=13, pad=18)
    fig.tight_layout(pad=2.2)
    plt.show()