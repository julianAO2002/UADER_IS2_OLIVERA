"""Patrón Flyweight: caracteres en un editor de texto.

Situación: un editor de texto maneja miles de caracteres en pantalla.
Cada caracter tiene un estilo (fuente, tamaño, color) que se repite mucho.
En lugar de crear un objeto por cada caracter, se comparte el objeto de estilo
(estado intrínseco) y solo se guarda la posición (estado extrínseco) por separado.
"""


class EstiloCaracter:
    """Flyweight: objeto compartido que almacena el estado intrínseco."""

    def __init__(self, fuente: str, tamaño: int, color: str):
        self.fuente = fuente
        self.tamaño = tamaño
        self.color = color

    def renderizar(self, char: str, x: int, y: int) -> None:
        print(f"'{char}' en ({x},{y}) | fuente={self.fuente} tamaño={self.tamaño} color={self.color}")


class FabricaEstilos:
    """Fábrica que garantiza que cada estilo único se instancia una sola vez."""

    def __init__(self):
        self._estilos: dict[tuple, EstiloCaracter] = {}

    def obtener(self, fuente: str, tamaño: int, color: str) -> EstiloCaracter:
        clave = (fuente, tamaño, color)
        if clave not in self._estilos:
            self._estilos[clave] = EstiloCaracter(fuente, tamaño, color)
        return self._estilos[clave]

    def total_instancias(self) -> int:
        return len(self._estilos)


if __name__ == "__main__":
    fabrica = FabricaEstilos()

    # Documento con muchos caracteres, pero pocos estilos distintos
    documento = [
        ("H", 0, 0, "Arial", 12, "negro"),
        ("o", 1, 0, "Arial", 12, "negro"),
        ("l", 2, 0, "Arial", 12, "negro"),
        ("a", 3, 0, "Arial", 12, "negro"),
        ("!", 4, 0, "Arial", 14, "rojo"),
        ("M", 0, 1, "Arial", 12, "negro"),
        ("u", 1, 1, "Arial", 12, "negro"),
        ("n", 2, 1, "Arial", 12, "negro"),
        ("d", 3, 1, "Arial", 12, "negro"),
        ("o", 4, 1, "Arial", 14, "rojo"),
    ]

    for char, x, y, fuente, tamaño, color in documento:
        estilo = fabrica.obtener(fuente, tamaño, color)
        estilo.renderizar(char, x, y)

    print(f"\nCaracteres totales: {len(documento)}")
    print(f"Instancias de EstiloCaracter creadas: {fabrica.total_instancias()} (en lugar de {len(documento)})")
