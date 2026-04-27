"""2. Elabore una clase para el cálculo del valor de impuestos a ser utilizado por
todas las clases que necesiten realizarlo. El cálculo de impuestos simplificado
deberá recibir un valor de importe base imponible y deberá retornar la suma
del cálculo de IVA (21%), IIBB (5%) y Contribuciones municipales (1,2%) sobre
esa base imponible.

Patrón elegido: Singleton
Por qué: el enunciado pide que la clase sea "utilizada por todas las clases que
necesiten realizarlo", lo que implica una única instancia compartida. Las tasas
impositivas son constantes (no hay estado mutable), por lo que no hay necesidad
de crear múltiples instancias. Factory y Builder sirven para construir objetos con
variantes; Prototype para clonar objetos costosos. Ninguno aplica aquí.
"""


class CalculadorImpuestos:
    _instance = None

    IVA = 0.21
    IIBB = 0.05
    CONTRIBUCIONES = 0.012

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def calcular(self, base_imponible: float) -> float:
        iva = base_imponible * self.IVA
        iibb = base_imponible * self.IIBB
        contribuciones = base_imponible * self.CONTRIBUCIONES
        return iva + iibb + contribuciones


if __name__ == "__main__":
    a = CalculadorImpuestos()
    b = CalculadorImpuestos()

    print(f"Misma instancia: {a is b}")
    base = 1000.0
    total_impuestos = a.calcular(base)
    print(f"Base imponible: ${base:.2f}")
    print(f"IVA (21%):      ${base * CalculadorImpuestos.IVA:.2f}")
    print(f"IIBB (5%):      ${base * CalculadorImpuestos.IIBB:.2f}")
    print(f"Contrib (1.2%): ${base * CalculadorImpuestos.CONTRIBUCIONES:.2f}")
    print(f"Total impuestos: ${total_impuestos:.2f}")