# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/); el proyecto usa [versionado semántico](https://semver.org/lang/es/).

## [1.0.0] - 2026-10-14 (build 1)

### Agregado

- Conversión JSON → CSV como filtro: `python json2csv.py {-i input} {-o output} {-d delimitador}`.
- Entrada por stdin y salida por stdout cuando no se indican `-i` / `-o`; coma como delimitador por defecto.
- Aplanado de objetos anidados (`a.b`), listas anidadas como JSON, arreglos de escalares en columna `value`.
- Manejo de excepciones: archivo inexistente, directorio, permisos, UTF-8 inválido, JSON inválido, raíz escalar, arreglos mixtos, delimitador inválido, salida igual a la entrada, errores de E/S, pipe roto y Ctrl+C.
- `--version` con VERSION y BUILD.
- Pruebas con pytest (cobertura ≥ 85%), ruff, black, pycodestyle, pydocstyle, mypy, pyright y bandit.
- Documentación con pdoc y workflow de CI/CD en GitHub Actions.
- Esqueleto inicial generado con CookieCutter (`audreyfeldroy/cookiecutter-pypackage`).
