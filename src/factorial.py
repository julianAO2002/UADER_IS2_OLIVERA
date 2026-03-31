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
    """Procesa entrada en formato:
    - 'número' (ej. 5): calcula solo ese número
    - 'desde-hasta' (ej. 4-8): calcula rango completo
    - '-hasta' (ej. -10): calcula desde 1 hasta el número
    - 'desde-' (ej. 5-): calcula desde el número hasta 60
    """
    if '-' in entrada:
        partes = entrada.split('-')
        
        # Filtrar cadenas vacías para manejar "-10" y "5-"
        if len(partes) == 2:
            desde_str, hasta_str = partes
            
            try:
                # Convertir a enteros con límites por defecto
                desde = int(desde_str) if desde_str else 1  # Si está vacío, desde = 1
                hasta = int(hasta_str) if hasta_str else 60  # Si está vacío, hasta = 60
                
                # Validar que los valores sean válidos
                if desde < 1 or hasta < 1:
                    print("Error: Los números deben ser mayores a 0")
                    return None
                
                # Validar que desde no sea mayor que hasta
                if desde > hasta:
                    print(f"Error: El primer número ({desde}) no puede ser mayor que el segundo ({hasta})")
                    return None
                
                return (desde, hasta)
            except ValueError:
                print("Error: Los valores deben ser números enteros válidos")
                return None
        else:
            return None
    else:
        # Entrada simple: un solo número
        try:
            num = int(entrada)
            if num < 1:
                print("Error: El número debe ser mayor a 0")
                return None
            return (num, num)
        except ValueError:
            print("Error: Debe ingresar un número entero válido")
            return None

# Verificar si se pasó un argumento
if len(sys.argv) < 2:
    # Si no se pasó argumento, solicitar al usuario
    entrada = input("Ingrese un número o rango (ej. 5, 4-8, -10, 5-): ")
else:
    # Si se pasó argumento, usarlo
    entrada = sys.argv[1]

# Procesar la entrada
rango = procesar_rango(entrada)
if rango is None:
    print("Error: Formato inválido. Use:")
    print("  - Un número simple (ej. 5)")
    print("  - Rango completo (ej. 4-8)")
    print("  - Hasta un número (ej. -10, desde 1 hasta 10)")
    print("  - Desde un número (ej. 5-, desde 5 hasta 60)")
    sys.exit()

desde, hasta = rango

# Calcular y mostrar factoriales
print(f"\n--- Cálculo de Factoriales de {desde} a {hasta} ---")
for num in range(desde, hasta + 1):
    resultado = factorial(num)
    print(f"Factorial de {num}! = {resultado}")
print() 

