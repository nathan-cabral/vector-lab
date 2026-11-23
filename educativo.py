"""Explicações em português para os resultados do núcleo matemático."""

from dataclasses import dataclass

import numpy as np

import operacoes as op


@dataclass(frozen=True)
class Explicacao:
    operacao: str
    formula: str
    substituicao: str
    desenvolvimento: str
    resultado: str
    significado: str

    def texto(self):
        return (f"{self.operacao}\nFórmula: {self.formula}\n"
                f"Substituição: {self.substituicao}\n"
                f"Desenvolvimento: {self.desenvolvimento}\n"
                f"Resultado: {self.resultado}\n"
                f"Geometria: {self.significado}")


def _n(numero):
    """Arredondamento exclusivo da apresentação (seis algarismos significativos)."""
    valor = float(numero)
    if abs(valor) < 1e-12:
        return "0"
    return f"{valor:.6g}"


def _v(vetor):
    return "(" + ", ".join(_n(x) for x in vetor) + ")"


def explicar(operacao, a, b=None, escalar=None):
    """Produz fórmula, substituição, desenvolvimento e interpretação.

    Nomes aceitos: soma, subtracao, multiplicacao_escalar, modulo,
    normalizacao, produto_escalar, produto_vetorial, angulo e projecao.
    Erros de domínio são os mesmos de operacoes.py.
    """
    nomes = {
        "soma": "Soma", "subtracao": "Subtração",
        "multiplicacao_escalar": "Multiplicação por escalar",
        "modulo": "Módulo", "normalizacao": "Normalização",
        "produto_escalar": "Produto escalar",
        "produto_vetorial": "Produto vetorial",
        "angulo": "Ângulo", "projecao": "Projeção de A sobre B",
    }
    if operacao not in nomes:
        raise ValueError(f"Operação desconhecida: {operacao}.")

    # Calcula primeiro: valida os dados com a mesma regra do núcleo matemático.
    if operacao == "multiplicacao_escalar":
        valor = op.multiplicacao_escalar(a, escalar)
    elif operacao in ("modulo", "normalizacao"):
        valor = getattr(op, operacao)(a)
    else:
        if b is None:
            raise ValueError("Esta operação exige o vetor B.")
        valor = getattr(op, operacao)(a, b)
    a = np.asarray(a, dtype=float)
    if b is not None:
        b = np.asarray(b, dtype=float)

    if operacao in ("soma", "subtracao"):
        sinal = "+" if operacao == "soma" else "−"
        passos = [f"{_n(x)} {sinal} {_n(y)} = {_n(z)}"
                  for x, y, z in zip(a, b, valor)]
        return Explicacao(nomes[operacao], f"A {sinal} B = (aᵢ {sinal} bᵢ)",
                          f"{_v(a)} {sinal} {_v(b)}",
                          "; ".join(passos), _v(valor),
                          "Soma: regra do paralelogramo, com B na ponta de A."
                          if operacao == "soma" else
                          "A − B aponta da ponta de B até a ponta de A.")

    if operacao == "multiplicacao_escalar":
        k = float(escalar)
        return Explicacao(nomes[operacao], "kA = (ka₁, ka₂[, ka₃])",
                          f"{_n(k)} × {_v(a)}",
                          "; ".join(f"{_n(k)} × {_n(x)} = {_n(y)}"
                                    for x, y in zip(a, valor)), _v(valor),
                          "O escalar altera o comprimento; se negativo, inverte o sentido.")

    if operacao == "modulo":
        soma_quadrados = float(np.dot(a, a))
        return Explicacao(nomes[operacao], "|A| = √(Σaᵢ²)",
                          f"|{_v(a)}| = √(" + " + ".join(f"{_n(x)}²" for x in a) + ")",
                          f"Σaᵢ² = {_n(soma_quadrados)}; √{_n(soma_quadrados)} = {_n(valor)}",
                          _n(valor), "É o comprimento de A desde a origem.")

    if operacao == "normalizacao":
        norma = op.modulo(a)
        return Explicacao(nomes[operacao], "Â = A / |A|",
                          f"Â = {_v(a)} / {_n(norma)}",
                          "; ".join(f"{_n(x)} / {_n(norma)} = {_n(y)}"
                                    for x, y in zip(a, valor)), _v(valor),
                          "Mantém a direção e o sentido de A, com comprimento 1.")

    if operacao == "produto_escalar":
        termos = [x * y for x, y in zip(a, b)]
        return Explicacao(nomes[operacao], "A · B = Σ(aᵢbᵢ)",
                          " + ".join(f"({_n(x)} × {_n(y)})" for x, y in zip(a, b)),
                          " + ".join(_n(x) for x in termos) + f" = {_n(valor)}",
                          _n(valor),
                          "Mede o alinhamento: positivo no mesmo sentido geral, negativo em sentidos opostos, zero se perpendiculares.")

    if operacao == "produto_vetorial":
        x, y, z = a
        u, v, w = b
        parcelas = ((y, w, z, v), (z, u, x, w), (x, v, y, u))
        return Explicacao(nomes[operacao],
                          "A × B = (a₂b₃ − a₃b₂, a₃b₁ − a₁b₃, a₁b₂ − a₂b₁)",
                          "(" + ", ".join(f"{_n(p)}×{_n(q)} − {_n(r)}×{_n(s)}"
                                          for p, q, r, s in parcelas) + ")",
                          "; ".join(f"{_n(p*q)} − {_n(r*s)} = {_n(t)}"
                                    for (p, q, r, s), t in zip(parcelas, valor)),
                          _v(valor),
                          "É perpendicular a A e B; o módulo é a área do paralelogramo formado por eles.")

    produto = op.produto_escalar(a, b)
    if operacao == "angulo":
        na, nb = op.modulo(a), op.modulo(b)
        cos = np.clip(produto / (na * nb), -1, 1)
        return Explicacao(nomes[operacao], "θ = arccos[(A · B) / (|A||B|)]",
                          f"θ = arccos[{_n(produto)} / ({_n(na)} × {_n(nb)})]",
                          f"cos θ = {_n(cos)}; θ = {_n(valor)}°",
                          f"{_n(valor)}°", "É a menor abertura entre os dois vetores.")

    denominador = op.produto_escalar(b, b)
    fator = produto / denominador
    return Explicacao(nomes[operacao], "proj_B(A) = [(A · B) / (B · B)]B",
                      f"proj_B(A) = [{_n(produto)} / {_n(denominador)}] × {_v(b)}",
                      f"Fator = {_n(fator)}; {_n(fator)} × {_v(b)} = {_v(valor)}",
                      _v(valor),
                      "É a componente de A na direção de B, podendo ter sentido contrário.")
