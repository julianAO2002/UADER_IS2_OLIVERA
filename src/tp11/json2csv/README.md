# json2csv

Herramienta de línea de comandos en Python que convierte documentos **JSON** a **CSV**, implementada con una **estrategia de filtro**: lee de un archivo o de la entrada estándar, transforma y escribe en un archivo o en la salida estándar.

- Versión: ver [`VERSION`](VERSION) — Build: ver [`BUILD`](BUILD) (`python json2csv.py --version`)
- Licencia: [MIT](LICENSE)
- Cambios: [`CHANGELOG.md`](CHANGELOG.md) — Prompts de IA: [`CONTEXT.md`](CONTEXT.md)
- Documentación: [`docs/USO.md`](docs/USO.md) y API generada con pdoc en [`docs/api/`](docs/api/index.html)

## Uso

```text
python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}
```

| Argumento | Descripción | Por defecto |
|-----------|-------------|-------------|
| `-i` | archivo JSON de entrada | entrada estándar |
| `-o` | archivo CSV de salida | salida estándar |
| `-d` | delimitador (un carácter, admite `\t`) | `,` |

```bash
python json2csv.py -i datos.json -o datos.csv
cat datos.json | python json2csv.py -d ";" > datos.csv
python -m json2csv < datos.json          # con PYTHONPATH=src
```

Códigos de salida: `0` éxito, `1` error de datos o E/S, `2` error de uso, `130` interrupción.

## Reglas de conversión

| Entrada JSON | Resultado CSV |
|--------------|---------------|
| arreglo de objetos | una fila por objeto; encabezado = unión de claves en orden de aparición |
| objeto único | una sola fila |
| objeto anidado `{"a": {"b": 1}}` | columna `a.b` |
| lista anidada `{"t": [1, 2]}` | celda con el texto JSON `[1, 2]` |
| arreglo de escalares | columna única `value` |
| `null` / `true` / `false` | vacío / `true` / `false` |
| arreglo vacío | salida vacía |

Errores controlados (mensaje `json2csv: error: ...` por stderr, sin traceback): archivo inexistente, directorio, permisos, codificación no UTF-8, JSON inválido (con línea y columna), raíz escalar, arreglos mixtos, delimitador inválido, salida igual a la entrada, falla de escritura, pipe roto e interrupción.

## Desarrollo

Todo el desarrollo se hace en un ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Controles de calidad (los mismos que ejecuta el workflow de CI):

```bash
ruff check .                                        # reglas de formato y lint
black --check .                                     # formato consistente
pycodestyle --max-line-length=120 --exclude=.venv . # PEP8
pydocstyle --convention=pep257 src json2csv.py      # PEP257
mypy                                                # tipos (strict)
pyright                                             # tipos (strict)
bandit -c pyproject.toml -r src json2csv.py         # seguridad
python -m pytest                                    # pruebas, cobertura >= 85%
pdoc -o docs/api ./src/json2csv ./src/json2csv/core.py ./src/json2csv/cli.py
```

## Estructura

Esqueleto generado con CookieCutter ([audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage)) y adaptado: sin dependencias de ejecución (solo biblioteca estándar), documentación con pdoc y workflow de CI/CD propio.

```text
json2csv/
├── json2csv.py          punto de entrada (python json2csv.py ...)
├── src/json2csv/
│   ├── __init__.py      versión y build
│   ├── __main__.py      python -m json2csv
│   ├── cli.py           filtro: argumentos, E/S y manejo de excepciones
│   └── core.py          conversión JSON -> CSV (pura, sin E/S)
├── tests/               pytest (hipótesis H1..H35)
├── docs/                USO.md + api/ (pdoc)
├── pyproject.toml       configuración de ruff, black, mypy, pyright, bandit, pytest
├── requirements.txt     dependencias del ambiente virtual
├── VERSION, BUILD       registro de versión y build
├── CHANGELOG.md, CONTEXT.md, LICENSE
```

## CI/CD

El workflow [`.github/workflows/tp11-json2csv.yml`](../../../.github/workflows/tp11-json2csv.yml) (en la raíz del repositorio) se dispara con cada PR y push a `main` que toque esta carpeta:

1. **CI**: venv + `requirements.txt`, ruff, black, pycodestyle, pydocstyle, mypy, pyright, bandit, pytest con cobertura mínima 85% y prueba de humo.
2. **CD**: tras un merge exitoso a `main` regenera la documentación con pdoc, la publica como artefacto (con `BUILD_INFO.txt`: versión, build y número de corrida) y, si la variable del repositorio `DOCS_PAGES` vale `true` (y Pages usa "GitHub Actions" como fuente), la despliega en GitHub Pages.

No se utiliza Trufflehog.
