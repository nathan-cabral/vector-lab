import unittest

from educativo import explicar


class EducativoTest(unittest.TestCase):
    def test_todas_as_operacoes_tem_etapas(self):
        casos = (
            ("soma", [3, 2], [2, 4], None, "(5, 6)"),
            ("subtracao", [3, 2], [2, 4], None, "(1, -2)"),
            ("multiplicacao_escalar", [3, 2], None, -2, "(-6, -4)"),
            ("modulo", [3, 4], None, None, "5"),
            ("normalizacao", [3, 4], None, None, "(0.6, 0.8)"),
            ("produto_escalar", [3, 2], [2, 4], None, "14"),
            ("produto_vetorial", [1, 0, 0], [0, 1, 0], None, "(0, 0, 1)"),
            ("angulo", [1, 0], [0, 1], None, "90°"),
            ("projecao", [3, 4], [1, 0], None, "(3, 0)"),
        )
        for nome, a, b, escalar, resultado in casos:
            with self.subTest(nome=nome):
                e = explicar(nome, a, b, escalar)
                self.assertEqual(e.resultado, resultado)
                self.assertTrue(all((e.formula, e.substituicao,
                                     e.desenvolvimento, e.significado)))
                self.assertIn("Resultado:", e.texto())

    def test_rejeita_operacoes_invalidas(self):
        for nome, a, b in (("desconhecida", [1, 2], None),
                           ("angulo", [0, 0], [1, 0]),
                           ("produto_vetorial", [1, 2], [3, 4])):
            with self.subTest(nome=nome), self.assertRaises(ValueError):
                explicar(nome, a, b)


if __name__ == "__main__":
    unittest.main()
