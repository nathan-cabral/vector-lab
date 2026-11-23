import unittest

import numpy as np

from operacoes import (
    angulo,
    modulo,
    multiplicacao_escalar,
    normalizacao,
    produto_escalar,
    produto_vetorial,
    projecao,
    soma,
    subtracao,
)


class OperacoesTest(unittest.TestCase):
    def test_operacoes_basicas_2d(self):
        np.testing.assert_array_equal(soma([3, 2], [2, 4]), [5, 6])
        np.testing.assert_array_equal(subtracao([3, 2], [2, 4]), [1, -2])
        np.testing.assert_array_equal(multiplicacao_escalar([3, 2], -2), [-6, -4])
        self.assertEqual(modulo([3, 4]), 5)
        np.testing.assert_allclose(normalizacao([3, 4]), [0.6, 0.8])
        self.assertEqual(produto_escalar([3, 2], [2, 4]), 14)
        self.assertAlmostEqual(angulo([1, 0], [0, 1]), 90)
        np.testing.assert_allclose(projecao([3, 4], [1, 0]), [3, 0])

    def test_operacoes_3d(self):
        np.testing.assert_array_equal(produto_vetorial([1, 0, 0], [0, 1, 0]), [0, 0, 1])
        np.testing.assert_array_equal(projecao([2, 3, 4], [0, 0, 2]), [0, 0, 4])

    def test_angulos_opostos_e_iguais(self):
        self.assertAlmostEqual(angulo([1, 0], [-1, 0]), 180)
        self.assertAlmostEqual(angulo([1, 2, 3], [1, 2, 3]), 0)

    def test_vetores_nulos(self):
        for operacao, args in (
            (normalizacao, ([0, 0],)),
            (angulo, ([0, 0], [1, 0])),
            (projecao, ([1, 0], [0, 0])),
        ):
            with self.subTest(operacao=operacao.__name__), self.assertRaises(ValueError):
                operacao(*args)

    def test_dimensoes_invalidas(self):
        for operacao, args in (
            (soma, ([1, 2], [1, 2, 3])),
            (produto_vetorial, ([1, 2], [3, 4])),
            (modulo, ([1],)),
            (modulo, ([[1, 2], [3, 4]],)),
        ):
            with self.subTest(operacao=operacao.__name__), self.assertRaises(ValueError):
                operacao(*args)

    def test_valores_invalidos(self):
        with self.assertRaises(ValueError):
            soma([1, np.nan], [2, 3])
        with self.assertRaises(ValueError):
            multiplicacao_escalar([1, 2], np.inf)


if __name__ == "__main__":
    unittest.main()
