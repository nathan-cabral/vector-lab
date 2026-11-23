"""Janela principal do Vector Lab."""

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from educativo import explicar
from graficos import criar_figura


OPERACOES = {
    "Soma": "soma", "Subtração": "subtracao",
    "Vetor × escalar": "multiplicacao_escalar", "Módulo": "modulo",
    "Normalização": "normalizacao", "Produto escalar": "produto_escalar",
    "Produto vetorial (3D)": "produto_vetorial", "Ângulo": "angulo",
    "Projeção de A sobre B": "projecao",
}
UNARIAS = {"modulo", "normalizacao", "multiplicacao_escalar"}


class BarraGrafico(NavigationToolbar2Tk):
    """Barra sem o comando Home, que não atende a este fluxo."""

    toolitems = tuple(item for item in NavigationToolbar2Tk.toolitems
                      if item[0] != "Home")


class VectorLab(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("VECTOR LAB — Calculadora Vetorial")
        self.geometry("1200x760")
        self.minsize(950, 650)
        self.configure(fg_color="#101722")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.canvas = None
        self.barra = None
        self.dados_grafico = None
        self.janela_cheia = None

        lateral = ctk.CTkScrollableFrame(self, width=300, fg_color="#1c2635")
        lateral.grid(row=0, column=0, sticky="nsew")
        lateral.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(lateral, text="VECTOR LAB", font=("Segoe UI", 25, "bold"),
                     text_color="#55c7ff").grid(row=0, column=0, padx=20, pady=(25, 2), sticky="w")
        ctk.CTkLabel(lateral, text="GEOMETRIA VETORIAL  •  2D / 3D",
                     text_color="#95a5ba").grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        self.modo = ctk.CTkSegmentedButton(lateral, values=["2D", "3D"],
                                            command=self._mudar_modo)
        self.modo.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        self.modo.set("2D")

        self.campos = {}
        for linha, nome, iniciais in ((3, "A", ("3", "2", "0")),
                                      (4, "B", ("2", "4", "0"))):
            caixa = ctk.CTkFrame(lateral, fg_color="#263345")
            caixa.grid(row=linha, column=0, padx=20, pady=6, sticky="ew")
            ctk.CTkLabel(caixa, text=f"VETOR {nome}", font=("Segoe UI", 12, "bold"),
                         text_color="#55c7ff" if nome == "A" else "#ffb65c").pack(
                             anchor="w", padx=12, pady=(10, 4))
            faixa = ctk.CTkFrame(caixa, fg_color="transparent")
            faixa.pack(fill="x", padx=10, pady=(0, 10))
            self.campos[nome] = {}
            for eixo, inicial in zip("xyz", iniciais):
                grupo = ctk.CTkFrame(faixa, fg_color="transparent")
                grupo.pack(side="left", expand=True, fill="x", padx=2)
                ctk.CTkLabel(grupo, text=eixo.upper()).pack()
                campo = ctk.CTkEntry(grupo, width=64, justify="center")
                campo.insert(0, inicial)
                campo.pack(fill="x")
                self.campos[nome][eixo] = (grupo, campo)

        ctk.CTkLabel(lateral, text="OPERAÇÃO", font=("Segoe UI", 12, "bold")).grid(
            row=5, column=0, padx=20, pady=(18, 5), sticky="w")
        self.seletor = ctk.CTkOptionMenu(lateral, values=list(OPERACOES),
                                         command=self._mudar_operacao)
        self.seletor.grid(row=6, column=0, padx=20, sticky="ew")
        self.seletor.set("Soma")
        self.rotulo_escalar = ctk.CTkLabel(lateral, text="ESCALAR k")
        self.rotulo_escalar.grid(row=7, column=0, padx=20, pady=(15, 4), sticky="w")
        self.escalar = ctk.CTkEntry(lateral)
        self.escalar.insert(0, "2")
        self.escalar.grid(row=8, column=0, padx=20, sticky="ew")
        ctk.CTkButton(lateral, text="CALCULAR", height=44,
                      font=("Segoe UI", 14, "bold"), command=self.calcular).grid(
                          row=9, column=0, padx=20, pady=(22, 12), sticky="ew")
        ctk.CTkLabel(lateral, text="Ponto ou vírgula decimal.\n"
                     "2D: arraste para mover. 3D: botão esquerdo\n"
                     "gira; botão direito move. Scroll aproxima.",
                     justify="left", text_color="#91a3b8").grid(
                         row=10, column=0, padx=20, pady=(4, 20), sticky="w")

        conteudo = ctk.CTkFrame(self, fg_color="#101722")
        conteudo.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)
        conteudo.grid_columnconfigure(0, weight=1)
        conteudo.grid_rowconfigure(1, weight=3)
        conteudo.grid_rowconfigure(3, weight=2)
        topo = ctk.CTkFrame(conteudo, fg_color="transparent")
        topo.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        topo.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(topo, text="VISUALIZAÇÃO", font=("Segoe UI", 14, "bold"),
                     text_color="#55c7ff").grid(row=0, column=0, sticky="w")
        ctk.CTkButton(topo, text="⛶  TELA CHEIA", width=145,
                      command=self.abrir_tela_cheia).grid(row=0, column=1, sticky="e")
        self.area = ctk.CTkFrame(conteudo, fg_color="#151b26")
        self.area.grid(row=1, column=0, sticky="nsew")
        ctk.CTkLabel(conteudo, text="ENTENDA O CÁLCULO",
                     font=("Segoe UI", 14, "bold"), text_color="#55c7ff").grid(
                         row=2, column=0, sticky="w", pady=(16, 6))
        self.texto = ctk.CTkTextbox(conteudo, fg_color="#1c2635",
                                    font=("Consolas", 13), wrap="word")
        self.texto.grid(row=3, column=0, sticky="nsew")
        self.texto.configure(state="disabled")
        self._mudar_operacao("Soma")
        self.after(150, self.calcular)

    def _mudar_modo(self, modo):
        for nome in ("A", "B"):
            grupo, _ = self.campos[nome]["z"]
            if modo == "3D":
                grupo.pack(side="left", expand=True, fill="x", padx=2)
            else:
                grupo.pack_forget()
        opcoes = list(OPERACOES)
        if modo == "2D":
            opcoes.remove("Produto vetorial (3D)")
            if self.seletor.get() == "Produto vetorial (3D)":
                self.seletor.set("Soma")
        self.seletor.configure(values=opcoes)
        self._mudar_operacao(self.seletor.get())

    def _mudar_operacao(self, escolha):
        operacao = OPERACOES[escolha]
        for _, campo in self.campos["B"].values():
            campo.configure(state="disabled" if operacao in UNARIAS else "normal")
        if operacao == "multiplicacao_escalar":
            self.rotulo_escalar.grid()
            self.escalar.grid()
        else:
            self.rotulo_escalar.grid_remove()
            self.escalar.grid_remove()

    def _ler_vetor(self, nome):
        valores = []
        for eixo in ("x", "y", "z") if self.modo.get() == "3D" else ("x", "y"):
            try:
                valores.append(float(self.campos[nome][eixo][1].get().strip().replace(",", ".")))
            except ValueError as erro:
                raise ValueError(f"Componente {eixo.upper()} de {nome}: informe um número.") from erro
        return valores

    def _mostrar_texto(self, mensagem):
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", mensagem)
        self.texto.configure(state="disabled")

    def calcular(self):
        try:
            nome = OPERACOES[self.seletor.get()]
            a = self._ler_vetor("A")
            b = self._ler_vetor("B") if nome not in UNARIAS else None
            escalar = None
            if nome == "multiplicacao_escalar":
                escalar = float(self.escalar.get().strip().replace(",", "."))
            explicacao = explicar(nome, a, b, escalar)
            figura = criar_figura(nome, a, b, escalar)
        except (ValueError, OverflowError) as erro:
            self._mostrar_texto(f"Verifique os dados: {erro}")
            return

        self.dados_grafico = (nome, a, b, escalar)
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.barra.destroy()
        self.canvas, self.barra = self._montar_grafico(self.area, figura)
        self._mostrar_texto(explicacao.texto())

    def _montar_grafico(self, pai, figura):
        canvas = FigureCanvasTkAgg(figura, master=pai)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        barra = BarraGrafico(canvas, pai, pack_toolbar=False)
        barra.update()
        barra.pack(fill="x")
        if figura.axes[0].name == "rectilinear":
            barra.pan()  # arrastar com o botão esquerdo move o plano 2D
        return canvas, barra

    def abrir_tela_cheia(self):
        if self.dados_grafico is None:
            return
        if self.janela_cheia is not None and self.janela_cheia.winfo_exists():
            self.janela_cheia.lift()
            return
        janela = ctk.CTkToplevel(self)
        self.janela_cheia = janela
        janela.title("VECTOR LAB — Gráfico")
        janela.configure(fg_color="#151b26")
        janela.attributes("-fullscreen", True)
        janela.bind("<Escape>", lambda _: janela.destroy())
        ctk.CTkButton(janela, text="FECHAR TELA CHEIA  (Esc)", width=200,
                      command=janela.destroy).pack(anchor="ne", padx=12, pady=8)
        figura = criar_figura(*self.dados_grafico)
        self._montar_grafico(janela, figura)
