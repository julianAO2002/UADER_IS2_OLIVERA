#!/usr/bin/env python3
"""TP5 - Ejercicio 3: Patrón Observer"""


class EventSystem:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, listener):
        self._subscribers.append(listener)

    def emit(self, id_emitido):
        print(f"Emitiendo ID: {id_emitido}")
        for subscriber in self._subscribers:
            subscriber.update(id_emitido)


class Listener:
    def __init__(self, own_id):
        self._id = own_id

    def update(self, id_emitido):
        if id_emitido == self._id:
            print(f"  -> Listener [{self._id}]: ¡ID coincide! Mensaje recibido.")


if __name__ == "__main__":
    event_system = EventSystem()

    l1 = Listener("A1B2")
    l2 = Listener("C3D4")
    l3 = Listener("E5F6")
    l4 = Listener("G7H8")

    for listener in [l1, l2, l3, l4]:
        event_system.subscribe(listener)

    ids_a_emitir = ["A1B2", "XXXX", "C3D4", "E5F6", "ZZZZ", "G7H8", "A1B2", "1234"]

    print("=== Sistema de notificación Observer ===\n")
    for id_emitido in ids_a_emitir:
        event_system.emit(id_emitido)
        print()
