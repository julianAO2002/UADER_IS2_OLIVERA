"""Conversión de documentos JSON a texto CSV.

Reglas de conversión:

* Un arreglo de objetos produce una fila por objeto. El encabezado es la
  unión de las claves en orden de primera aparición; las claves ausentes en
  un objeto quedan como celdas vacías.
* Un objeto único se trata como un arreglo de un elemento.
* Los objetos anidados se aplanan con notación de punto (`a.b.c`).
* Las listas anidadas se serializan como texto JSON dentro de la celda.
* Un arreglo de valores escalares produce una única columna `value`.
* `null` se convierte en una celda vacía y los booleanos en `true`/`false`.
* Un arreglo vacío produce una salida vacía.
"""

from __future__ import annotations

import csv
import io
import json
from typing import Any, TypeGuard, cast

COLUMNA_ESCALAR = "value"
DELIMITADORES_PROHIBIDOS = frozenset({'"', "\r", "\n"})


class ConversionError(Exception):
    """Error de datos o de parámetros durante la conversión."""


def validar_delimitador(delimitador: str) -> str:
    r"""Devuelve el delimitador si es válido.

    Acepta la secuencia de escape ``\t`` (barra invertida y t) como tabulador.

    Raises:
        ConversionError: si no es un único carácter o es un carácter reservado.
    """
    if delimitador == "\\t":
        delimitador = "\t"
    if len(delimitador) != 1:
        raise ConversionError(f"el delimitador debe ser un único carácter: {delimitador!r}")
    if delimitador in DELIMITADORES_PROHIBIDOS:
        raise ConversionError(f"delimitador no permitido: {delimitador!r}")
    return delimitador


def _celda(valor: Any) -> str:
    """Convierte un valor JSON escalar o lista en el texto de una celda."""
    if valor is None:
        return ""
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, list):
        return json.dumps(valor, ensure_ascii=False)
    return str(valor)


def _aplanar(objeto: dict[str, Any], prefijo: str = "") -> dict[str, str]:
    """Aplana un objeto JSON anidado usando claves con notación de punto."""
    plano: dict[str, str] = {}
    for clave, valor in objeto.items():
        nombre = f"{prefijo}.{clave}" if prefijo else str(clave)
        if isinstance(valor, dict):
            plano.update(_aplanar(cast(dict[str, Any], valor), nombre))
        else:
            plano[nombre] = _celda(valor)
    return plano


def _es_lista(valor: object) -> TypeGuard[list[Any]]:
    """Indica si un valor JSON decodificado es un arreglo."""
    return isinstance(valor, list)


def _como_lista(datos: object) -> list[Any]:
    """Normaliza la raíz del JSON a una lista de elementos."""
    if isinstance(datos, dict):
        return [datos]
    if _es_lista(datos):
        return datos
    raise ConversionError("el JSON debe ser un objeto o un arreglo")


def registros_desde_json(texto: str) -> tuple[list[str], list[dict[str, str]]]:
    """Interpreta texto JSON y devuelve el encabezado y las filas a escribir.

    Raises:
        ConversionError: si el texto no es JSON válido o su estructura no
            puede representarse como tabla.
    """
    if not texto.strip():
        raise ConversionError("la entrada está vacía")
    try:
        datos: Any = json.loads(texto)
    except json.JSONDecodeError as error:
        raise ConversionError(f"JSON inválido (línea {error.lineno}, columna {error.colno}): {error.msg}") from error

    elementos = _como_lista(datos)
    if all(isinstance(elemento, dict) for elemento in elementos):
        filas = [_aplanar(cast(dict[str, Any], elemento)) for elemento in elementos]
    elif not any(isinstance(elemento, (dict, list)) for elemento in elementos):
        filas = [{COLUMNA_ESCALAR: _celda(elemento)} for elemento in elementos]
    else:
        raise ConversionError("el arreglo mezcla objetos con otros tipos de valores")

    encabezado: list[str] = []
    for fila in filas:
        encabezado.extend(clave for clave in fila if clave not in encabezado)
    return encabezado, filas


def convertir(texto: str, delimitador: str = ",") -> str:
    """Convierte texto JSON en texto CSV usando el delimitador indicado.

    Raises:
        ConversionError: si el JSON o el delimitador no son válidos.
    """
    delimitador = validar_delimitador(delimitador)
    encabezado, filas = registros_desde_json(texto)
    if not encabezado:
        return ""
    salida = io.StringIO()
    escritor = csv.DictWriter(salida, fieldnames=encabezado, delimiter=delimitador, lineterminator="\n")
    escritor.writeheader()
    escritor.writerows(filas)
    return salida.getvalue()
