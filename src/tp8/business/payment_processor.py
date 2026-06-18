"""Componente de re-ingenieria que automatiza la seleccion de cuenta."""
#############################################################
# copyright UADERFCyT-IS2(c)2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP8 - Re-ingenieria del proceso de pagos
#############################################################

from data.getJason import GetJason
from business.account_handler import AccountHandler
from domain.payment_log import PaymentLog
from config.version import SALDOS_INICIALES


class PaymentProcessor:
    """Componente de re-ingenieria que automatiza la seleccion de cuenta.

    Construye la cadena de cuentas (Chain of Command) y rutea las solicitudes
    de pago alternando entre las cuentas para balancear la carga. Registra
    cada pago realizado en un PaymentLog iterable.
    """

    def __init__(self, jsonfile):
        self._reader = GetJason(jsonfile)
        self._log = PaymentLog()
        self._tokens = list(SALDOS_INICIALES.keys())
        self._next_index = 0
        # Cada cuenta se modela como un AccountHandler independiente.
        self._accounts = {
            token: AccountHandler(token, balance, self._reader)
            for token, balance in SALDOS_INICIALES.items()
        }

    def _build_chain(self, start_token):
        """Arma la cadena empezando por start_token (ruteo balanceado/alternado)."""
        ordered = [start_token] + [t for t in self._tokens if t != start_token]
        head = None
        for token in reversed(ordered):
            account = self._accounts[token]
            account.set_next(head)
            head = account
        return head

    def request_payment(self, request_id, amount):
        """Solicita un pago; selecciona la cuenta automaticamente.

        Alterna la cuenta de inicio en cada solicitud para balancear los
        pagos. Si la cuenta inicial no tiene saldo, la cadena delega en la
        siguiente. Retorna el Payment realizado o None si no hay fondos.
        """
        start_token = self._tokens[self._next_index % len(self._tokens)]
        self._next_index += 1
        chain = self._build_chain(start_token)
        payment = chain.handle(request_id, amount)
        if payment is not None:
            self._log.add(payment)
        return payment

    def list_payments(self):
        """Lista todos los pagos realizados en orden cronologico (Iterator)."""
        print("Pagos realizados (orden cronologico):")
        for payment in self._log:
            print(f"  {payment}")

    def balances(self):
        """Retorna un dict con el saldo actual de cada cuenta."""
        return {token: acc.balance for token, acc in self._accounts.items()}
