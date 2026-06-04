#############################################################
# copyright UADERFCyT-IS2©2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP7 - Refactorizacion con patrones de diseño
#############################################################

import json
import sys
from base_reader import BaseJasonReader

# Implementacion original obtenida por ingenieria inversa (TP6).
# No aplica patrones de diseño. Se mantiene para comparacion
# mediante la estrategia Branching by Abstraction.
class getJasonOriginal(BaseJasonReader):
    def __init__(self):
        # Lee el nombre del archivo JSON desde el primer argumento
        self.jsonfile = sys.argv[1]
        self.jsonkey = "token1"

    def getJason(self):
        # Abre el archivo, parsea el JSON y retorna el valor de la clave
        with open(self.jsonfile, 'r') as myfile:
            data = myfile.read()
        obj = json.loads(data)
        return str(obj[self.jsonkey])
