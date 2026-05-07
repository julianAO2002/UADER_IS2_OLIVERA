"""Patrón Composite: Ensamblado jerárquico de piezas."""


class Componente:
    def __init__(self, nombre: str):
        self.nombre = nombre

    def mostrar(self, nivel: int = 0) -> None:
        raise NotImplementedError


class Pieza(Componente):
    def mostrar(self, nivel: int = 0) -> None:
        print("  " * nivel + f"- {self.nombre}")


class Conjunto(Componente):
    def __init__(self, nombre: str):
        super().__init__(nombre)
        self.hijos: list[Componente] = []

    def agregar(self, componente: Componente) -> None:
        self.hijos.append(componente)

    def mostrar(self, nivel: int = 0) -> None:
        print("  " * nivel + f"[{self.nombre}]")
        for hijo in self.hijos:
            hijo.mostrar(nivel + 1)


if __name__ == "__main__":
    producto = Conjunto("Producto Principal")

    for i in range(1, 4):
        sub = Conjunto(f"Subconjunto {i}")
        for j in range(1, 5):
            sub.agregar(Pieza(f"Pieza {i}.{j}"))
        producto.agregar(sub)

    producto.mostrar()

    print("\n-- Agregando subconjunto opcional --\n")
    opcional = Conjunto("Subconjunto Opcional")
    for j in range(1, 5):
        opcional.agregar(Pieza(f"Pieza 4.{j}"))
    producto.agregar(opcional)

    producto.mostrar()
