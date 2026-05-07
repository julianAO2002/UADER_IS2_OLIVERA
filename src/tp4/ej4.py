"""Patrón Decorator: operaciones sucesivas sobre un número."""


class Numero:
    def __init__(self, valor: float):
        self._valor = valor

    def obtener(self) -> float:
        return self._valor

    def imprimir(self) -> None:
        print(f"Valor: {self.obtener()}")


class DecoradorNumero(Numero):
    def __init__(self, numero: Numero):
        self._numero = numero

    def obtener(self) -> float:
        return self._numero.obtener()


class SumarDos(DecoradorNumero):
    def obtener(self) -> float:
        return self._numero.obtener() + 2


class MultiplicarPorDos(DecoradorNumero):
    def obtener(self) -> float:
        return self._numero.obtener() * 2


class DividirPorTres(DecoradorNumero):
    def obtener(self) -> float:
        return self._numero.obtener() / 3


if __name__ == "__main__":
    base = Numero(6)

    print("Sin decoradores:")
    base.imprimir()

    print("\nCon +2:")
    SumarDos(base).imprimir()

    print("\nCon +2, luego x2:")
    MultiplicarPorDos(SumarDos(base)).imprimir()

    print("\nCon +2, luego x2, luego /3:")
    DividirPorTres(MultiplicarPorDos(SumarDos(base))).imprimir()
