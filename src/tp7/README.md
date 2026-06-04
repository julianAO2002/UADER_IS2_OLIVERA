# TP7 - Refactorización con Patrones de Diseño

## Descripción

Refactorización del programa `getJason.py` original (obtenido por ingeniería inversa en TP6) aplicando patrones de diseño y la estrategia **Branching by Abstraction** para gestionar la convergencia entre la versión original y la refactorizada.

## Patrones aplicados

### Singleton
Garantiza que la clase `getJason` tenga una única instancia durante toda la ejecución. Se implementa sobreescribiendo `__new__` para devolver siempre la misma instancia ya creada.

### Chain of Responsibility
Reemplaza los condicionales de validación de argumentos por una cadena de validadores, donde cada eslabón maneja su caso y delega al siguiente. Facilita agregar o quitar validaciones sin modificar el resto.

Validadores en orden:
1. `ArgCountValidator` — verifica que haya al menos un argumento
2. `VersionValidator` — si el argumento es `-v`, muestra la versión y termina
3. `ExtraArgsValidator` — verifica que no haya argumentos de más
4. `ExtensionValidator` — verifica que el archivo tenga extensión `.json`
5. `FileExistsValidator` — verifica que el archivo exista en el sistema

### Branching by Abstraction
Estrategia para reemplazar una implementación por otra de forma gradual sin romper el código existente. Ambas versiones conviven bajo una abstracción común (`BaseJasonReader`) y se alterna entre ellas con un flag.

## Estructura

```
tp7/
├── base_reader.py       # Abstracción base (BaseJasonReader)
├── getJasonOriginal.py  # Implementación original sin patrones
├── getJason.py          # Implementación refactorizada (Singleton + Chain of Responsibility)
├── main.py              # Punto de entrada con switch entre implementaciones
└── sitedata.json        # Archivo de datos de ejemplo
```

## Uso

```bash
# Ejecutar con la implementación activa
python main.py sitedata.json

# Ver versión
python main.py -v
```

Para alternar entre la versión original y la refactorizada, modificar el flag en `main.py`:

```python
USE_REFACTORED = True   # usa getJason (Singleton + Chain)
USE_REFACTORED = False  # usa getJasonOriginal (versión original)
```

## Análisis estático con pylint (ítem h)

Se ejecutó `pylint getJason.py` y se corrigieron todas las observaciones hasta alcanzar **10.00/10**.

### Observaciones iniciales (5.34/10)

| Código | Descripción | Solución aplicada |
| ------ | ----------- | ----------------- |
| `C0114` | Falta docstring de módulo | Se agregó docstring al inicio del archivo |
| `C0103` | Nombre de módulo no sigue snake_case (`getJason`) | Se suprimió con `pylint: disable=invalid-name` — el nombre es parte del contrato del TP |
| `C0115` | Falta docstring en clases (`Validator` y subclases, `GetJason`) | Se agregó docstring a todas las clases |
| `C0116` | Falta docstring en métodos (`validate`, `getJason`) | Se agregó docstring a todos los métodos públicos |
| `R0903` | Pocas métodos públicos (< 2) en clases validadoras | Se suprimió con `pylint: disable=too-few-public-methods` — los nodos de Chain of Responsibility tienen un único método `validate` por diseño; agregar métodos ficticios sería mala práctica |
| `W1514` | `open()` sin especificar encoding | Se agregó `encoding='utf-8'` al llamado `open()` |
| `E1101` | `GetJason` sin atributos `jsonfile`/`jsonkey` como miembros de instancia | Los atributos se renombraron con prefijo `_` y se declararon como atributos de clase (`_jsonfile = None`, `_jsonkey = None`) para que pylint los reconozca |

### Resultado final

```text
Your code has been rated at 10.00/10
```

## Autor

Julian Olivera
