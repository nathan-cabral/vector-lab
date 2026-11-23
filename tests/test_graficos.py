import unittest

import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_agg import FigureCanvasAgg

from graficos import COR_ANGULO, criar_figura


class GraficosTest(unittest.TestCase):
    def test_figuras_2d_e_3d_renderizam(self):
        casos = (
            ("soma", [3, 2], [2, 4], None, "rectilinear"),
            ("produto_vetorial", [1, 0, 0], [0, 1, 0], None, "3d"),
            ("angulo", [1, 0], [0, 1], None, "rectilinear"),
            ("normalizacao", [3, 4], None, None, "rectilinear"),
        )
        for nome, a, b, escalar, tipo in casos:
            with self.subTest(nome=nome):
                figura = criar_figura(nome, a, b, escalar)
                self.assertEqual(figura.axes[0].name, tipo)
                FigureCanvasAgg(figura).draw()

    def test_rejeita_operacao_invalida(self):
        with self.assertRaises(ValueError):
            criar_figura("produto_vetorial", [1, 2], [3, 4])

    def test_construcao_da_subtracao_liga_b_a_a(self):
        eixo = criar_figura("subtracao", [3, 2], [2, 4]).axes[0]
        auxiliar = next(linha for linha in eixo.lines
                        if linha.get_linestyle() == "--")
        self.assertEqual(list(auxiliar.get_xdata()), [2, 3])
        self.assertEqual(list(auxiliar.get_ydata()), [4, 2])

    def test_angulo_aparece_nos_dois_modos(self):
        for a, b in (([1, 0], [0, 1]), ([1, 0, 0], [0, 1, 0])):
            with self.subTest(a=a):
                eixo = criar_figura("angulo", a, b).axes[0]
                self.assertTrue(any("90" in texto.get_text() for texto in eixo.texts))
                self.assertTrue(any(linha.get_color() == COR_ANGULO for linha in eixo.lines))
                FigureCanvasAgg(eixo.figure).draw()


if __name__ == "__main__":
    unittest.main()
