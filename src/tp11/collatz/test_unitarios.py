"""Unit test cases (white box) for collatz.py - TP11 Gestion de Calidad.

Each test is named after its test case identifier (T01..T26) so the
traceability matrix RTMX in the README can reference it directly.
"""

import contextlib
import importlib
import io
import pathlib
import sys
import time

import pytest

RUTA = pathlib.Path(__file__).with_name("collatz.py")


@pytest.fixture(scope="module")
def mod():
    """Import collatz.py capturing anything it prints at import time."""
    sys.path.insert(0, str(RUTA.parent))
    sys.modules.pop("collatz", None)
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        modulo = importlib.import_module("collatz")
    modulo.SALIDA_IMPORT = salida.getvalue()
    return modulo


# --- R3: iteration count (branches of the while loop) ---------------------


def test_t01_uno_no_entra_al_ciclo(mod):
    assert mod.collatz(1) == 0


def test_t02_rama_par(mod):
    assert mod.collatz(2) == 1


def test_t03_rama_impar(mod):
    assert mod.collatz(3) == 7


def test_t04_ejemplo_del_enunciado(mod):
    assert mod.collatz(20) == 7


def test_t05_secuencia_larga(mod):
    assert mod.collatz(27) == 111


def test_t06_limite_superior(mod):
    assert mod.collatz(1999) == 50


# --- R2 / R5: input validation --------------------------------------------


def test_t07_rechaza_cero(mod):
    with pytest.raises(ValueError):
        mod.validar_entrada("0")


def test_t08_rechaza_negativo(mod):
    with pytest.raises(ValueError):
        mod.validar_entrada("-5")


def test_t09_rechaza_mayor_a_1999(mod):
    with pytest.raises(ValueError):
        mod.validar_entrada("2000")


def test_t10_rechaza_no_numerico(mod):
    with pytest.raises(ValueError):
        mod.validar_entrada("abc")


def test_t11_acepta_limites(mod):
    assert mod.validar_entrada("1") == 1
    assert mod.validar_entrada("1999") == 1999


# --- F2 / F4: non functional ----------------------------------------------


def test_t19_tasa_de_comentarios():
    """F2: at most 12 lines of code per comment line."""
    lineas = [l.strip() for l in RUTA.read_text(encoding="utf-8").splitlines()]
    codigo = [l for l in lineas if l]
    comentarios = [l for l in codigo if l.startswith("#") or '"""' in l]
    assert comentarios, "el programa no tiene comentarios"
    assert len(codigo) / len(comentarios) <= 12


def test_t20_rendimiento_rango_completo(mod):
    """F4: the whole valid range [1, 1999] is computed in under 1 second."""
    inicio = time.perf_counter()
    for numero in range(1, 2000):
        mod.collatz(numero)
    assert time.perf_counter() - inicio < 1


# --- Added during inspection session 2 ------------------------------------


def test_t21_rechaza_decimal(mod):
    with pytest.raises(ValueError):
        mod.validar_entrada("3.5")


def test_t22_rechaza_vacio(mod):
    with pytest.raises(ValueError):
        mod.validar_entrada("")


def test_t23_acepta_espacios(mod):
    assert mod.validar_entrada("  27  ") == 27


def test_t26_import_sin_efectos(mod):
    """F5: importing the module must not print or ask for input."""
    assert mod.SALIDA_IMPORT == ""
