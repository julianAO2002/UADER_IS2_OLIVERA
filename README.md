# UADER IS2 - Ingeniería de Software 2

Repositorio de trabajos prácticos del curso **Ingeniería de Software 2** de la Universidad Autónoma de Entre Ríos (UADER).

## Estructura del Repositorio

```text
src/
├── tp1/        Ejercicios introductorios (primos, factorial, Collatz)
├── tp3/        Ejercicios varios
├── tp4/        Patrones de diseño estructurales
├── tp5/        Patrones de diseño de comportamiento
├── tp6/        Ingeniería reversa de getJason
├── tp7/        Refactorización con patrones de diseño
├── tp8/        Re-ingeniería del proceso de pagos (arquitectura en capas)
└── ChatGPT/    Calculadora RPN
doc/            Documentación y gráficos
```

## Trabajos Prácticos

### TP1

Ejercicios introductorios en Python: números primos, factorial (OOP), conjetura de Collatz.

### TP3

Ejercicios varios de programación orientada a objetos.

### TP4 - Patrones Estructurales

Implementación de patrones de diseño estructurales: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.

### TP5 - Patrones de Comportamiento
Implementación de patrones de diseño de comportamiento:

1. **Chain of Responsibility** - Cadena que procesa números 1-100 clasificándolos en primos, pares o sin consumir.
2. **Iterator** - Iterador sobre una cadena de caracteres en sentido directo y reverso.
3. **Observer** - Sistema de notificación donde listeners reaccionan cuando se emite su propio ID.
4. **State (Scanner)** - Radio con barrido de estaciones AM/FM y memorias M1-M4.
5. **Memento (Memory)** - Historial de hasta 4 estados con recuperación por índice (`undo(steps=0..3)`).

### TP6 - Ingeniería Reversa

Ingeniería reversa del programa `getJason.py` a partir de su bytecode compilado (`.pyc`): decompilación y reconstrucción del código fuente.

### TP7 - Refactorización con Patrones de Diseño

Refactorización de `getJason.py` aplicando **Singleton** y **Chain of Responsibility**, con la estrategia **Branching by Abstraction** para alternar entre la versión original y la refactorizada. Análisis estático con pylint (10.00/10).

### TP8 - Re-ingeniería del Proceso de Pagos

Re-ingeniería que automatiza la selección de cuenta para liberar pagos: basta con que exista saldo y los pagos se distribuyen de forma balanceada (alternada) entre `token1` ($1000) y `token2` ($2000).

- **Patrones**: Singleton (token → clave), Chain of Command (cuentas), Iterator (listado cronológico de pagos), Chain of Responsibility (validación de argumentos).
- **Arquitectura en capas** organizada en paquetes: `config/`, `presentation/`, `business/`, `domain/`, `data/`.
- Versión 1.2.0 — pylint 10.00/10.

## Requisitos

- Python 3.x

## Autor

**Julian Olivera**  
Ingeniería de Software 2 — UADER
