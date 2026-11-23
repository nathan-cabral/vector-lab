"""Figuras Matplotlib 2D/3D prontas para incorporação em uma janela Tk."""

import numpy as np
from matplotlib.figure import Figure

import operacoes as op


CORES = {"A": "#55c7ff", "B": "#ffb65c", "Resultado": "#8ef0af"}
FUNDO = "#151b26"
TEXTO = "#dce7f4"


def _dados(operacao, a, b, escalar):
    """Obtém vetores pela mesma validação e cálculo usados pelo aplicativo."""
    if operacao == "multiplicacao_escalar":
        resultado = op.multiplicacao_escalar(a, escalar)
    elif operacao in ("modulo", "normalizacao"):
        resultado = getattr(op, operacao)(a)
    elif operacao in ("soma", "subtracao", "produto_escalar",
                      "produto_vetorial", "angulo", "projecao"):
        if b is None:
            raise ValueError("Esta operação exige o vetor B.")
        resultado = getattr(op, operacao)(a, b)
    else:
        raise ValueError(f"Operação desconhecida: {operacao}.")

    vetores = {"A": np.asarray(a, dtype=float)}
    if b is not None and operacao not in ("modulo", "normalizacao",
                                           "multiplicacao_escalar"):
        vetores["B"] = np.asarray(b, dtype=float)
    if isinstance(resultado, np.ndarray):
        vetores["Resultado"] = resultado
    return vetores


def criar_figura(operacao, a, b=None, escalar=None):
    """Cria uma Figure sem abrir janela externa.

    A e B partem da origem. O resultado vetorial também parte da origem;
    para soma/subtração há uma linha auxiliar de construção geométrica.
    Produto escalar, módulo e ângulo são escalares e não criam seta resultante.
    """
    vetores = _dados(operacao, a, b, escalar)
    dimensao = len(vetores["A"])
    figura = Figure(figsize=(7, 5), dpi=100, facecolor=FUNDO)
    eixo = figura.add_subplot(111, projection="3d" if dimensao == 3 else None)
    eixo.set_facecolor(FUNDO)
    figura.subplots_adjust(left=0.12, right=0.94, bottom=0.12, top=0.9)

    maior = max(float(np.max(np.abs(v))) for v in vetores.values())
    limite = max(1.0, maior * 1.3)
    origem = np.zeros(dimensao)

    for nome, vetor in vetores.items():
        cor = CORES[nome]
        if dimensao == 2:
            if np.any(vetor):
                eixo.annotate("", xy=vetor, xytext=origem,
                              arrowprops={"arrowstyle": "-|>", "color": cor,
                                          "lw": 2.5, "mutation_scale": 16})
            else:
                eixo.plot([0], [0], marker="o", color=cor)
            eixo.text(vetor[0], vetor[1],
                      f" {nome} ({vetor[0]:.3g}, {vetor[1]:.3g})", color=cor)
            eixo.plot([], [], color=cor, lw=2.5, label=nome)
        else:
            if np.any(vetor):
                eixo.quiver(*origem, *vetor, color=cor, arrow_length_ratio=0.1,
                            linewidth=2.5, label=nome)
            else:
                eixo.scatter(*origem, color=cor, label=nome)
            eixo.text(*vetor, f" {nome} ({', '.join(f'{x:.3g}' for x in vetor)})",
                      color=cor)

    if operacao in ("soma", "subtracao"):
        a_v, b_v = vetores["A"], vetores["B"]
        inicio = a_v if operacao == "soma" else b_v
        fim = vetores["Resultado"] if operacao == "soma" else a_v
        if dimensao == 2:
            eixo.plot([inicio[0], fim[0]], [inicio[1], fim[1]],
                      "--", color=CORES["B" if operacao == "soma" else "A"], alpha=0.7)
        else:
            eixo.plot([inicio[0], fim[0]], [inicio[1], fim[1]],
                      [inicio[2], fim[2]], "--", color=CORES["B" if operacao == "soma" else "A"], alpha=0.7)

    if operacao == "angulo":
        a_v, b_v = vetores["A"], vetores["B"]
        unidade_a = a_v / np.linalg.norm(a_v)
        unidade_b = b_v / np.linalg.norm(b_v)
        graus = op.angulo(a_v, b_v)
        radianos = np.linspace(0, np.radians(graus), 80)
        if dimensao == 2:
            sentido = np.sign(np.linalg.det(np.stack((unidade_a, unidade_b))))
            if sentido == 0:
                sentido = 1
            perpendicular = sentido * np.array([-unidade_a[1], unidade_a[0]])
        else:
            componente = unidade_b - np.dot(unidade_b, unidade_a) * unidade_a
            if np.linalg.norm(componente) < 1e-12:
                base = np.eye(3)[np.argmin(np.abs(unidade_a))]
                componente = base - np.dot(base, unidade_a) * unidade_a
            perpendicular = componente / np.linalg.norm(componente)
        raio = max(0.25, min(np.linalg.norm(a_v), np.linalg.norm(b_v)) * 0.28)
        pontos = raio * (np.outer(np.cos(radianos), unidade_a)
                         + np.outer(np.sin(radianos), perpendicular))
        meio = raio * (np.cos(radianos[len(radianos) // 2]) * unidade_a
                       + np.sin(radianos[len(radianos) // 2]) * perpendicular)
        if dimensao == 2:
            eixo.plot(pontos[:, 0], pontos[:, 1], color="#ffe584", lw=2.5)
            eixo.text(*meio, f"  θ = {graus:.3g}°", color="#ffe584")
        else:
            eixo.plot(pontos[:, 0], pontos[:, 1], pontos[:, 2],
                      color="#ffe584", lw=2.5)
            eixo.text(*meio, f"  θ = {graus:.3g}°", color="#ffe584")

    eixo.set_xlim(-limite, limite)
    eixo.set_ylim(-limite, limite)
    eixo.set_xlabel("X", color=TEXTO)
    eixo.set_ylabel("Y", color=TEXTO)
    if dimensao == 2:
        eixo.axhline(0, color="#617086", lw=0.8)
        eixo.axvline(0, color="#617086", lw=0.8)
        eixo.grid(True, alpha=0.2)
        eixo.set_aspect("equal", adjustable="box")
    else:
        eixo.set_zlim(-limite, limite)
        eixo.set_zlabel("Z", color=TEXTO)
        eixo.set_box_aspect((1, 1, 1))
        eixo.tick_params(colors=TEXTO)
        for painel in (eixo.xaxis, eixo.yaxis, eixo.zaxis):
            painel.pane.fill = False
    eixo.tick_params(colors=TEXTO)
    eixo.set_title(operacao.replace("_", " ").title(), color=TEXTO)
    eixo.legend(loc="upper left", facecolor=FUNDO, edgecolor="#617086",
                labelcolor=TEXTO)
    return figura
