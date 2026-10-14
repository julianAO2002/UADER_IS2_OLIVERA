# CONTEXT — uso de herramientas de IA

El proyecto se desarrolló con asistencia de **Claude Code** (modelo Claude Opus 5.5, Anthropic) dentro del repositorio del curso.

## Prompts utilizados

1. `resolve el tp11` — pedido inicial sobre el enunciado `IS2_TP11_Gestión de Calidad.pdf`, que incluye la consigna de json2csv:

   > Desarrolle una herramienta en lenguaje Python para convertir archivos de formato JSON a formato CSV. El programa deberá implementarse con una estrategia de filtro. El formato de ejecución será: `python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}` [...] Asegure la implementación de controles robustos para las condiciones de excepción [...] Implemente el proyecto en GitHub utilizando un marco para integración continua con las siguientes características: a. [...] u.

2. Respuestas a las preguntas del asistente:
   - Ubicación del proyecto: *"Subcarpeta src/tp11"* (dentro del repositorio del curso, con el workflow en `.github/workflows/`).
   - Formato de las respuestas teóricas: *"README.md"*.
3. `hace un pdf tambien con las respuestas teoricas`

## Qué hizo la IA

- Generó el esqueleto con `cookiecutter gh:audreyfeldroy/cookiecutter-pypackage` (configuración de GitHub del template omitida) y lo adaptó.
- Escribió `core.py`, `cli.py`, las pruebas y la configuración de las herramientas de calidad.
- Corrió localmente ruff, black, pycodestyle, pydocstyle, mypy, pyright, bandit y pytest hasta dejarlos sin errores.
- Redactó README, CHANGELOG, USO.md y el workflow de CI/CD.

## Revisión humana

El código y la documentación generados deben ser revisados por el autor antes de su entrega; el push y los PR a GitHub los realiza el autor.
