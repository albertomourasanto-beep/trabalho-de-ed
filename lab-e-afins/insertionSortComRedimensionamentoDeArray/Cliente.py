import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import os

from array_dinamico import ArrayDinamico
from carregar_arquivo import carregarArquivo
from insertion_sort import insertionSort
from selection_sort import selectionsort
from grafico import mostrarGrafico

# ─────────────────────────────────────────────────────────────
#  Paleta de cores (tema escuro Catppuccin-inspirado)
# ─────────────────────────────────────────────────────────────
BG       = "#1e1e2e"
PAINEL   = "#2a2a3e"
BORDA    = "#45475a"
ACENTO   = "#7c6af7"
TEXTO    = "#cdd6f4"
TEXTO2   = "#6c7086"
VERDE    = "#a6e3a1"
VERMELHO = "#f38ba8"
BTN_BG   = "#313244"
BTN_HOV  = "#45475a"

FONTE        = ("Segoe UI", 10)
FONTE_BOLD   = ("Segoe UI", 10, "bold")
FONTE_TITULO = ("Segoe UI", 14, "bold")
FONTE_MONO   = ("Consolas", 10)


# ─────────────────────────────────────────────────────────────
#  Componente de botão com hover
# ─────────────────────────────────────────────────────────────
class BotaoModerno(tk.Button):
    def __init__(self, parent, cor_texto=None, **kw):
        super().__init__(
            parent,
            bg=BTN_BG,
            fg=cor_texto or TEXTO,
            activebackground=BTN_HOV,
            activeforeground=cor_texto or TEXTO,
            font=FONTE,
            relief="flat",
            bd=0,
            padx=14,
            pady=9,
            cursor="hand2",
            **kw
        )
        self._cor = cor_texto or TEXTO
        self.bind("<Enter>", lambda _: self.config(bg=BTN_HOV))
        self.bind("<Leave>", lambda _: self.config(bg=BTN_BG))


