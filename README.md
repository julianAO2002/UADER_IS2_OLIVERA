# 🔍 Generador de Números Primos

## Propósito del Repositorio

Este repositorio contiene la implementación de un **programa educativo en Python** diseñado para identificar y visualizar los números primos dentro de un intervalo específico. El proyecto es parte del curso **Ingeniería de Software 2** de la Universidad Autónoma de Entre Ríos (UADER).

### 📋 Objetivos Principales

El proyecto busca:
- Comprender los algoritmos de búsqueda de números primos
- Aplicar conceptos de control de flujo en Python
- Implementar soluciones eficientes para problemas matemáticos

## 🚀 Características del Proyecto

### Estructura del Repositorio

* **src/** - Contiene el código fuente principal
* **doc/** - Documentación del proyecto
* **bin/** - Archivos ejecutables y compilados
* **script/** - Scripts auxiliares para automatización

### Funcionalidades Principales

1. **Detección de números primos** - Identifica todos los números primos en un rango definido
2. **Rango configurable** - Permite establecer intervalos personalizados
3. **Algoritmo simple** - Implementa un método directo de verificación por divisibilidad

## 💻 Uso del Programa

### Requisitos

* Python 3.x instalado en el sistema
* Acceso a terminal o línea de comandos

### Pasos para Ejecutar

1. Navegar al directorio raíz del proyecto
2. Ejecutar el comando: `python src/primes.py`
3. El programa mostrará todos los números primos entre 1 y 500

## 🔬 Algoritmo Implementado

### Concepto Base

El programa verifica cada número en el rango evaluando si posee divisores además de 1 y él mismo.

**Pseudocódigo:**

```
Para cada número n en [1, 500]:
    Si n > 1:
        Verificar divisores desde 2 hasta n-1
        Si no hay divisores:
            El número es primo → mostrar
        Si hay divisores:
            El número no es primo → descartar
```

### Complejidad del Algoritmo

* **Complejidad temporal:** O(n²) - peor caso
* **Complejidad espacial:** O(1) - sin uso de memoria adicional

## 📊 Ejemplo de Salida

```
Prime numbers between 1 and 500 are:
2
3
5
7
11
13
17
19
23
29
...
```

## 🎓 Conceptos Educativos

### Temas Cubiertos

* Iteración y bucles en Python
* Condicionales y control de flujo
* Uso del `else` en bucles `for`
* Operador módulo para verificación de divisibilidad

### Mejoras Futuras

- Implementar el algoritmo de Criba de Eratóstenes para mejor eficiencia
- Agregar interfaz gráfica de usuario
- Crear versiones en otros lenguajes de programación
- Optimizar para rangos más grandes

## 📚 Referencias y Recursos

Para profundizar en el tema de números primos y algoritmos, consulta:

- **[Khan Academy - Números Primos](https://www.khanacademy.org/math/arithmetic-home/factors-multiples/prime-numbers/v/prime-numbers)** - Recurso educativo sobre teoría de números primos
- [Documentación oficial de Python 3](https://docs.python.org/3/)
- [Wikipedia - Número Primo](https://es.wikipedia.org/wiki/N%C3%BAmero_primo)

## 👥 Autor

Desarrollado como parte del curso **Ingeniería de Software 2**  
**Universidad Autónoma de Entre Ríos (UADER)**

---

### 📝 Notas Importantes

* Este código es de propósito educativo
* Se recomienda revisar y entender cada línea del código
* Para proyectos de producción, considerar algoritmos más optimizados

**Última actualización:** 31 de marzo de 2026