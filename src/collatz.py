"""
Conjetura de Collatz (3n+1)

Este programa calcula el número de iteraciones necesarias para que 
la secuencia de Collatz converja a 1 para números entre 1 y 10000.

La conjetura de Collatz establece:
- Si n es par: n = n / 2
- Si n es impar: n = 3n + 1
- Se repite hasta llegar a 1
"""

import matplotlib.pyplot as plt


def calcular_collatz(n):
    """
    Calcula el número de iteraciones necesarias para que
    la secuencia de Collatz converja a 1.
    
    Args:
        n: número inicial
        
    Returns:
        número de iteraciones
    """
    iteraciones = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2  # Si es par, dividir entre 2
        else:
            n = 3 * n + 1  # Si es impar, 3n+1
        iteraciones += 1
    return iteraciones


def main():
    """
    Calcula la secuencia de Collatz para números entre 1 y 10000
    y genera un gráfico de convergencia.
    """
    print("Calculando conjetura de Collatz para números 1-10000...")
    
    # Listas para almacenar datos
    numeros = []
    iteraciones = []
    
    # Calcular iteraciones para cada número
    for n in range(1, 10001):
        num_iteraciones = calcular_collatz(n)
        numeros.append(n)
        iteraciones.append(num_iteraciones)
        
        # Mostrar progreso cada 1000 números
        if n % 1000 == 0:
            print(f"  Procesados {n} números...")
    
    print(f"✓ Cálculo completado")
    
    # Crear el gráfico
    print("Generando gráfico...")
    plt.figure(figsize=(14, 8))
    plt.scatter(iteraciones, numeros, s=1, alpha=0.5, color='blue')
    
    plt.xlabel('Número de Iteraciones', fontsize=12, fontweight='bold')
    plt.ylabel('Número n (inicial)', fontsize=12, fontweight='bold')
    plt.title('Conjetura de Collatz (3n+1): Iteraciones vs Número Inicial', 
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Agregar estadísticas
    max_iteraciones = max(iteraciones)
    min_iteraciones = min(iteraciones)
    promedio_iteraciones = sum(iteraciones) / len(iteraciones)
    
    # Texto con estadísticas
    stats_text = f'Min: {min_iteraciones} | Promedio: {promedio_iteraciones:.1f} | Máx: {max_iteraciones}'
    plt.text(0.5, 0.98, stats_text, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top', horizontalalignment='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Guardar gráfico
    plt.tight_layout()
    plt.savefig('doc/collatz_grafico.png', dpi=150, bbox_inches='tight')
    print(f"✓ Gráfico guardado en: doc/collatz_grafico.png")
    
    # Mostrar gráfico
    plt.show()
    
    # Imprimir algunos datos interesantes
    print("\n📊 Estadísticas:")
    print(f"   Iteraciones mínimas: {min_iteraciones}")
    print(f"   Iteraciones máximas: {max_iteraciones}")
    print(f"   Iteraciones promedio: {promedio_iteraciones:.2f}")
    
    # Encontrar el número con más iteraciones
    idx_max = iteraciones.index(max_iteraciones)
    print(f"   Número con más iteraciones: {numeros[idx_max]} ({max_iteraciones} iteraciones)")


if __name__ == "__main__":
    main()
