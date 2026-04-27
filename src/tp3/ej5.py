"""5. Extienda el ejemplo visto en el taller en clase de forma que se pueda utilizar
para construir aviones en lugar de vehiculos. Para simplificar suponga que un
avion tiene un body, 2 turbinas, 2 alas y un tren de aterrizaje.

Patron elegido: Builder
Por que: un avion se construye ensamblando partes paso a paso (body, turbinas,
alas, tren de aterrizaje). Builder separa la construccion compleja en pasos
ordenados, con un Director que orquesta el proceso. Es la extension natural del
ejemplo de vehiculos visto en clase. Singleton no aplica porque se pueden
construir multiples aviones. Factory elige entre tipos distintos, no ensambla
partes. Prototype clona objetos existentes, lo cual no corresponde aqui.
"""


class Avion:
    def __init__(self):
        self.body = None
        self.turbinas = []
        self.alas = []
        self.tren_aterrizaje = None

    def __str__(self):
        return (
            f"Avion:\n"
            f"  Body: {self.body}\n"
            f"  Turbinas: {self.turbinas}\n"
            f"  Alas: {self.alas}\n"
            f"  Tren de aterrizaje: {self.tren_aterrizaje}"
        )


class AvionBuilder:
    def __init__(self):
        self._avion = Avion()

    def construir_body(self, tipo: str):
        self._avion.body = tipo
        return self

    def agregar_turbina(self, turbina: str):
        self._avion.turbinas.append(turbina)
        return self

    def agregar_ala(self, ala: str):
        self._avion.alas.append(ala)
        return self

    def construir_tren_aterrizaje(self, tipo: str):
        self._avion.tren_aterrizaje = tipo
        return self

    def build(self) -> Avion:
        return self._avion


class Director:
    def __init__(self, builder: AvionBuilder):
        self._builder = builder

    def construir_avion(self) -> Avion:
        return (
            self._builder
            .construir_body("fuselaje metalico")
            .agregar_turbina("turbina izquierda")
            .agregar_turbina("turbina derecha")
            .agregar_ala("ala izquierda")
            .agregar_ala("ala derecha")
            .construir_tren_aterrizaje("tren retractil")
            .build()
        )


if __name__ == "__main__":
    builder = AvionBuilder()
    director = Director(builder)
    avion = director.construir_avion()
    print(avion)
