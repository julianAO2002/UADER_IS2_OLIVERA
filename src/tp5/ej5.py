import os
#*--------------------------------------------------------------------
#* Ejercicio 5: Patrón Memento con historial de 4 estados y undo con índice
#*--------------------------------------------------------------------
class Memento:
    def __init__(self, file, content):
        self.file = file
        self.content = content


class FileWriterUtility:

    def __init__(self, file):
        self.file = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        return Memento(self.file, self.content)

    def undo(self, memento):
        self.file = memento.file
        self.content = memento.content


class FileWriterCaretaker:

    MAX_HISTORY = 4

    def __init__(self):
        self._history = []

    def save(self, writer):
        memento = writer.save()
        self._history.append(memento)
        if len(self._history) > self.MAX_HISTORY:
            self._history.pop(0)

    def undo(self, writer, steps=0):
        """
        steps=0: recupera el estado inmediato anterior
        steps=1,2,3: recupera estados más antiguos
        """
        index = -(1 + steps)
        if abs(index) > len(self._history):
            print(f"No hay suficientes estados guardados para retroceder {steps + 1} paso(s).")
            return
        writer.undo(self._history[index])


if __name__ == '__main__':

    os.system("cls" if os.name == "nt" else "clear")
    print("Crea un objeto que gestionará la versión anterior")
    caretaker = FileWriterCaretaker()

    print("Crea el objeto cuyo estado se quiere preservar")
    writer = FileWriterUtility("GFG.txt")

    print("Se graba algo en el objeto y se salva")
    writer.write("Clase de IS2 en UADER\n")
    print(writer.content + "\n")
    caretaker.save(writer)

    print("Se graba información adicional")
    writer.write("Material adicional de la clase de patrones\n")
    print(writer.content + "\n")
    caretaker.save(writer)

    print("Se graba información adicional II")
    writer.write("Material adicional de la clase de patrones II\n")
    print(writer.content + "\n")
    caretaker.save(writer)

    print("Se graba información adicional III")
    writer.write("Material adicional de la clase de patrones III\n")
    print(writer.content + "\n")
    caretaker.save(writer)

    print("se invoca al <undo> con steps=0 (estado inmediato anterior)")
    caretaker.undo(writer, steps=0)
    print("Estado actual:")
    print(writer.content + "\n")

    print("se invoca al <undo> con steps=2 (3 estados atrás)")
    caretaker.undo(writer, steps=2)
    print("Estado actual:")
    print(writer.content + "\n")
