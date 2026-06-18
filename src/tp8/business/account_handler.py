"""Cadena de comando de cuentas (patron Chain of Command)."""
#############################################################
# copyright UADERFCyT-IS2(c)2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP8 - Re-ingenieria del proceso de pagos
#############################################################

from domain.payment import Payment


class AccountHandler:
    """Patron Chain of Command: eslabon que controla una cuenta.

    Si la cuenta tiene saldo suficiente atiende el pago; en caso contrario
    delega la solicitud al siguiente eslabon de la cadena.
    """

    def __init__(self, token, balance, reader, next_handler=None):
        self._token = token
        self._balance = balance
        self._reader = reader
        self._next = next_handler

    @property
    def token(self):
        """Token (banco) controlado por este eslabon."""
        return self._token

    @property
    def balance(self):
        """Saldo actual de la cuenta."""
        return self._balance

    def set_next(self, next_handler):
        """Define el siguiente eslabon de la cadena."""
        self._next = next_handler

    def handle(self, request_id, amount):
        """Procesa el pago si hay saldo, o lo delega al siguiente eslabon.

        Retorna el objeto Payment realizado, o None si ningun eslabon de la
        cadena pudo atender la solicitud.
        """
        if self._balance >= amount:
            self._balance -= amount
            key = self._reader.get_key(self._token)
            return Payment(request_id, self._token, amount, key)
        if self._next is not None:
            return self._next.handle(request_id, amount)
        return None
