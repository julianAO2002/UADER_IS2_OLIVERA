import unittest
from rpn import eval_rpn, RPNError

class TestRPN(unittest.TestCase):

    def test_suma(self):
        self.assertEqual(eval_rpn("3 4 +".split()), 7)

    def test_expresion_compleja(self):
        self.assertEqual(eval_rpn("5 1 2 + 4 * + 3 -".split()), 14)

    def test_multiplicacion(self):
        self.assertEqual(eval_rpn("2 3 4 * +".split()), 14)

    def test_division_por_cero(self):
        try:
            eval_rpn("3 0 /".split())
            self.fail("Se esperaba RPNError por división por cero")
        except RPNError:
            pass

    def test_token_invalido(self):
        try:
            eval_rpn("3 4 &".split())
            self.fail("Se esperaba RPNError por token inválido")
        except RPNError:
            pass

    def test_pila_insuficiente(self):
        try:
            eval_rpn("+".split())
            self.fail("Se esperaba RPNError por pila insuficiente")
        except RPNError:
            pass

    def test_pila_final_invalida(self):
        try:
            eval_rpn("3 4".split())
            self.fail("Se esperaba RPNError por pila final inválida")
        except RPNError:
            pass

    def test_dup(self):
        self.assertEqual(eval_rpn("5 dup +".split()), 10)

    def test_swap(self):
        self.assertEqual(eval_rpn("3 4 swap -".split()), 1)

    def test_constantes(self):
        self.assertAlmostEqual(eval_rpn("p".split()), 3.14159, places=4)

    def test_trig(self):
        self.assertAlmostEqual(eval_rpn("90 sin".split()), 1, places=4)
    
    def test_drop(self):
        self.assertEqual(eval_rpn("5 6 drop".split()), 5)

    def test_clear(self):
        try:
            eval_rpn("3 4 clear".split())
            self.fail("Se esperaba RPNError por pila vacía tras clear")
        except RPNError:
            pass

    def test_exp(self):
        self.assertAlmostEqual(eval_rpn("1 exp".split()), 2.71828, places=4)

    def test_10x(self):
        self.assertEqual(eval_rpn("2 10x".split()), 100)

    def test_yx(self):
        self.assertEqual(eval_rpn("2 3 yx".split()), 8)

    def test_inverse(self):
        self.assertEqual(eval_rpn("4 1/x".split()), 0.25)

    def test_chs(self):
        self.assertEqual(eval_rpn("5 chs".split()), -5)

    def test_memoria(self):
        self.assertEqual(eval_rpn("7 sto0 rcl0".split()), 7)

    def test_memoria_invalida(self):
        try:
            eval_rpn("5 sto10".split())
            self.fail("Se esperaba RPNError por memoria inválida")
        except RPNError:
            pass

    def test_asin(self):
        self.assertAlmostEqual(eval_rpn("1 asin".split()), 90, places=4)

    def test_acos(self):
        self.assertAlmostEqual(eval_rpn("1 acos".split()), 0, places=4)

    def test_atg(self):
        self.assertAlmostEqual(eval_rpn("1 atg".split()), 45, places=4)

    def test_dup_error(self):
        try:
            eval_rpn("dup".split())
            self.fail("Se esperaba RPNError por dup con pila vacía")
        except RPNError:
            pass

    def test_1_over_zero(self):
        try:
            eval_rpn("0 1/x".split())
            self.fail("Se esperaba RPNError por 1/0")
        except RPNError:
            pass

    def test_constante_e(self):
        self.assertAlmostEqual(eval_rpn("e".split()), 2.71828, places=4)

    def test_constante_j(self):
        self.assertAlmostEqual(eval_rpn("j".split()), 1.61803, places=4)

    def test_resta(self):
        self.assertEqual(eval_rpn("10 3 -".split()), 7)

    def test_sqrt(self):
        self.assertAlmostEqual(eval_rpn("9 sqrt".split()), 3.0, places=4)

    def test_log(self):
        self.assertAlmostEqual(eval_rpn("100 log".split()), 2.0, places=4)

    def test_ln(self):
        self.assertAlmostEqual(eval_rpn("1 ln".split()), 0.0, places=4)

    def test_cos(self):
        self.assertAlmostEqual(eval_rpn("0 cos".split()), 1.0, places=4)

    def test_tg(self):
        self.assertAlmostEqual(eval_rpn("45 tg".split()), 1.0, places=4)

    def test_rcl_invalido(self):
        try:
            eval_rpn("rcl10".split())
            self.fail("Se esperaba RPNError por rcl inválido")
        except RPNError:
            pass

    def test_swap_pila_insuficiente(self):
        try:
            eval_rpn("3 swap".split())
            self.fail("Se esperaba RPNError por swap con pila insuficiente")
        except RPNError:
            pass

    def test_main_con_args(self):
        import sys
        from unittest.mock import patch
        from io import StringIO
        with patch("sys.argv", ["rpn.py", "3", "4", "+"]):
            from rpn import main
            with patch("sys.stdout", new_callable=StringIO) as mock_out:
                main()
                self.assertIn("7", mock_out.getvalue())

    def test_main_sin_args(self):
        import sys
        from unittest.mock import patch
        from io import StringIO
        with patch("sys.argv", ["rpn.py"]):
            from rpn import main
            with patch("builtins.input", return_value="5 3 +"), \
                 patch("sys.stdout", new_callable=StringIO) as mock_out:
                main()
                self.assertIn("8", mock_out.getvalue())

if __name__ == "__main__":
    unittest.main()