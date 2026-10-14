# json2csv — funcionamiento de los módulos

## Flujo (estrategia de filtro)

```text
 archivo -i  ─┐                                         ┌─► archivo -o
              ├─► cli._leer ─► core.convertir ─► cli._escribir
 stdin       ─┘        (texto)      (texto CSV)         └─► stdout
```

`cli.main` sólo coordina: analiza argumentos, lee, delega la conversión y escribe. Toda condición de excepción se captura en `cli.main` y se traduce en un mensaje por stderr y un código de salida; nunca se muestra un traceback.

## `json2csv.core`

| Función | Responsabilidad |
|---------|-----------------|
| `validar_delimitador(d)` | acepta un único carácter (o `\t`); rechaza vacío, múltiple, `"` y saltos de línea |
| `registros_desde_json(texto)` | decodifica el JSON, normaliza la raíz a lista, aplana objetos y arma el encabezado |
| `convertir(texto, d)` | produce el texto CSV con `csv.DictWriter` (comillas automáticas) |
| `ConversionError` | única excepción de dominio: datos o parámetros inválidos |

## `json2csv.cli`

| Elemento | Responsabilidad |
|----------|-----------------|
| `crear_parser()` | define `-i`, `-o`, `-d` y `--version` |
| `main(argv, stdin, stdout, stderr)` | ejecuta el filtro y devuelve el código de salida; los flujos son inyectables para las pruebas |

| Código | Significado |
|--------|-------------|
| 0 | conversión exitosa |
| 1 | error de datos o de entrada/salida |
| 2 | error de uso (argumentos) |
| 130 | interrumpido por el usuario (Ctrl+C) |

## Ejemplo

Entrada:

```json
[{"id": 1, "cliente": {"nombre": "Ana"}, "tags": ["vip"]},
 {"id": 2, "cliente": {"nombre": "Luis"}, "activo": false}]
```

`python json2csv.py -d ";"`:

```text
id;cliente.nombre;tags;activo
1;Ana;"[""vip""]";
2;Luis;;false
```
