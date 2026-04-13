"""
Programa de cálculo de factorial usando Programación Orientada a Objetos (OOP)
Implementa una clase Factorial con soporte para rangos
"""

import sys


class Factorial:
    """
    Clase para calcular factoriales.
    
    Atributos:
        resultados (list): Lista de tuplas (número, factorial)
    """
    
    def __init__(self):
        """Inicializa la instancia de Factorial con una lista vacía de resultados."""
        self.resultados = []
    
    def _calcular_factorial(self, n):
        """
        Calcula el factorial de un número.
        
        Args:
            n (int): Número del cual calcular el factorial
            
        Returns:
            int: El factorial de n
        """
        if n < 0:
            raise ValueError("No se puede calcular factorial de números negativos")
        if n == 0 or n == 1:
            return 1
        
        resultado = 1
        for i in range(2, n + 1):
            resultado *= i
        return resultado
    
    def procesar_rango(self, entrada):
        """
        Procesa una entrada en formato "-hasta", "desde-", "desde-hasta" o número simple.
        
        Args:
            entrada (str): String con el rango o número
            
        Returns:
            tuple: (desde, hasta) en formato entero
        """
        entrada = entrada.strip()
        
        # Caso: número simple (ej. "5")
        if '-' not in entrada:
            numero = int(entrada)
            return (numero, numero)
        
        # Caso: "-hasta" (ej. "-10")
        if entrada.startswith('-'):
            hasta = int(entrada[1:])
            return (1, hasta)
        
        # Caso: "desde-" (ej. "5-")
        if entrada.endswith('-'):
            desde = int(entrada[:-1])
            return (desde, 60)
        
        # Caso: "desde-hasta" (ej. "4-8")
        partes = entrada.split('-')
        if len(partes) == 2:
            desde = int(partes[0])
            hasta = int(partes[1])
            return (desde, hasta)
        
        raise ValueError(f"Formato de rango inválido: {entrada}")
    
    def run(self, min_val, max_val):
        """
        Calcula los factoriales entre min_val y max_val (inclusive).
        
        Args:
            min_val (int): Número mínimo del rango
            max_val (int): Número máximo del rango
            
        Raises:
            ValueError: Si los parámetros son inválidos
        """
        # Convertir a int si son strings
        min_val = int(min_val)
        max_val = int(max_val)
        
        # Validaciones
        if min_val <= 0:
            raise ValueError("El número mínimo debe ser mayor a 0")
        if max_val <= 0:
            raise ValueError("El número máximo debe ser mayor a 0")
        if min_val > max_val:
            raise ValueError(f"El rango es inválido: {min_val} > {max_val}")
        
        # Limpiar resultados previos
        self.resultados = []
        
        # Calcular factoriales
        for numero in range(min_val, max_val + 1):
            factorial = self._calcular_factorial(numero)
            self.resultados.append((numero, factorial))
            print(f"{numero}! = {factorial}")
    
    def obtener_resultados(self):
        """
        Retorna los resultados calculados.
        
        Returns:
            list: Lista de tuplas (número, factorial)
        """
        return self.resultados


def main():
    """Función principal del programa."""
    
    # Crear instancia de la clase Factorial
    calc = Factorial()
    
    # Solicitar entrada al usuario
    entrada = sys.argv[1] if len(sys.argv) > 1 else input(
        "Ingrese un número o rango (ej. 5, 4-8, -10, 5-): "
    )
    
    try:
        # Procesar el rango
        desde, hasta = calc.procesar_rango(entrada)
        
        # Calcular factoriales
        print(f"\nCalculando factoriales del {desde} al {hasta}:\n")
        calc.run(desde, hasta)
        
        # Mostrar resumen
        print(f"\nTotal de factoriales calculados: {len(calc.obtener_resultados())}")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Formatos válidos:")
        print("  - Número simple: 5")
        print("  - Rango completo: 4-8")
        print("  - Sin límite inferior: -10 (calcula desde 1 hasta 10)")
        print("  - Sin límite superior: 5- (calcula desde 5 hasta 60)")
        sys.exit(1)


if __name__ == "__main__":
    main()
