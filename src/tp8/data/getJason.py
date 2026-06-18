"""
Modulo getJason - Singleton lector de claves por token (banco).

A partir de un nombre de token (banco) devuelve la clave asociada almacenada
en el archivo JSON (sitedata.json). Es el objeto singleton que se integra al
componente de pagos del TP8.
"""
# pylint: disable=invalid-name
# El nombre del modulo es getJason por convencion del TP; no puede renombrarse.
#############################################################
# copyright UADERFCyT-IS2(c)2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP8 - Re-ingenieria del proceso de pagos
#############################################################

import json

from data.base_reader import BaseJasonReader


class GetJason(BaseJasonReader):
    """Lector de JSON con patron Singleton: garantiza una unica instancia.

    A partir de un nombre de token (banco) devuelve la clave asociada
    almacenada en el archivo JSON (sitedata.json).
    """

    _instance = None
    _jsonfile = None

    def __new__(cls, jsonfile=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._jsonfile = jsonfile
        return cls._instance

    def _load(self):
        """Lee y parsea el archivo JSON configurado."""
        with open(self._jsonfile, 'r', encoding='utf-8') as myfile:
            data = myfile.read()
        return json.loads(data)

    def get_key(self, token):
        """Retorna la clave asociada a un token (banco)."""
        return str(self._load()[token])

    def get_jason(self, token="token1"):
        """Retorna el valor de la clave indicada (compatibilidad TP7)."""
        return self.get_key(token)

    def getJason(self, token="token1"):  # noqa: N802
        """Alias de compatibilidad con la interfaz BaseJasonReader."""
        return self.get_jason(token)
