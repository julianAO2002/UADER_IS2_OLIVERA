"""Patrón Bridge: Láminas de acero y trenes laminadores."""


class TrenLaminador:
    def producir(self, espesor: float, ancho: float) -> None:
        raise NotImplementedError


class TrenLaminador5m(TrenLaminador):
    def producir(self, espesor: float, ancho: float) -> None:
        print(f"Tren 5m: produciendo plancha de {espesor}\" x {ancho}m x 5m")


class TrenLaminador10m(TrenLaminador):
    def producir(self, espesor: float, ancho: float) -> None:
        print(f"Tren 10m: produciendo plancha de {espesor}\" x {ancho}m x 10m")


class LaminaAcero:
    def __init__(self, espesor: float, ancho: float, tren: TrenLaminador):
        self.espesor = espesor
        self.ancho = ancho
        self.tren = tren

    def producir(self) -> None:
        self.tren.producir(self.espesor, self.ancho)


if __name__ == "__main__":
    tren5 = TrenLaminador5m()
    tren10 = TrenLaminador10m()

    lamina_a = LaminaAcero(0.5, 1.5, tren5)
    lamina_b = LaminaAcero(0.5, 1.5, tren10)

    lamina_a.producir()
    lamina_b.producir()
