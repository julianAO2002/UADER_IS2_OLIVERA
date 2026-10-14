"""Conjetura de Collatz: iteraciones necesarias para alcanzar el valor 1."""
import sys

LIMITE = 1999


# Calculando el número de iteraciones del algoritmo de Collatz
def collatz(num):
    """Devuelve las iteraciones necesarias para que num llegue a 1."""
    iteraciones = 0
    while num != 1:
        if num % 2 == 0:
            num = num // 2
        else:
            num = 3 * num + 1
        iteraciones += 1
    return iteraciones


# Valida que el texto sea un entero en el rango [1, LIMITE]
def validar_entrada(texto):
    """Convierte texto a entero; ValueError si no es válido o fuera de rango."""
    numero = int(texto.strip())
    if numero < 1 or numero > LIMITE:
        raise ValueError("fuera de rango")
    return numero


# Solicita el número por teclado hasta que sea válido
def main():
    """Pide un entero por teclado e imprime el número y sus iteraciones."""
    while True:
        try:
            texto = input("Ingrese un número entero entre 1 y %d: " % LIMITE)
        except EOFError:
            print("\nFin de la entrada: no se ingresó un número válido.")
            return 1
        try:
            numero = validar_entrada(texto)
        except ValueError:
            print("Error: '%s' no es un entero entre 1 y %d." % (texto, LIMITE))
            continue
        print("El número de iteraciones para %d es %d" % (numero, collatz(numero)))
        return 0


if __name__ == "__main__":
    sys.exit(main())
