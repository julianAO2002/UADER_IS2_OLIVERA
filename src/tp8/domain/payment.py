"""Modelo de un pago realizado."""
#############################################################
# copyright UADERFCyT-IS2(c)2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP8 - Re-ingenieria del proceso de pagos
#############################################################


class Payment:  # pylint: disable=too-few-public-methods
    """Representa un pago realizado: numero de pedido, token, monto y clave."""

    def __init__(self, request_id, token, amount, key):
        self.request_id = request_id
        self.token = token
        self.amount = amount
        self.key = key

    def __str__(self):
        return (f"Pedido #{self.request_id} | token={self.token} | "
                f"monto=${self.amount} | clave={self.key}")
