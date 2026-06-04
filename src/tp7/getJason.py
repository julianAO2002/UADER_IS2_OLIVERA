"""
Modulo getJason - Lector de archivos JSON con patrones de diseño.

Implementa Singleton para la instancia lectora y Chain of Responsibility
para la validacion de argumentos de linea de comandos.
"""
# pylint: disable=invalid-name
# El nombre del modulo es getJason por convencion del TP; no puede renombrarse.
#############################################################
# copyright UADERFCyT-IS2©2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP7 - Refactorizacion con patrones de diseño
#############################################################

import os
import json
import sys
from base_reader import BaseJasonReader

VERSION = "1.0.0"


class Validator:  # pylint: disable=too-few-public-methods
    """Nodo base de la cadena de responsabilidad para validacion de argumentos."""

    def __init__(self, next_validator=None):
        self._next = next_validator

    def validate(self, args):
        """Delega la validacion al siguiente eslabón de la cadena."""
        if self._next:
            self._next.validate(args)


class ArgCountValidator(Validator):  # pylint: disable=too-few-public-methods
    """Verifica que se haya pasado al menos un argumento."""

    def validate(self, args):
        """Falla con mensaje de uso si no hay argumentos suficientes."""
        if len(args) < 2:
            print("Uso: python getJason.py <archivo.json>")
            sys.exit(1)
        super().validate(args)


class VersionValidator(Validator):  # pylint: disable=too-few-public-methods
    """Muestra la version y termina si el argumento es -v."""

    def validate(self, args):
        """Imprime la version y sale si se solicito con -v."""
        if args[1] == "-v":
            print(f"Version: {VERSION}")
            sys.exit(0)
        super().validate(args)


class ExtraArgsValidator(Validator):  # pylint: disable=too-few-public-methods
    """Verifica que no se hayan pasado mas argumentos de los esperados."""

    def validate(self, args):
        """Falla si hay mas de un argumento posicional."""
        if len(args) > 2:
            print("Error: demasiados argumentos. Uso: python getJason.py <archivo.json>")
            sys.exit(1)
        super().validate(args)


class ExtensionValidator(Validator):  # pylint: disable=too-few-public-methods
    """Verifica que el archivo tenga extension .json."""

    def validate(self, args):
        """Falla si la extension del archivo no es .json."""
        if not args[1].endswith(".json"):
            print("Error: el archivo debe ser .json")
            sys.exit(1)
        super().validate(args)


class FileExistsValidator(Validator):  # pylint: disable=too-few-public-methods
    """Verifica que el archivo exista en el sistema de archivos."""

    def validate(self, args):
        """Falla si el archivo indicado no existe en disco."""
        if not os.path.exists(args[1]):
            print(f"Error: no se encontró el archivo '{args[1]}'")
            sys.exit(1)
        super().validate(args)


chain = ArgCountValidator(
    VersionValidator(
        ExtraArgsValidator(
            ExtensionValidator(
                FileExistsValidator()
            )
        )
    )
)
chain.validate(sys.argv)


class GetJason(BaseJasonReader):
    """Lector de JSON con patron Singleton: garantiza una unica instancia."""

    _instance = None
    _jsonfile = None
    _jsonkey = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._jsonfile = sys.argv[1]
            cls._instance._jsonkey = "token1"
        return cls._instance

    def get_jason(self):
        """Abre el archivo JSON y retorna el valor de la clave configurada."""
        with open(self._jsonfile, 'r', encoding='utf-8') as myfile:
            data = myfile.read()
        obj = json.loads(data)
        return str(obj[self._jsonkey])

    def getJason(self):  # noqa: N802
        """Alias de compatibilidad con la interfaz BaseJasonReader."""
        return self.get_jason()


if __name__ == "__main__":
    reader = GetJason()
    print(reader.getJason())
