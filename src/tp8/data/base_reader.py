"""Abstraccion base del lector de JSON (Branching by Abstraction)."""
#############################################################
# copyright UADERFCyT-IS2(c)2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP8 - Re-ingenieria del proceso de pagos
#############################################################


class BaseJasonReader:  # pylint: disable=too-few-public-methods
    """Contrato base que deben cumplir las implementaciones de lector de JSON."""

    def getJason(self):  # noqa: N802  # pylint: disable=invalid-name
        """Retorna el valor leido del JSON. Debe implementarlo cada subclase."""
        raise NotImplementedError
