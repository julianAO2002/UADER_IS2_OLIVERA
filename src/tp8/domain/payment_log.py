"""Registro iterable de pagos (patron Iterator)."""
#############################################################
# copyright UADERFCyT-IS2(c)2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP8 - Re-ingenieria del proceso de pagos
#############################################################


class PaymentIterator:
    """Patron Iterator: recorre los pagos en orden cronologico."""

    def __init__(self, payments):
        self._payments = payments
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._payments):
            raise StopIteration
        payment = self._payments[self._index]
        self._index += 1
        return payment


class PaymentLog:
    """Coleccion iterable de pagos (patron Iterator).

    Almacena los pagos en el orden en que fueron realizados y expone un
    iterador para recorrerlos cronologicamente.
    """

    def __init__(self):
        self._payments = []

    def add(self, payment):
        """Agrega un pago al registro."""
        self._payments.append(payment)

    def __iter__(self):
        return PaymentIterator(self._payments)
