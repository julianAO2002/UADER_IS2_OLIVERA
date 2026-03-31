#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys
def factorial(num): 
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
        
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

# Función para procesar entrada en formato "desde-hasta"
def procesar_rango(entrada):
    """Procesa entrada en formato 'desde-hasta' o un número simple"""
    if '-' in entrada:
        partes = entrada.split('-')
        if len(partes) != 2:
            return None
        try:
            desde = int(partes[0])
            hasta = int(partes[1])
            if desde > hasta:
                return None
            return (desde, hasta)
        except ValueError:
            return None
    else:
        try:
            num = int(entrada)
            return (num, num)
        except ValueError:
            return None

# Verificar si se pasó un argumento
if len(sys.argv) < 2:
    # Si no se pasó argumento, solicitar al usuario
    entrada = input("Ingrese un número o rango (ej. 4 o 4-8): ")
else:
    # Si se pasó argumento, usarlo
    entrada = sys.argv[1]

# Procesar la entrada
rango = procesar_rango(entrada)
if rango is None:
    print("Error: Formato inválido. Use un número (ej. 5) o rango (ej. 4-8)")
    sys.exit()

desde, hasta = rango

# Calcular y mostrar factoriales
print(f"\n--- Cálculo de Factoriales de {desde} a {hasta} ---")
for num in range(desde, hasta + 1):
    resultado = factorial(num)
    print(f"Factorial de {num}! = {resultado}")
print() 

