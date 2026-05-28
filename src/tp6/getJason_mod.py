"""
getJason_mod.py
Recupera el valor de una clave de un archivo JSON.

Uso: python getJason_mod.py <archivo.json> [clave]
  archivo.json  : path al archivo JSON de entrada
  clave         : clave a recuperar (default: "token1")
"""

import json
import sys


def get_value(jsonfile, jsonkey='token1'):
    with open(jsonfile, 'r') as myfile:
        obj = json.loads(myfile.read())
    if jsonkey not in obj:
        raise KeyError(f'Clave "{jsonkey}" no encontrada en {jsonfile}')
    return str(obj[jsonkey])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python getJason_mod.py <archivo.json> [clave]')
        sys.exit(1)
    jsonfile = sys.argv[1]
    jsonkey  = sys.argv[2] if len(sys.argv) > 2 else 'token1'
    try:
        print(get_value(jsonfile, jsonkey))
    except FileNotFoundError:
        print(f'Error: archivo "{jsonfile}" no encontrado')
        sys.exit(1)
    except KeyError as e:
        print(f'Error: {e}')
        sys.exit(1)
