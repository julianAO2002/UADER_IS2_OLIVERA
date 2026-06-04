#############################################################
# copyright UADERFCyT-IS2©2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP7 - Refactorizacion con patrones de diseño
#############################################################

import sys
import os

VERSION = "1.0.0"

# Validaciones de argumentos antes de instanciar cualquier clase
if len(sys.argv) < 2:
    print("Uso: python main.py <archivo.json>")
    sys.exit(1)

if sys.argv[1] == "-v":
    print(f"Version: {VERSION}")
    sys.exit(0)

if len(sys.argv) > 2:
    print("Error: demasiados argumentos. Uso: python main.py <archivo.json>")
    sys.exit(1)

if not sys.argv[1].endswith(".json"):
    print("Error: el archivo debe ser .json")
    sys.exit(1)

if not os.path.exists(sys.argv[1]):
    print(f"Error: no se encontró el archivo '{sys.argv[1]}'")
    sys.exit(1)

# Branching by Abstraction: flag para alternar entre la implementacion
# original y la refactorizada sin modificar el resto del codigo.
# Ambas cumplen el contrato de BaseJasonReader.
USE_REFACTORED = True

if USE_REFACTORED:
    # Version refactorizada: aplica Singleton y Chain of Responsibility
    from getJason import getJason
    reader = getJason()
else:
    # Version original: sin patrones de diseño (obtenida por ingenieria inversa)
    from getJasonOriginal import getJasonOriginal
    reader = getJasonOriginal()

print(reader.getJason())
