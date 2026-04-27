"""6. Dado una clase que implemente el patron prototipo verifique que una clase
generada a partir de ella permite por su parte obtener tambien copias de si
misma.

Patron elegido: Prototype
Por que: el enunciado lo indica explicitamente. Prototype permite clonar objetos
existentes sin depender de su clase concreta. La verificacion clave es que un
clon puede a su vez generar otros clones, formando una cadena. Singleton no
aplica porque se necesitan multiples instancias. Factory y Builder crean objetos
nuevos desde cero, no copias de uno existente.
"""

import copy


class Prototipo:
    def __init__(self, nombre: str, datos: list):
        self.nombre = nombre
        self.datos = datos

    def clonar(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"Prototipo(nombre={self.nombre}, datos={self.datos}, id={id(self)})"


if __name__ == "__main__":
    original = Prototipo("original", [1, 2, 3])
    print(f"Original:      {original}")

    clon1 = original.clonar()
    clon1.nombre = "clon1"
    clon1.datos.append(4)
    print(f"Clon1:         {clon1}")

    # verificacion: el clon puede a su vez generar copias de si mismo
    clon2 = clon1.clonar()
    clon2.nombre = "clon2 (clon de clon1)"
    clon2.datos.append(5)
    print(f"Clon2:         {clon2}")

    # verificar que son objetos independientes
    print(f"\nOriginal no modificado: {original}")
    print(f"Clon1 no modificado por clon2: {clon1}")
