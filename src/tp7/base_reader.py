#############################################################
# copyright UADERFCyT-IS2©2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP7 - Refactorizacion con patrones de diseño
#############################################################

# Abstraccion base para Branching by Abstraction.
# Define el contrato que deben cumplir todas las implementaciones
# de lector de JSON, tanto la original como la refactorizada.
class BaseJasonReader:
    def getJason(self):
        raise NotImplementedError
