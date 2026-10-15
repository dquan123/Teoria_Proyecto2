"""
Proyecto No. 2 - Teoria de la Computacion
main.py (version del Paso 2: lee la gramatica y elimina producciones epsilon)

Uso:
    python main.py gramaticas/1.txt
"""

import sys
from gramatica import cargar_gramatica
from simplificacion import eliminar_epsilon, eliminar_unitarias, eliminar_inutiles
from simplificacion import convertir_a_cnf, esta_en_cnf

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
    
    print("\n=== Eliminando producciones unitarias ===")
    g2 = eliminar_unitarias(g1)
    g2.mostrar("Gramatica sin producciones unitarias:")
    
    print("\n=== Eliminando simbolos inutiles ===")
    g3 = eliminar_inutiles(g2)
    g3.mostrar("Gramatica sin simbolos inutiles:")
    
    print("\n=== Convirtiendo a Forma Normal de Chomsky ===")
    g4 = convertir_a_cnf(g3)
    g4.mostrar("Gramatica en CNF:")
    if esta_en_cnf(g4):
        print("  Verificacion: toda produccion es A -> B C  o  A -> a   (esta en CNF)")
    else:
        print("  Verificacion: ERROR, la gramatica NO quedo en CNF")


main()