"""
Punto de entrada del TP8 - Re-ingenieria del proceso de pagos.

Valida los argumentos de linea de comandos (Chain of Responsibility) y
ejecuta una demostracion del procesador de pagos automatico:
  * Singleton: GetJason da la clave a partir de un token (banco).
  * Chain of Command: AccountHandler controla cada cuenta y atiende el pago.
  * Iterator: PaymentLog recorre los pagos en orden cronologico.

Uso:
    python main.py sitedata.json
    python main.py -v
"""
#############################################################
# copyright UADERFCyT-IS2(c)2024 todos los derechos reservados
# Autor: Julian Olivera
# Materia: Ingenieria de Software 2
# TP8 - Re-ingenieria del proceso de pagos
#############################################################

import sys

from presentation.validators import build_validation_chain
from business.payment_processor import PaymentProcessor


def main(argv):
    """Valida argumentos y ejecuta la demo de pagos automaticos."""
    build_validation_chain().validate(argv)

    processor = PaymentProcessor(argv[1])

    # Demostracion: pedidos de pago de $500 ruteados automaticamente.
    for request_id in range(1, 7):
        payment = processor.request_payment(request_id, 500)
        if payment is not None:
            print(f"Pedido #{payment.request_id}: pago de ${payment.amount} "
                  f"realizado desde '{payment.token}'.")
        else:
            print(f"Pedido #{request_id}: rechazado, sin saldo suficiente.")

    print()
    processor.list_payments()
    print()
    print(f"Saldos finales: {processor.balances()}")


if __name__ == "__main__":
    main(sys.argv)
