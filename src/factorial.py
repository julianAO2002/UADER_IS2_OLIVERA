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

# Verificar si se pasó un argumento
if len(sys.argv) < 2:
    # Si no se pasó argumento, solicitar al usuario
    try:
        num = int(input("Ingrese un número para calcular el factorial: "))
    except ValueError:
        print("Error: Debe ingresar un número válido")
        sys.exit()
else:
    # Si se pasó argumento, usarlo
    try:
        num = int(sys.argv[1])
    except ValueError:
        print("Error: El argumento debe ser un número válido")
        sys.exit()

print("Factorial ",num,"! es ", factorial(num)) 