# ─────────────────────────────────────────────────────────────
#  Aplicação principal
# ─────────────────────────────────────────────────────────────
class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Insertion Sort — Visualizador")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ── Estado ───────────────────────────────────────────
        self.arrayPrincipal  = ArrayDinamico()
        self.arrayOrdenado   = None
        self.tempoOrdenacao  = 0.0
        self.arquivoAtual    = None
        self.historico: list = []

        # variáveis compartilhadas entre threads
        self._progress_val = [0]
        self._sort_done    = False
        self._sort_result  = [None]

        self._build_ui()

    # ─────────────────────────────────────────────────────────
    #  Construção da interface
    # ─────────────────────────────────────────────────────────
    def _build_ui(self):
        self._configurar_estilos()

        # ── Cabeçalho ────────────────────────────────────────
        frame_header = tk.Frame(self.root, bg=PAINEL)
        frame_header.pack(fill="x")

        tk.Label(frame_header, text="  Insertion Sort",
                font=FONTE_TITULO, bg=PAINEL, fg=ACENTO,
                pady=14).pack(side="left")
        tk.Label(frame_header, text="Visualizador de ordenações",
                font=("Segoe UI", 9), bg=PAINEL, fg=TEXTO2,
                pady=14).pack(side="left", padx=(6, 0))

        # ── Área de saída ─────────────────────────────────────
        frame_texto = tk.Frame(self.root, bg=BORDA)
        frame_texto.pack(padx=18, pady=(14, 4), fill="both")

        scroll = tk.Scrollbar(frame_texto)
        scroll.pack(side="right", fill="y")

        self.texto = tk.Text(
            frame_texto,
            height=16, width=64,
            bg=PAINEL, fg=TEXTO,
            font=FONTE_MONO,
            insertbackground=TEXTO,
            relief="flat",
            padx=12, pady=10,
            selectbackground=ACENTO,
            yscrollcommand=scroll.set,
            state="normal"
        )
        self.texto.pack(padx=1, pady=1)
        scroll.config(command=self.texto.yview)

        # ── Label do arquivo ──────────────────────────────────
        self.lbl_arquivo = tk.Label(
            self.root,
            text="⬜  Nenhum arquivo carregado",
            font=("Segoe UI", 9), bg=BG, fg=TEXTO2
        )
        self.lbl_arquivo.pack(pady=(2, 0))

        # ── Barra de progresso ────────────────────────────────
        frame_prog = tk.Frame(self.root, bg=BG)
        frame_prog.pack(padx=18, pady=(8, 2), fill="x")

        tk.Label(frame_prog, text="Progresso  ",
                font=("Segoe UI", 9), bg=BG, fg=TEXTO2).pack(side="left")

        self.progress_bar = ttk.Progressbar(
            frame_prog,
            orient="horizontal",
            length=1,
            mode="determinate",
            style="App.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(side="left", fill="x", expand=True)

        self.lbl_pct = tk.Label(
            frame_prog, text="  0%",
            font=("Segoe UI", 9, "bold"),
            bg=BG, fg=ACENTO, width=5
        )
        self.lbl_pct.pack(side="left")

        # ── Grade de botões ───────────────────────────────────
        frame_btns = tk.Frame(self.root, bg=BG)
        frame_btns.pack(padx=18, pady=(12, 14))

        self._botoes: list[tk.Button] = []

        def btn(text, cmd, row, col, cor=None):
            b = BotaoModerno(frame_btns, text=text, command=cmd, cor_texto=cor)
            b.grid(row=row, column=col, padx=5, pady=4, sticky="ew")
            self._botoes.append(b)
            return b

        btn("📂  Carregar Arquivo",  self.carregar,        0, 0)
        btn("⚡  Ordenar por insertion", self.ordenaris,         0, 1, ACENTO)
        btn("⚡  Ordenar por selection", self.ordenarses,  0, 2, ACENTO)
        btn("📋  Listar Original",  self.listar_original, 1, 0)
        btn("✅  Listar Ordenado",  self.listar_ordenado, 1, 1)
        btn("📊  Estatísticas",     self.estatisticas,    1, 2)
        btn("📈  Gráfico",          self.mostrar_grafico, 2, 0, VERDE)
        btn("✖  Sair",             self.root.quit,       2, 2, VERMELHO)

        for c in range(3):
            frame_btns.columnconfigure(c, weight=1)

        # ── Barra de status ───────────────────────────────────
        self.lbl_status = tk.Label(
            self.root,
            text="Pronto.",
            font=("Segoe UI", 8),
            bg=BORDA, fg=TEXTO2,
            anchor="w", padx=10, pady=3
        )
        self.lbl_status.pack(fill="x", side="bottom")

        self._escrever(
            "Bem-vindo!\n\n"
            "  1. Carregue um arquivo .txt com um nome por linha.\n"
            "  2. Clique em Ordenar para executar o Insertion Sort.\n"
            "  3. Use Estatísticas e Gráfico para analisar o desempenho.\n\n"
            "  Dica: faça múltiplas ordenações com arquivos diferentes\n"
            "  para comparar os tempos no gráfico."
        )

    # ─────────────────────────────────────────────────────────
    #  Estilos ttk
    # ─────────────────────────────────────────────────────────
    def _configurar_estilos(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure(
            "App.Horizontal.TProgressbar",
            troughcolor=PAINEL,
            background=ACENTO,
            bordercolor=BORDA,
            lightcolor=ACENTO,
            darkcolor=ACENTO,
            thickness=12
        )

    # ─────────────────────────────────────────────────────────
    #  Helpers de UI
    # ─────────────────────────────────────────────────────────
    def _escrever(self, msg: str):
        self.texto.config(state="normal")
        self.texto.delete(1.0, tk.END)
        self.texto.insert(tk.END, msg)

    def _status(self, msg: str, cor: str = TEXTO2):
        self.lbl_status.config(text=msg, fg=cor)

    def _set_botoes(self, estado: str):
        for b in self._botoes:
            b.config(state=estado)

    def _set_progresso(self, valor: int):
        self.progress_bar["value"] = valor
        self.lbl_pct.config(text=f"{valor:>3}%")

    # ─────────────────────────────────────────────────────────
    #  Ações dos botões
    # ─────────────────────────────────────────────────────────
    def carregar(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos", "*.*")]
        )
        if not caminho:
            return

        self.arrayPrincipal = ArrayDinamico()
        carregarArquivo(caminho, self.arrayPrincipal)
        self.arrayOrdenado  = None
        self.arquivoAtual   = os.path.basename(caminho)

        self._set_progresso(0)
        self.lbl_arquivo.config(
            text=f"🟢  {self.arquivoAtual}  —  "
                f"{self.arrayPrincipal.getQuantidade()} elementos",
            fg=VERDE
        )
        self._escrever(
            f"✔  Arquivo carregado com sucesso!\n\n"
            f"   Nome     : {self.arquivoAtual}\n"
            f"   Elementos: {self.arrayPrincipal.getQuantidade()}\n\n"
            f"Clique em Ordenar quando estiver pronto."
        )
        self._status(f"Carregado: {self.arquivoAtual}", VERDE)

    # ── Ordenar (executa em thread separada) ──────────────────
    def ordenaris(self):
        if self.arrayPrincipal.getQuantidade() == 0:
            messagebox.showwarning("Atenção", "Carregue um arquivo primeiro!")
            return

        # Reinicia estado de progresso
        self._progress_val[0] = 0
        self._sort_done       = False
        self._sort_result[0]  = None

        self._set_progresso(0)
        self._set_botoes("disabled")
        self._status("Ordenando…", ACENTO)
        self._escrever("⏳  Ordenação em andamento, aguarde…")

        def _tarefa():
            def _cb(i, total):
                self._progress_val[0] = int((i / total) * 100)

            t0     = time.time()
            result = insertionSort(self.arrayPrincipal, _cb)
            t1     = time.time()
            self._sort_result[0] = (result, t1 - t0)
            self._sort_done      = True

        threading.Thread(target=_tarefa, daemon=True).start()
        self._monitorar_progresso()
    def ordenarses(self):
        if self.arrayPrincipal.getQuantidade() == 0:
            messagebox.showwarning("Atenção", "Carregue um arquivo primeiro!")
            return

        # Reinicia estado de progresso
        self._progress_val[0] = 0
        self._sort_done       = False
        self._sort_result[0]  = None

        self._set_progresso(0)
        self._set_botoes("disabled")
        self._status("Ordenando…", ACENTO)
        self._escrever("⏳  Ordenação em andamento, aguarde…")

        def _tarefa():
            def _cb(i, total):
                self._progress_val[0] = int((i / total) * 100)

            t0     = time.time()
            result = selectionsort(self.arrayPrincipal, _cb)
            t1     = time.time()
            self._sort_result[0] = (result, t1 - t0)
            self._sort_done      = True

        threading.Thread(target=_tarefa, daemon=True).start()
        self._monitorar_progresso()
    def _monitorar_progresso(self):
        if not self._sort_done:
            v = self._progress_val[0]
            self._set_progresso(v)
            self.root.after(40, self._monitorar_progresso)
            return

        # ── Ordenação concluída ───────────────────────────────
        self._set_progresso(100)
        result, tempo = self._sort_result[0]
        self.arrayOrdenado  = result
        self.tempoOrdenacao = tempo

        self.historico.append({
            "execucao"  : len(self.historico) + 1,
            "arquivo"   : self.arquivoAtual or "desconhecido",
            "quantidade": self.arrayPrincipal.getQuantidade(),
            "tempo"     : self.tempoOrdenacao,
        })

        self._set_botoes("normal")
        self._status(f"Concluído em {tempo:.6f}s", VERDE)
        self._escrever(
            f"✔  Ordenação concluída!\n\n"
            f"   Arquivo  : {self.arquivoAtual}\n"
            f"   Elementos: {self.arrayPrincipal.getQuantidade()}\n"
            f"   Tempo    : {tempo:.6f} s\n"
            f"   Execução : #{len(self.historico)}\n\n"
            f"Use Listar Ordenado para ver o resultado,\n"
            f"ou Gráfico para comparar com execuções anteriores."
        )

    # ── Listagens ─────────────────────────────────────────────
    def listar_original(self):
        if self.arrayPrincipal.getQuantidade() == 0:
            self._escrever("⚠  Nenhum dado carregado.")
            return
        self._listar(self.arrayPrincipal,
                    f"Lista Original — {self.arquivoAtual}")

    def listar_ordenado(self):
        if self.arrayOrdenado is None:
            self._escrever("⚠  Execute a ordenação antes de listar o resultado.")
            return
        self._listar(self.arrayOrdenado,
                    f"Lista Ordenada — {self.arquivoAtual}")

    def _listar(self, array: ArrayDinamico, titulo: str):
        linhas = [f"── {titulo} ──\n"]
        for i in range(array.getQuantidade()):
            linhas.append(f"  {i+1:>5}.  {array.getValue(i)}")
        self._escrever("\n".join(linhas))

    # ── Estatísticas ──────────────────────────────────────────
    def estatisticas(self):
        if self.arrayPrincipal.getQuantidade() == 0:
            messagebox.showwarning("Atenção", "Nenhum arquivo carregado.")
            return
        if not self.historico:
            messagebox.showwarning(
                "Atenção",
                "Nenhuma ordenação realizada ainda.\n"
                "Clique em Ordenar primeiro!"
            )
            return

        tempo_med = sum(h["tempo"] for h in self.historico) / len(self.historico)
        tempo_min = min(self.historico, key=lambda h: h["tempo"])
        tempo_max = max(self.historico, key=lambda h: h["tempo"])

        linhas = [
            "── Estatísticas ──────────────────────────────────",
            "",
            f"  Arquivo atual    : {self.arquivoAtual}",
            f"  Elementos        : {self.arrayPrincipal.getQuantidade()}",
            f"  Capacidade array : {self.arrayPrincipal.getTamanho()}",
            "",
            f"  Última ordenação : {self.tempoOrdenacao:.6f} s",
            f"  Tempo médio      : {tempo_med:.6f} s",
            f"  Mais rápida      : {tempo_min['tempo']:.6f} s  "
            f"(#{tempo_min['execucao']} — {tempo_min['arquivo']})",
            f"  Mais lenta       : {tempo_max['tempo']:.6f} s  "
            f"(#{tempo_max['execucao']} — {tempo_max['arquivo']})",
            f"  Total execuções  : {len(self.historico)}",
            "",
            "── Histórico ──────────────────────────────────────",
            "",
        ]

        for h in self.historico:
            linhas.append(
                f"  #{h['execucao']:<3}  {h['arquivo']:<24}"
                f"  {h['quantidade']:>6} elem.   {h['tempo']:.6f} s"
            )

        self._escrever("\n".join(linhas))

    # ── Gráfico ───────────────────────────────────────────────
    def mostrar_grafico(self):
        if not self.historico:
            messagebox.showwarning(
                "Atenção",
                "Nenhuma ordenação registrada.\n"
                "Realize ao menos uma ordenação para gerar o gráfico."
            )
            return
        mostrarGrafico(self.historico)


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = App(root)
    root.mainloop()