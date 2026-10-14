"""Pruebas de la interfaz de línea de comandos (estrategia de filtro)."""

import io
import os
import pathlib
import subprocess
import sys

import pytest

import json2csv
from json2csv import cli

RAIZ = pathlib.Path(__file__).resolve().parents[1]
JSON = '[{"a": 1, "b": 2}]'


def ejecutar(argv, entrada=""):
    """Ejecuta cli.main con flujos en memoria y devuelve (código, stdout, stderr)."""
    salida, errores = io.StringIO(), io.StringIO()
    codigo = cli.main(argv, stdin=io.StringIO(entrada), stdout=salida, stderr=errores)
    return codigo, salida.getvalue(), errores.getvalue()


def test_stdin_a_stdout():
    """H19: sin -i ni -o funciona como filtro stdin -> stdout."""
    assert ejecutar([], JSON) == (0, "a,b\n1,2\n", "")


def test_archivo_a_archivo(tmp_path):
    """H20: -i y -o leen y escriben archivos."""
    entrada, salida = tmp_path / "in.txt", tmp_path / "out.txt"
    entrada.write_text(JSON, encoding="utf-8")
    assert ejecutar(["-i", str(entrada), "-o", str(salida)]) == (0, "", "")
    assert salida.read_text(encoding="utf-8") == "a,b\n1,2\n"


def test_archivo_con_bom(tmp_path):
    """H21: un archivo UTF-8 con BOM se lee correctamente."""
    entrada = tmp_path / "bom.json"
    entrada.write_bytes(b"\xef\xbb\xbf" + JSON.encode())
    assert ejecutar(["-i", str(entrada)])[1] == "a,b\n1,2\n"


def test_delimitador_por_argumento():
    """H22: -d cambia el delimitador."""
    assert ejecutar(["-d", ";"], JSON)[1] == "a;b\n1;2\n"


def test_archivo_inexistente(tmp_path):
    """H23: un archivo de entrada inexistente devuelve 1 con mensaje claro."""
    codigo, _, errores = ejecutar(["-i", str(tmp_path / "no.json")])
    assert codigo == 1
    assert "no existe el archivo" in errores


def test_entrada_es_directorio(tmp_path):
    """H24: pasar un directorio como entrada se informa como error."""
    codigo, _, errores = ejecutar(["-i", str(tmp_path)])
    assert codigo == 1
    assert "json2csv: error" in errores


def test_json_invalido_por_stdin():
    """H25: JSON inválido devuelve 1 sin traceback."""
    codigo, salida, errores = ejecutar([], "{malo")
    assert (codigo, salida) == (1, "")
    assert errores.startswith("json2csv: error: JSON inválido")


def test_delimitador_invalido_por_argumento():
    """H26: un delimitador inválido devuelve 1."""
    assert ejecutar(["-d", "::"], JSON)[0] == 1


def test_entrada_no_utf8(tmp_path):
    """H27: un archivo que no es UTF-8 se informa como error de codificación."""
    entrada = tmp_path / "latin1.json"
    entrada.write_bytes('{"a": "ñ"}'.encode("latin-1"))
    codigo, _, errores = ejecutar(["-i", str(entrada)])
    assert codigo == 1
    assert "UTF-8" in errores


def test_salida_igual_a_entrada(tmp_path):
    """H28: no se permite sobrescribir el archivo de entrada."""
    entrada = tmp_path / "x.json"
    entrada.write_text(JSON, encoding="utf-8")
    assert ejecutar(["-i", str(entrada), "-o", str(entrada)])[0] == 1
    assert entrada.read_text(encoding="utf-8") == JSON


def test_salida_en_directorio_inexistente(tmp_path):
    """H29: no poder crear el archivo de salida devuelve 1."""
    destino = tmp_path / "no" / "existe" / "out.csv"
    assert ejecutar(["-o", str(destino)], JSON)[0] == 1


@pytest.mark.parametrize(
    ("excepcion", "codigo", "mensaje"),
    [
        (PermissionError(13, "denegado", "f.json"), 1, "permiso denegado"),
        (OSError(5, "falla de disco"), 1, "error de E/S"),
        (BrokenPipeError(), 1, ""),
        (KeyboardInterrupt(), 130, "interrumpido"),
    ],
)
def test_excepciones_de_entrada_salida(monkeypatch, excepcion, codigo, mensaje):
    """H30: las excepciones de E/S e interrupción se traducen a códigos de salida."""

    def fallar(*_args):
        raise excepcion

    monkeypatch.setattr(cli, "_leer", fallar)
    obtenido, _, errores = ejecutar([])
    assert obtenido == codigo
    assert mensaje in errores


def test_argumento_desconocido(capsys):
    """H31: un argumento desconocido es un error de uso (código 2)."""
    assert cli.main(["--xyz"]) == 2
    assert "usage" in capsys.readouterr().err


def test_version(capsys):
    """H32: --version informa VERSION y BUILD y termina con 0."""
    assert cli.main(["--version"]) == 0
    assert f"{json2csv.__version__} (build {json2csv.__build__})" in capsys.readouterr().out


def test_version_coincide_con_archivos():
    """H33: los archivos VERSION y BUILD coinciden con el paquete."""
    assert (RAIZ / "VERSION").read_text(encoding="utf-8").strip() == json2csv.__version__
    assert int((RAIZ / "BUILD").read_text(encoding="utf-8").strip()) == json2csv.__build__


def test_main_usa_flujos_del_sistema(monkeypatch):
    """H34: sin flujos explícitos main usa sys.stdin y sys.stdout."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(JSON))
    salida = io.StringIO()
    monkeypatch.setattr(sys, "stdout", salida)
    assert cli.main([]) == 0
    assert salida.getvalue() == "a,b\n1,2\n"


def test_script_de_entrada_extremo_a_extremo():
    """H35: 'python json2csv.py -d ;' funciona como filtro de punta a punta."""
    entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
    resultado = subprocess.run(  # noqa: S603
        [sys.executable, str(RAIZ / "json2csv.py"), "-d", ";"],
        input=JSON,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=entorno,
        check=False,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert resultado.stdout.splitlines() == ["a;b", "1;2"]
