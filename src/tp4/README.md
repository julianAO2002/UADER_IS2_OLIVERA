# TP4 - Patrones de Diseño Estructurales

## Ejercicio 1 - Proxy (`ej1.py`)

`Ping` realiza 10 intentos de ping a una IP. `execute()` solo acepta IPs que comiencen con `"192."`, mientras que `executefree()` no tiene restricción. `PingProxy` intercepta las llamadas: si la IP es `"192.168.0.254"` redirige el ping a `www.google.com` usando `executefree()`; en cualquier otro caso delega a `execute()` de `Ping`.

## Ejercicio 2 - Bridge (`ej2.py`)

`LaminaAcero` representa una lámina genérica de acero. La implementación del laminado se delega a una jerarquía separada (`TrenLaminador5m` / `TrenLaminador10m`). El bridge desacopla la abstracción (lámina) de la implementación (tren), permitiendo combinarlas libremente sin herencia múltiple.

## Ejercicio 3 - Composite (`ej3.py`)

`Pieza` y `Conjunto` comparten la interfaz `Componente`. Un `Conjunto` puede contener tanto `Pieza`s como otros `Conjunto`s, formando una jerarquía árbol. El producto principal tiene tres subconjuntos de cuatro piezas cada uno; se puede agregar un subconjunto opcional sin modificar el código existente.

## Ejercicio 4 - Decorator (`ej4.py`)

`Numero` es la clase base que guarda un valor. Cada decorador (`SumarDos`, `MultiplicarPorDos`, `DividirPorTres`) envuelve a un `Numero` y sobreescribe `obtener()` aplicando su operación sobre el resultado del decorado. Se pueden anidar en cualquier orden: `DividirPorTres(MultiplicarPorDos(SumarDos(base)))`.

## Ejercicio 5 - Flyweight (`ej5.py`)

Escenario: editor de texto con miles de caracteres. El estilo (fuente, tamaño, color) es estado intrínseco compartido; la posición (x, y) es estado extrínseco único por caracter. `FabricaEstilos` garantiza que cada combinación de estilo se instancia una sola vez, reduciendo drásticamente el uso de memoria.

---

## Ejecución

```bash
cd src/tp4
python ej1.py
python ej2.py
python ej3.py
python ej4.py
python ej5.py
```
