"""Pruebas unitarias de json2csv.core.

Cada prueba documenta en su docstring la hipótesis de test que verifica.
"""

import pytest

from json2csv.core import ConversionError, convertir, registros_desde_json, validar_delimitador


def test_arreglo_de_objetos():
    """H1: un arreglo de objetos produce encabezado más una fila por objeto."""
    texto = '[{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]'
    assert convertir(texto) == "a,b\n1,x\n2,y\n"


def test_objeto_unico():
    """H2: un objeto suelto se trata como una única fila."""
    assert convertir('{"nombre": "Ana", "edad": 30}') == "nombre,edad\nAna,30\n"


def test_claves_heterogeneas():
    """H3: el encabezado es la unión ordenada de claves; faltantes quedan vacías."""
    texto = '[{"a": 1}, {"b": 2}, {"a": 3, "c": 4}]'
    assert convertir(texto) == "a,b,c\n1,,\n,2,\n3,,4\n"


def test_objetos_anidados_se_aplanan():
    """H4: los objetos anidados se aplanan con notación de punto."""
    texto = '{"id": 1, "dir": {"calle": "Mitre", "geo": {"lat": -31.7}}}'
    assert convertir(texto) == "id,dir.calle,dir.geo.lat\n1,Mitre,-31.7\n"


def test_listas_anidadas_como_json():
    """H5: una lista dentro de un objeto se guarda como texto JSON en la celda."""
    assert convertir('{"tags": ["a", "b"]}') == 'tags\n"[""a"", ""b""]"\n'


def test_nulos_y_booleanos():
    """H6: null es celda vacía y los booleanos se escriben en minúscula."""
    assert convertir('[{"x": null, "y": true, "z": false}]') == "x,y,z\n,true,false\n"


def test_arreglo_de_escalares():
    """H7: un arreglo de escalares produce la columna única 'value'.

    Una fila de una sola celda vacía se escribe como '""' para no
    confundirse con una línea en blanco.
    """
    assert convertir('[1, "dos", 3.5, null]') == 'value\n1\ndos\n3.5\n""\n'


def test_arreglo_vacio():
    """H8: un arreglo vacío produce una salida vacía."""
    assert convertir("[]") == ""


def test_objeto_vacio():
    """H9: un objeto vacío no tiene columnas y produce salida vacía."""
    assert convertir("{}") == ""


@pytest.mark.parametrize(
    ("delimitador", "esperado"),
    [(";", "a;b\n1;2\n"), ("|", "a|b\n1|2\n"), ("\\t", "a\tb\n1\t2\n")],
)
def test_delimitador_personalizado(delimitador, esperado):
    r"""H10: el delimitador indicado reemplaza a la coma (admite \t)."""
    assert convertir('{"a": 1, "b": 2}', delimitador) == esperado


def test_valores_con_delimitador_se_entrecomillan():
    """H11: un valor que contiene el delimitador se escribe entre comillas."""
    assert convertir('{"a": "x,y"}') == 'a\n"x,y"\n'


def test_unicode_se_preserva():
    """H12: los caracteres no ASCII se mantienen sin escapar."""
    assert convertir('{"ciudad": "Concepción del Uruguay"}') == "ciudad\nConcepción del Uruguay\n"


@pytest.mark.parametrize("delimitador", ["", ";;", '"', "\n", "\r"])
def test_delimitador_invalido(delimitador):
    """H13: delimitadores vacíos, múltiples o reservados se rechazan."""
    with pytest.raises(ConversionError):
        validar_delimitador(delimitador)


@pytest.mark.parametrize("texto", ["", "   \n", "{no es json}", "[1, 2"])
def test_json_vacio_o_invalido(texto):
    """H14: entrada vacía o JSON mal formado produce ConversionError."""
    with pytest.raises(ConversionError):
        convertir(texto)


def test_json_invalido_informa_posicion():
    """H15: el mensaje de JSON inválido indica línea y columna."""
    with pytest.raises(ConversionError, match="línea 1, columna"):
        convertir("{'a': 1}")


@pytest.mark.parametrize("texto", ["42", '"texto"', "true", "null"])
def test_raiz_escalar_rechazada(texto):
    """H16: un JSON cuya raíz es un escalar no puede tabularse."""
    with pytest.raises(ConversionError, match="objeto o un arreglo"):
        convertir(texto)


@pytest.mark.parametrize("texto", ['[{"a": 1}, 2]', "[[1, 2], [3]]"])
def test_arreglo_mixto_rechazado(texto):
    """H17: un arreglo que mezcla objetos o listas con otros valores se rechaza."""
    with pytest.raises(ConversionError, match="mezcla"):
        convertir(texto)


def test_registros_desde_json_devuelve_estructura():
    """H18: registros_desde_json expone encabezado y filas aplanadas."""
    encabezado, filas = registros_desde_json('[{"a": {"b": 1}}]')
    assert encabezado == ["a.b"]
    assert filas == [{"a.b": "1"}]
