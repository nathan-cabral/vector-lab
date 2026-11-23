"""Operações vetoriais numéricas para vetores cartesianos 2D e 3D.

As funções devolvem arrays NumPy sem arredondamento. A interface será responsável
por formatar os valores para exibição.
"""

import numpy as np


def _vetor(valor, nome="vetor"):
    try:
        vetor = np.asarray(valor, dtype=float)
    except (TypeError, ValueError) as erro:
        raise ValueError(f"{nome} deve conter apenas números reais.") from erro
    if vetor.ndim != 1 or vetor.size not in (2, 3):
        raise ValueError(f"{nome} deve ter exatamente 2 ou 3 componentes.")
    if not np.all(np.isfinite(vetor)):
        raise ValueError(f"{nome} deve conter apenas valores finitos.")
    return vetor


def _par(a, b):
    a, b = _vetor(a, "A"), _vetor(b, "B")
    if a.size != b.size:
        raise ValueError("A e B devem ter a mesma dimensão.")
    return a, b


def soma(a, b):
    a, b = _par(a, b)
    return a + b


def subtracao(a, b):
    a, b = _par(a, b)
    return a - b


def multiplicacao_escalar(a, escalar):
    a = _vetor(a, "A")
    try:
        valor = float(escalar)
    except (TypeError, ValueError) as erro:
        raise ValueError("O escalar deve ser um número real.") from erro
    if not np.isfinite(valor):
        raise ValueError("O escalar deve ser finito.")
    return a * valor


def modulo(a):
    return float(np.linalg.norm(_vetor(a, "A")))


def normalizacao(a):
    a = _vetor(a, "A")
    norma = np.linalg.norm(a)
    if norma == 0:
        raise ValueError("Não é possível normalizar o vetor nulo.")
    return a / norma


def produto_escalar(a, b):
    a, b = _par(a, b)
    return float(np.dot(a, b))


def produto_vetorial(a, b):
    a, b = _par(a, b)
    if a.size != 3:
        raise ValueError("O produto vetorial exige vetores 3D.")
    return np.cross(a, b)


def angulo(a, b):
    """Retorna o menor ângulo entre A e B em graus."""
    a, b = _par(a, b)
    norma_a, norma_b = np.linalg.norm(a), np.linalg.norm(b)
    if norma_a == 0 or norma_b == 0:
        raise ValueError("O ângulo não é definido para vetor nulo.")
    cosseno = np.dot(a, b) / (norma_a * norma_b)
    return float(np.degrees(np.arccos(np.clip(cosseno, -1.0, 1.0))))


def projecao(a, b):
    """Retorna a projeção vetorial de A sobre B."""
    a, b = _par(a, b)
    denominador = np.dot(b, b)
    if denominador == 0:
        raise ValueError("Não é possível projetar sobre o vetor nulo.")
    return (np.dot(a, b) / denominador) * b
