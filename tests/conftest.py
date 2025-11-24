import sys
import os
from pathlib import Path

# Caminho absoluto do diretório /src
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Garante que o pytest enxergue src
sys.path.insert(0, str(SRC))

print(">> PYTEST LOADING SRC FROM:", SRC)
