"""
Proyecto No. 2 - Teoria de la Computacion
main.py (version del Paso 1: solo lee y muestra la gramatica)

Uso:
    python main.py gramaticas/1.txt
"""

import sys
from gramatica import cargar_gramatica


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_gramatica>")
        sys.exit(1)

    g = cargar_gramatica(sys.argv[1])
    g.mostrar("Gramatica leida:")
    print(f"  V (no terminales) = {g.V}")
    print(f"  T (terminales)    = {g.terminales()}")
    print(f"  S (inicial)       = {g.S}")


main()