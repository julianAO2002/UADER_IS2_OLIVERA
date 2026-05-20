import os
#*--------------------------------------------------------------------
#* Ejercicio 4: Patrón State - Scanner con memorias AM/FM (M1-M4)
#*--------------------------------------------------------------------
"""State class: Base State class"""
class State:

    def scan(self):

        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print("Sintonizando... Estación {} {}".format(self.stations[self.pos], self.name))

#*------- Implementa como barrer las estaciones de AM
class AmState(State):

    def __init__(self, radio):

        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate

#*------- Implementa como barrer las estaciones de FM
"""Separate class for FM state"""
class FmState(State):

    def __init__(self, radio):

        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate

#*------- Clase para representar una memoria de frecuencia
class Memory:
    def __init__(self, label, band, frequency):
        self.label = label
        self.band = band        # "AM" o "FM"
        self.frequency = frequency

    def tune(self):
        print("Sintonizando memoria {} -> {} {}".format(self.label, self.frequency, self.band))

#*--------- Construye la radio con todas sus formas de sintonía
class Radio:

    def __init__(self):

        self.fmstate = FmState(self)
        self.amstate = AmState(self)

#*--- Inicialmente en FM
        self.state = self.fmstate

#*--- Memorias M1-M4 con frecuencias AM y FM
        self.memories = [
            Memory("M1", "FM", "98.7"),
            Memory("M2", "AM", "870"),
            Memory("M3", "FM", "105.5"),
            Memory("M4", "AM", "1110"),
        ]

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()

    def scan_memories(self):
        print("-- Barrido de memorias --")
        for memory in self.memories:
            memory.tune()
        print("-- Fin de memorias --")

#*---------------------

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("\nCrea un objeto radio y almacena las siguientes acciones")
    radio = Radio()
    actions = [radio.scan] * 3 + [radio.toggle_amfm] + [radio.scan] * 3
    actions *= 2

#*---- Recorre las acciones ejecutando la acción y luego barre memorias

    print("Recorre las acciones ejecutando la acción, el objeto cambia la interfaz según el estado")
    for action in actions:
        action()

    print()
    radio.scan_memories()
