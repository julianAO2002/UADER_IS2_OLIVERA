"""Cadena de responsabilidad para la validacion de argumentos de linea de comandos.

Patron Chain of Responsibility: cada validador atiende un aspecto y delega
en el siguiente eslabon de la cadena.
"""
#############################################################
# copyright UADERFCyT-IS2(c)2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP8 - Re-ingenieria del proceso de pagos
#############################################################

import os
import sys

from config.version import VERSION


class Validator:  # pylint: disable=too-few-public-methods
    """Nodo base de la cadena de responsabilidad para validacion de argumentos."""

    def __init__(self, next_validator=None):
        self._next = next_validator

    def validate(self, args):
        """Delega la validacion al siguiente eslabon de la cadena."""
        if self._next:
            self._next.validate(args)


class ArgCountValidator(Validator):  # pylint: disable=too-few-public-methods
    """Verifica que se haya pasado al menos un argumento."""

    def validate(self, args):
        """Falla con mensaje de uso si no hay argumentos suficientes."""
        if len(args) < 2:
            print("Uso: python main.py <archivo.json>")
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
            print("Error: demasiados argumentos. Uso: python main.py <archivo.json>")
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
            print(f"Error: no se encontro el archivo '{args[1]}'")
            sys.exit(1)
        super().validate(args)


def build_validation_chain():
    """Construye y retorna la cadena de validacion de argumentos completa."""
    return ArgCountValidator(
        VersionValidator(
            ExtraArgsValidator(
                ExtensionValidator(
                    FileExistsValidator()
                )
            )
        )
    )
