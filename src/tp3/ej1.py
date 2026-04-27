"""1. Provea una clase que dado un número entero cualquiera retorne el factorial del
mismo, debe asegurarse que todas las clases que lo invoquen utilicen la misma
instancia de clase."""


class Factorial:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def calcular(self, n: int) -> int:
        if n < 0:
            raise ValueError("No existe factorial de números negativos")
        resultado = 1
        for i in range(2, n + 1):
            resultado *= i
        return resultado


if __name__ == "__main__":
    a = Factorial()
    b = Factorial()

    print(f"Misma instancia: {a is b}")
    print(f"5! = {a.calcular(5)}")
    print(f"10! = {b.calcular(10)}")
