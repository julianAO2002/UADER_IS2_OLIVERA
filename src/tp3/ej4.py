"""4. Implemente una clase "factura" que tenga un importe correspondiente al total
de la factura pero de acuerdo a la condicion impositiva del cliente (IVA
Responsable, IVA No Inscripto, IVA Exento) genere facturas que indiquen tal
condicion.

Patron elegido: Factory
Por que: el problema requiere crear objetos de distintos tipos segun la condicion
impositiva del cliente. Factory encapsula la logica de creacion en un solo lugar,
devolviendo la subclase correcta segun el parametro recibido. Builder no aplica
porque no hay configuraciones opcionales complejas, sino tipos distintos de objeto.
Singleton no aplica porque se necesitan multiples facturas. Prototype clona
instancias existentes, lo cual no corresponde aqui.
"""


class Factura:
    def __init__(self, importe: float):
        self.importe = importe

    def mostrar(self):
        raise NotImplementedError


class FacturaResponsableInscripto(Factura):
    def mostrar(self):
        print(f"Factura A - IVA Responsable Inscripto | Total: ${self.importe:.2f}")


class FacturaNoInscripto(Factura):
    def mostrar(self):
        print(f"Factura B - IVA No Inscripto | Total: ${self.importe:.2f}")


class FacturaExento(Factura):
    def mostrar(self):
        print(f"Factura C - IVA Exento | Total: ${self.importe:.2f}")


class FacturaFactory:
    @staticmethod
    def crear(condicion: str, importe: float) -> Factura:
        tipos = {
            "responsable": FacturaResponsableInscripto,
            "no_inscripto": FacturaNoInscripto,
            "exento": FacturaExento,
        }
        if condicion not in tipos:
            raise ValueError(f"Condicion impositiva desconocida: {condicion}")
        return tipos[condicion](importe)


if __name__ == "__main__":
    f1 = FacturaFactory.crear("responsable", 1000.0)
    f2 = FacturaFactory.crear("no_inscripto", 2500.50)
    f3 = FacturaFactory.crear("exento", 800.0)

    f1.mostrar()
    f2.mostrar()
    f3.mostrar()
