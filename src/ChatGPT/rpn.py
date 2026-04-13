#!/usr/bin/env python3
"""
Módulo de evaluación de expresiones en notación polaca inversa (RPN).

Soporta operaciones aritméticas básicas, funciones trigonométricas,
operaciones de pila, constantes matemáticas y registros de memoria.
El despacho de operaciones usa polimorfismo: cada operación es una
clase con un método apply(stack, mem) que encapsula su lógica.
"""

import math
import sys


class RPNError(Exception):
    """Excepción lanzada ante cualquier error semántico en la evaluación RPN."""


# ---------------------------------------------------------------------------
# Jerarquía de operaciones (polimorfismo)
# ---------------------------------------------------------------------------


class Operation:
    """Clase base abstracta para todas las operaciones RPN."""

    def apply(self, stack, mem):
        """Ejecuta la operación sobre la pila y los registros de memoria."""
        raise NotImplementedError


class _Pop:
    """Mixin auxiliar: extrae el tope de la pila con verificación."""

    @staticmethod
    def pop(stack):
        """Extrae el tope de la pila; lanza RPNError si está vacía."""
        if not stack:
            raise RPNError("Pila insuficiente")
        return stack.pop()


# --- Constantes matemáticas ---


class ConstantOp(Operation):
    """Empuja una constante matemática predefinida a la pila."""

    def __init__(self, value):
        """Inicializa con el valor numérico de la constante."""
        self._value = value

    def apply(self, stack, mem):
        """Empuja el valor constante al tope de la pila."""
        stack.append(self._value)


# --- Operaciones aritméticas binarias ---


class AddOp(_Pop, Operation):
    """Suma los dos operandos superiores de la pila."""

    def apply(self, stack, mem):
        b, a = self.pop(stack), self.pop(stack)
        stack.append(a + b)


class SubOp(_Pop, Operation):
    """Resta el tope de la pila al segundo elemento."""

    def apply(self, stack, mem):
        b, a = self.pop(stack), self.pop(stack)
        stack.append(a - b)


class MulOp(_Pop, Operation):
    """Multiplica los dos operandos superiores de la pila."""

    def apply(self, stack, mem):
        b, a = self.pop(stack), self.pop(stack)
        stack.append(a * b)


class DivOp(_Pop, Operation):
    """Divide el segundo elemento entre el tope de la pila."""

    def apply(self, stack, mem):
        b, a = self.pop(stack), self.pop(stack)
        if b == 0:
            raise RPNError("División por cero")
        stack.append(a / b)


# --- Operaciones de pila ---


class DupOp(_Pop, Operation):
    """Duplica el elemento en el tope de la pila."""

    def apply(self, stack, mem):
        if not stack:
            raise RPNError("Pila insuficiente")
        stack.append(stack[-1])


class SwapOp(Operation):
    """Intercambia los dos elementos superiores de la pila."""

    def apply(self, stack, mem):
        if len(stack) < 2:
            raise RPNError("Pila insuficiente")
        stack[-1], stack[-2] = stack[-2], stack[-1]


class DropOp(_Pop, Operation):
    """Descarta el elemento en el tope de la pila."""

    def apply(self, stack, mem):
        self.pop(stack)


class ClearOp(Operation):
    """Vacía completamente la pila."""

    def apply(self, stack, mem):
        stack.clear()


# --- Funciones matemáticas unarias ---


class UnaryOp(_Pop, Operation):
    """Operación unaria genérica: aplica una función al tope de la pila."""

    def __init__(self, func):
        """Inicializa con la función matemática a aplicar."""
        self._func = func

    def apply(self, stack, mem):
        """Aplica la función al tope de la pila y empuja el resultado."""
        stack.append(self._func(self.pop(stack)))


class InverseOp(_Pop, Operation):
    """Calcula el inverso multiplicativo 1/x del tope de la pila."""

    def apply(self, stack, mem):
        a = self.pop(stack)
        if a == 0:
            raise RPNError("División por cero")
        stack.append(1 / a)


class PowOp(_Pop, Operation):
    """Eleva el segundo elemento a la potencia del tope (a^b)."""

    def apply(self, stack, mem):
        b, a = self.pop(stack), self.pop(stack)
        stack.append(a**b)


# --- Funciones trigonométricas (entrada en grados) ---


class TrigOp(_Pop, Operation):
    """Función trigonométrica directa con entrada en grados."""

    def __init__(self, func):
        """Inicializa con la función trigonométrica (sin, cos, tan)."""
        self._func = func

    def apply(self, stack, mem):
        """Convierte grados a radianes y aplica la función trigonométrica."""
        stack.append(self._func(math.radians(self.pop(stack))))


class InvTrigOp(_Pop, Operation):
    """Función trigonométrica inversa con resultado en grados."""

    def __init__(self, func):
        """Inicializa con la función inversa (asin, acos, atan)."""
        self._func = func

    def apply(self, stack, mem):
        """Aplica la función inversa y convierte el resultado a grados."""
        stack.append(math.degrees(self._func(self.pop(stack))))


# --- Operaciones de memoria ---


class StoOp(_Pop, Operation):
    """Almacena el tope de la pila en un registro de memoria."""

    def __init__(self, idx):
        """Inicializa con el índice del registro destino (0–9)."""
        if not 0 <= idx <= 9:
            raise RPNError("Memoria inválida")
        self._idx = idx

    def apply(self, stack, mem):
        """Extrae el tope de la pila y lo guarda en mem[idx]."""
        mem[self._idx] = self.pop(stack)


class RclOp(Operation):
    """Recupera el valor de un registro de memoria y lo empuja a la pila."""

    def __init__(self, idx):
        """Inicializa con el índice del registro fuente (0–9)."""
        if not 0 <= idx <= 9:
            raise RPNError("Memoria inválida")
        self._idx = idx

    def apply(self, stack, mem):
        """Empuja el valor de mem[idx] al tope de la pila."""
        stack.append(mem[self._idx])


