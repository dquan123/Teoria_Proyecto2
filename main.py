"""
Proyecto No. 2 - Teoria de la Computacion
main.py (version del Paso 2: lee la gramatica y elimina producciones epsilon)

Uso:
    python main.py gramaticas/1.txt
"""

import sys
from gramatica import cargar_gramatica
from simplificacion import eliminar_epsilon


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_gramatica>")
        sys.exit(1)

    g = cargar_gramatica(sys.argv[1])
    g.mostrar("Gramatica leida:")
    print(f"  V (no terminales) = {g.V}")
    print(f"  T (terminales)    = {g.terminales()}")
    print(f"  S (inicial)       = {g.S}")

    print("\n=== Eliminando producciones epsilon ===")
    g1 = eliminar_epsilon(g)
    g1.mostrar("Gramatica sin producciones epsilon:")


main()