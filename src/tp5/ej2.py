#!/usr/bin/env python3
"""TP5 - Ejercicio 2: Patrón Iterator"""


class StringIterator:
    def __init__(self, string, reverse=False):
        self._string = string
        self._reverse = reverse
        self._index = len(string) - 1 if reverse else 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._reverse:
            if self._index < 0:
                raise StopIteration
            char = self._string[self._index]
            self._index -= 1
        else:
            if self._index >= len(self._string):
                raise StopIteration
            char = self._string[self._index]
            self._index += 1
        return char


class StringCollection:
    def __init__(self, string):
        self._string = string

    def forward(self):
        return StringIterator(self._string, reverse=False)

    def reverse(self):
        return StringIterator(self._string, reverse=True)


if __name__ == "__main__":
    cadena = "Ingeniería de Software II"
    collection = StringCollection(cadena)

    print(f"Cadena original: {cadena}\n")

    print("Recorrido directo:")
    print("".join(collection.forward()))

    print("\nRecorrido reverso:")
    print("".join(collection.reverse()))