# ---------------------------------------------------------------------------
# Tabla de despacho: token → instancia de Operation
# ---------------------------------------------------------------------------

OPERATIONS = {
    # Constantes
    "p": ConstantOp(math.pi),
    "e": ConstantOp(math.e),
    "j": ConstantOp((1 + 5**0.5) / 2),
    # Aritmética
    "+": AddOp(),
    "-": SubOp(),
    "*": MulOp(),
    "/": DivOp(),
    # Pila
    "dup": DupOp(),
    "swap": SwapOp(),
    "drop": DropOp(),
    "clear": ClearOp(),
    # Funciones unarias
    "sqrt": UnaryOp(math.sqrt),
    "log": UnaryOp(math.log10),
    "ln": UnaryOp(math.log),
    "exp": UnaryOp(math.exp),
    "10x": UnaryOp(lambda x: 10**x),
    "yx": PowOp(),
    "1/x": InverseOp(),
    "chs": UnaryOp(lambda x: -x),
    # Trigonometría directa (entrada en grados)
    "sin": TrigOp(math.sin),
    "cos": TrigOp(math.cos),
    "tg": TrigOp(math.tan),
    # Trigonometría inversa (resultado en grados)
    "asin": InvTrigOp(math.asin),
    "acos": InvTrigOp(math.acos),
    "atg": InvTrigOp(math.atan),
}


def _resolve(tok, _):
    """
    Resuelve un token a su instancia de Operation correspondiente.

    Para tokens fijos busca en OPERATIONS; para sto/rcl construye
    la instancia con el índice extraído del token.
    """
    if tok in OPERATIONS:
        return OPERATIONS[tok]
    if tok.startswith("sto"):
        return StoOp(int(tok[3:]))
    if tok.startswith("rcl"):
        return RclOp(int(tok[3:]))
    raise RPNError(f"Token inválido: {tok}")


# ---------------------------------------------------------------------------
# Evaluador principal
# ---------------------------------------------------------------------------


def eval_rpn(tokens):
    """
    Evalúa una lista de tokens en notación polaca inversa (RPN).

    Parámetros
    ----------
    tokens : list[str]
        Lista de tokens que representan la expresión RPN.

    Retorna
    -------
    float
        Resultado de la evaluación.

    Lanza
    -----
    RPNError
        Si ocurre división por cero, token desconocido, pila insuficiente
        o la pila final no contiene exactamente un valor.
    """
    stack = []
    mem = [0.0] * 10

    for tok in tokens:
        # Intentar interpretar el token como número flotante
        try:
            stack.append(float(tok))
            continue
        except ValueError:
            pass

        # Resolver la operación y ejecutarla polimórficamente
        op = _resolve(tok.lower(), mem)
        op.apply(stack, mem)

    # La expresión RPN válida debe dejar exactamente un resultado en la pila
    if len(stack) != 1:
        raise RPNError("La pila final debe tener exactamente un valor")

    return stack[0]


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------


def main():
    """
    Punto de entrada principal.

    Lee la expresión RPN desde argumentos de línea de comandos o,
    si no se proporcionan, solicita al usuario que la ingrese.
    Imprime el resultado o un mensaje de error en stderr.
    """
    # Leer expresión desde argumentos o entrada interactiva
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
    else:
        expr = input("RPN> ")

    try:
        result = eval_rpn(expr.split())
        print(result)
    except RPNError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Análisis pylint
# ---------------------------------------------------------------------------
#
# Primera corrida (antes de correcciones):
#   rpn.py:17:4:  W0107  unnecessary-pass          → CORREGIDO
#   rpn.py:24:0:  R0903  too-few-public-methods     → ignorado (ver abajo)
#   rpn.py:32:0:  R0903  too-few-public-methods     → ignorado (ver abajo)
#   rpn.py:45:0:  R0903  too-few-public-methods     → ignorado (ver abajo)
#   rpn.py:104:0: R0903  too-few-public-methods     → ignorado (ver abajo)
#   rpn.py:120:0: R0903  too-few-public-methods     → ignorado (ver abajo)
#   rpn.py:201:0: R0903  too-few-public-methods     → ignorado (ver abajo)
#   rpn.py:254:18: W0613 unused-argument 'mem'      → CORREGIDO
#   Score: 9.36/10
#
# Correcciones aplicadas:
#   W0107 — Se eliminó el `pass` innecesario en RPNError; el docstring
#            ya actúa como cuerpo de la clase en Python.
#   W0613 — El argumento `mem` en _resolve() se renombró a `_` para
#            indicar explícitamente que es ignorado por diseño.
#
# Segunda corrida (luego de correcciones):
#   rpn.py:23:0:  R0903  too-few-public-methods  (Operation)
#   rpn.py:31:0:  R0903  too-few-public-methods  (_Pop)
#   rpn.py:44:0:  R0903  too-few-public-methods  (ConstantOp)
#   rpn.py:103:0: R0903  too-few-public-methods  (SwapOp)
#   rpn.py:119:0: R0903  too-few-public-methods  (ClearOp)
#   rpn.py:200:0: R0903  too-few-public-methods  (RclOp)
#   Score: 9.52/10  (+0.16)
#
# Advertencias R0903 no corregidas — justificación:
#   El código implementa el patrón Command: cada clase encapsula una única
#   operación RPN cuya interfaz pública es apply(). Tener exactamente un
#   método público no es un defecto sino la intención del patrón. Agregar
#   métodos extra solo para satisfacer la heurística de pylint violaría el
#   principio de responsabilidad única sin aportar valor funcional.
