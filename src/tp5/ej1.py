#!/usr/bin/env python3
"""TP5 - Ejercicio 1: Patrón Cadena de Responsabilidad"""


class Handler:
    def __init__(self):
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    def handle(self, number):
        if self._next:
            return self._next.handle(number)
        return False


class PrimeHandler(Handler):
    def _is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def handle(self, number):
        if self._is_prime(number):
            print(f"  {number}: consumido por PrimeHandler (primo)")
            return True
        return super().handle(number)


class EvenHandler(Handler):
    def handle(self, number):
        if number % 2 == 0:
            print(f"  {number}: consumido por EvenHandler (par)")
            return True
        return super().handle(number)


if __name__ == "__main__":
    prime_handler = PrimeHandler()
    even_handler = EvenHandler()
    prime_handler.set_next(even_handler)

    print("Procesando números del 1 al 100:")
    for n in range(1, 101):
        if not prime_handler.handle(n):
            print(f"  {n}: no consumido")
