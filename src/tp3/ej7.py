"""7. Imagine una situacion donde pueda ser de utilidad el patron Abstract Factory.

Situacion imaginada: generacion de facturas en papel o PDF.
Cada formato tiene su propio encabezado y cuerpo, pero el codigo cliente
los usa de la misma manera sin saber que formato concreto se esta usando.

Por que Abstract Factory y no los otros:
- Permite crear familias de objetos relacionados (encabezado + cuerpo) que
  deben ser consistentes entre si segun el formato elegido.
- Factory simple crea un solo tipo de objeto; aqui se crean dos componentes
  que deben pertenecer a la misma familia.
- Builder, Singleton y Prototype no aplican al problema.
"""


# --- Productos abstractos ---

class Encabezado:
    def mostrar(self):
        raise NotImplementedError


class Cuerpo:
    def mostrar(self):
        raise NotImplementedError


# --- Familia: papel ---

class EncabezadoPapel(Encabezado):
    def mostrar(self):
        print("=== FACTURA EN PAPEL ===")


class CuerpoPapel(Cuerpo):
    def mostrar(self):
        print("Detalle impreso en hoja A4")


# --- Familia: PDF ---

class EncabezadoPDF(Encabezado):
    def mostrar(self):
        print(">>> FACTURA PDF <<<")


class CuerpoPDF(Cuerpo):
    def mostrar(self):
        print("Detalle generado en archivo .pdf")


# --- Abstract Factory ---

class FacturaFactory:
    def crear_encabezado(self) -> Encabezado:
        raise NotImplementedError

    def crear_cuerpo(self) -> Cuerpo:
        raise NotImplementedError


class FacturaPapelFactory(FacturaFactory):
    def crear_encabezado(self) -> Encabezado:
        return EncabezadoPapel()

    def crear_cuerpo(self) -> Cuerpo:
        return CuerpoPapel()


class FacturaPDFFactory(FacturaFactory):
    def crear_encabezado(self) -> Encabezado:
        return EncabezadoPDF()

    def crear_cuerpo(self) -> Cuerpo:
        return CuerpoPDF()


# --- Cliente ---

def emitir_factura(factory: FacturaFactory):
    factory.crear_encabezado().mostrar()
    factory.crear_cuerpo().mostrar()


if __name__ == "__main__":
    print("--- Formato Papel ---")
    emitir_factura(FacturaPapelFactory())

    print("--- Formato PDF ---")
    emitir_factura(FacturaPDFFactory())
