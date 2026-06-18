# TP8 - Ingeniería Reversa, Re-factoría y Re-Ingeniería

## Descripción

Re-ingeniería del proceso de pagos sobre el programa `getJason.py` (continuación del TP7).

En la versión anterior un **empleado decidía manualmente** sobre qué banco liberar un pago y elegía el token respectivo. En esta versión el proceso de decisión se **automatiza**: basta con que exista saldo en la cuenta y los pagos se distribuyen de forma **balanceada** (alternada) entre las cuentas disponibles.

El objeto *singleton* que, dado un nombre de token (banco), devuelve la clave (leída de `sitedata.json`) se integra a un nuevo componente que, ante una solicitud de pago, selecciona automáticamente la cuenta desde la que se realiza.

## Reglas de negocio

- Dos cuentas, controladas mediante el patrón **cadena de comando**:
  - `token1` con saldo inicial de **$1000**
  - `token2` con saldo inicial de **$2000**
- Pedidos de pago de **$500** (número de pedido, monto) ruteados **alternativamente** a cada cuenta que tenga saldo suficiente.
- Salida por pedido: número de pedido, token utilizado y monto pagado.
- Función de **listado** que muestra todos los pagos realizados por orden cronológico (patrón **iterator**).
- Versión avanzada a **1.2**.

## Patrón de arquitectura: Layered Architecture (capas)

El sistema se organiza en **paquetes por capa**, con dependencias en una sola dirección y sin ciclos:

```text
main → presentation / business → domain / data → config
```

```text
tp8/
├── main.py                      # Punto de entrada (orquesta el flujo)
├── sitedata.json                # Relación token (banco) → clave
├── config/                      # Configuración
│   └── version.py               #   VERSION = "1.2.0", SALDOS_INICIALES
├── presentation/                # Presentación / entrada
│   └── validators.py            #   Chain of Responsibility (validación de args)
├── business/                    # Lógica de negocio
│   ├── payment_processor.py     #   Orquesta el ruteo balanceado de pagos
│   └── account_handler.py       #   Chain of Command (control de cuentas)
├── domain/                      # Modelo de dominio
│   ├── payment.py               #   Entidad Payment
│   └── payment_log.py           #   Iterator (registro cronológico)
└── data/                        # Acceso a datos
    ├── base_reader.py           #   Abstracción del lector (BaseJasonReader)
    └── getJason.py              #   Singleton (token → clave)
```

## Patrones de diseño aplicados

### Singleton — `data/getJason.py`

`GetJason` garantiza una única instancia. Dado un nombre de token (banco) devuelve la clave asociada almacenada en `sitedata.json` (método `get_key`).

### Chain of Command — `business/account_handler.py`

`AccountHandler` modela cada cuenta como un eslabón de una cadena. Si la cuenta tiene saldo suficiente atiende el pago; en caso contrario delega la solicitud al siguiente eslabón. `PaymentProcessor` reconstruye la cadena en cada pedido empezando por la cuenta que corresponde según el ruteo alternado, logrando el balanceo.

### Iterator — `domain/payment_log.py`

`PaymentLog` es una colección iterable de pagos y `PaymentIterator` la recorre en orden cronológico. La función `list_payments()` del procesador usa este iterador para el listado.

### Chain of Responsibility — `presentation/validators.py`

La validación de argumentos de línea de comandos se resuelve con una cadena de validadores (heredado y adaptado del TP7):

1. `ArgCountValidator` — verifica que haya al menos un argumento
2. `VersionValidator` — si el argumento es `-v`, muestra la versión y termina
3. `ExtraArgsValidator` — verifica que no haya argumentos de más
4. `ExtensionValidator` — verifica que el archivo tenga extensión `.json`
5. `FileExistsValidator` — verifica que el archivo exista en el sistema

## Uso

```bash
# Ejecutar la demostración de pagos automáticos
python main.py sitedata.json

# Ver versión
python main.py -v
```

### Salida de ejemplo

```text
Pedido #1: pago de $500 realizado desde 'token1'.
Pedido #2: pago de $500 realizado desde 'token2'.
Pedido #3: pago de $500 realizado desde 'token1'.
Pedido #4: pago de $500 realizado desde 'token2'.
Pedido #5: pago de $500 realizado desde 'token2'.
Pedido #6: pago de $500 realizado desde 'token2'.

Pagos realizados (orden cronologico):
  Pedido #1 | token=token1 | monto=$500 | clave=C598-ECF9-F0F7-881A
  Pedido #2 | token=token2 | monto=$500 | clave=C598-ECF9-F0F7-881B
  Pedido #3 | token=token1 | monto=$500 | clave=C598-ECF9-F0F7-881A
  Pedido #4 | token=token2 | monto=$500 | clave=C598-ECF9-F0F7-881B
  Pedido #5 | token=token2 | monto=$500 | clave=C598-ECF9-F0F7-881B
  Pedido #6 | token=token2 | monto=$500 | clave=C598-ECF9-F0F7-881B

Saldos finales: {'token1': 0, 'token2': 0}
```

> Los primeros 4 pedidos alternan entre cuentas (ruteo balanceado). Al agotarse el saldo de `token1` tras el pedido #4, la cadena delega los pedidos #5 y #6 en `token2`, que aún tiene saldo. Total: 6 × $500 = $3000 = saldo combinado inicial.

## Análisis estático con pylint (ítem h)

Se ejecutó pylint sobre toda la estructura de paquetes:

```bash
python -m pylint main.py config presentation business domain data
```

Resultado: **10.00/10** (el enunciado requiere 8 o superior).

```text
Your code has been rated at 10.00/10
```

### Supresiones justificadas

| Código | Dónde | Justificación |
| ------ | ----- | ------------- |
| `invalid-name` | `getJason.py` (módulo) y `getJason` (método) | El nombre es parte del contrato del TP; no puede renombrarse |
| `too-few-public-methods` | Validadores, `Payment`, `BaseJasonReader` | Nodos de cadena / entidades de datos con un único método por diseño |

## Autor

Julian Olivera
