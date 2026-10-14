"""json2csv: filtro que convierte documentos JSON a formato CSV.

El paquete expone la conversión pura (`json2csv.core`) separada de la
interfaz de línea de comandos (`json2csv.cli`), que actúa como un filtro
clásico: lee de un archivo o de la entrada estándar y escribe en un archivo
o en la salida estándar.
"""

from .core import ConversionError, convertir, registros_desde_json

__version__ = "1.0.0"
__build__ = 1

__all__ = [
    "ConversionError",
    "__build__",
    "__version__",
    "convertir",
    "registros_desde_json",
]
