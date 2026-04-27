"""3. Genere una clase donde se instancie una comida rapida 'hamburguesa' que
pueda ser entregada en mostrador, retirada por el cliente o enviada por
delivery. A los efectos practicos bastara que la clase imprima el metodo de
entrega.

Patron elegido: Builder
Por que: la hamburguesa es siempre el mismo producto base, pero se construye con
distintas configuraciones de entrega. Builder permite separar la construccion del
objeto de su representacion final, agregando pasos opcionales (metodo de entrega)
antes de obtener el objeto terminado. Singleton no aplica porque se necesitan
multiples pedidos. Factory crearia subclases innecesarias para algo que es el
mismo producto. Prototype clona objetos existentes, lo cual no corresponde aqui.
"""


class Hamburguesa:
    def __init__(self, metodo_entrega: str):
        self.metodo_entrega = metodo_entrega

    def entregar(self):
        print(f"Hamburguesa entregada por: {self.metodo_entrega}")


class HamburguesaBuilder:
    def __init__(self):
        self._metodo_entrega = None

    def en_mostrador(self):
        self._metodo_entrega = "mostrador"
        return self

    def retiro_cliente(self):
        self._metodo_entrega = "retiro por el cliente"
        return self

    def delivery(self):
        self._metodo_entrega = "delivery"
        return self

    def build(self) -> Hamburguesa:
        if self._metodo_entrega is None:
            raise ValueError("Debe especificar un metodo de entrega")
        return Hamburguesa(self._metodo_entrega)


if __name__ == "__main__":
    pedido1 = HamburguesaBuilder().en_mostrador().build()
    pedido2 = HamburguesaBuilder().retiro_cliente().build()
    pedido3 = HamburguesaBuilder().delivery().build()

    pedido1.entregar()
    pedido2.entregar()
    pedido3.entregar()
