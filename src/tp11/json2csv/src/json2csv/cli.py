"""Interfaz de línea de comandos de json2csv con estrategia de filtro.

Uso::

    python json2csv.py [-i input.txt] [-o output.txt] [-d delimitador]

Sin ``-i`` lee la entrada estándar; sin ``-o`` escribe en la salida
estándar; sin ``-d`` usa la coma como delimitador.

Códigos de salida: 0 éxito, 1 error de datos o de E/S, 2 error de uso,
130 interrupción del usuario.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from typing import TextIO

from . import __build__, __version__
from .core import ConversionError, convertir

EXITO = 0
ERROR_DATOS = 1
ERROR_USO = 2
INTERRUMPIDO = 130


def crear_parser() -> argparse.ArgumentParser:
    """Construye el analizador de argumentos de la herramienta."""
    parser = argparse.ArgumentParser(
        prog="json2csv",
        description="Convierte JSON a CSV. Funciona como filtro: stdin -> stdout.",
    )
    parser.add_argument("-i", dest="entrada", metavar="input", help="archivo JSON de entrada (por defecto stdin)")
    parser.add_argument("-o", dest="salida", metavar="output", help="archivo CSV de salida (por defecto stdout)")
    parser.add_argument(
        "-d",
        dest="delimitador",
        metavar="delimitador",
        default=",",
        help="delimitador de campos, un carácter; admite \\t (por defecto ',')",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__} (build {__build__})")
    return parser


def _leer(ruta: str | None, stdin: TextIO) -> str:
    """Lee el texto de entrada desde un archivo o desde stdin."""
    if ruta is None:
        return stdin.read()
    with open(ruta, encoding="utf-8-sig") as archivo:
        return archivo.read()


def _escribir(ruta: str | None, texto: str, stdout: TextIO) -> None:
    """Escribe el texto resultante en un archivo o en stdout."""
    if ruta is None:
        stdout.write(texto)
        stdout.flush()
        return
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        archivo.write(texto)


def main(
    argv: Sequence[str] | None = None,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Ejecuta la herramienta y devuelve el código de salida."""
    entrada_std = stdin if stdin is not None else sys.stdin
    salida_std = stdout if stdout is not None else sys.stdout
    errores = stderr if stderr is not None else sys.stderr

    try:
        argumentos = crear_parser().parse_args(argv)
    except SystemExit as salida:
        return int(salida.code) if isinstance(salida.code, int) else ERROR_USO

    try:
        texto = _leer(argumentos.entrada, entrada_std)
        if argumentos.salida is not None and argumentos.entrada == argumentos.salida:
            raise ConversionError("el archivo de salida no puede ser el mismo que el de entrada")
        csv_texto = convertir(texto, argumentos.delimitador)
        _escribir(argumentos.salida, csv_texto, salida_std)
    except ConversionError as error:
        errores.write(f"json2csv: error: {error}\n")
        return ERROR_DATOS
    except FileNotFoundError as error:
        errores.write(f"json2csv: error: no existe el archivo: {error.filename}\n")
        return ERROR_DATOS
    except IsADirectoryError as error:
        errores.write(f"json2csv: error: es un directorio: {error.filename}\n")
        return ERROR_DATOS
    except PermissionError as error:
        errores.write(f"json2csv: error: permiso denegado: {error.filename}\n")
        return ERROR_DATOS
    except UnicodeDecodeError:
        errores.write("json2csv: error: la entrada no está codificada en UTF-8\n")
        return ERROR_DATOS
    except BrokenPipeError:
        return ERROR_DATOS
    except OSError as error:
        errores.write(f"json2csv: error de E/S: {error}\n")
        return ERROR_DATOS
    except KeyboardInterrupt:
        errores.write("json2csv: interrumpido por el usuario\n")
        return INTERRUMPIDO
    return EXITO
