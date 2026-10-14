"""Functional test cases (black box) for collatz.py - TP11 Gestion de Calidad.

The program is executed as a separate process, feeding the keyboard input
through stdin and checking only what the user sees.
"""

import os
import pathlib
import subprocess
import sys

RUTA = pathlib.Path(__file__).with_name("collatz.py")


def ejecutar(entrada):
    """Run collatz.py with the given stdin text and return the result."""
    entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, str(RUTA)],
        input=entrada,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        env=entorno,
        check=False,
    )


def assert_rechazo(entrada):
    """The input is rejected with a message and without a traceback."""
    resultado = ejecutar(entrada)
    assert "Error" in resultado.stdout
    assert "Traceback" not in resultado.stderr
    assert "El número de iteraciones" not in resultado.stdout


# --- R1 / R3 / R4: valid input ----------------------------------------------


def test_t12_caso_nominal():
    resultado = ejecutar("20\n")
    assert "El número de iteraciones para 20 es 7" in resultado.stdout
    assert resultado.returncode == 0


def test_t13_limite_inferior():
    resultado = ejecutar("1\n")
    assert "El número de iteraciones para 1 es 0" in resultado.stdout
    assert resultado.returncode == 0


def test_t14_limite_superior():
    resultado = ejecutar("1999\n")
    assert "El número de iteraciones para 1999 es 50" in resultado.stdout
    assert resultado.returncode == 0


# --- R2 / R5: invalid input -------------------------------------------------


def test_t15_rechaza_2000():
    assert_rechazo("2000\n")


def test_t16_rechaza_cero():
    assert_rechazo("0\n")


def test_t17_rechaza_negativo():
    assert_rechazo("-3\n")


def test_t18_rechaza_texto():
    assert_rechazo("abc\n")


# --- Added during inspection session 2 --------------------------------------


def test_t24_fin_de_entrada_sin_traceback():
    resultado = ejecutar("")
    assert "Traceback" not in resultado.stderr
    assert resultado.returncode == 1


def test_t25_reintenta_tras_entrada_invalida():
    resultado = ejecutar("abc\n20\n")
    assert "Error" in resultado.stdout
    assert "El número de iteraciones para 20 es 7" in resultado.stdout
    assert resultado.returncode == 0
