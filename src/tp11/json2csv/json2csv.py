"""Punto de entrada: python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "src"))

from json2csv.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
