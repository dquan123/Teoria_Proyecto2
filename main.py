"""
Proyecto No. 2 - Teoria de la Computacion
main.py

Flujo del programa:
    1. Lee la gramatica desde un archivo.
    2. La simplifica y la convierte a Forma Normal de Chomsky (CNF):
           eliminar epsilon -> eliminar unitarias -> eliminar inutiles -> CNF
    3. Pide una frase y aplica el algoritmo CYK.
    4. Muestra SI/NO, el tiempo que tardo CYK y, si la frase pertenece al
       lenguaje, su parse tree.                                          
"""

import sys
import time
from pathlib import Path

from gramatica import cargar_gramatica
from simplificacion import eliminar_epsilon, eliminar_unitarias, eliminar_inutiles
from simplificacion import convertir_a_cnf, esta_en_cnf
from cyk import cyk, mostrar_tabla
from arbol import construir_arbol, mostrar_arbol, dibujar_arbol

# Carpeta donde vive este script (para encontrar la gramatica sin importar desde
# donde se ejecute el programa)
CARPETA_SCRIPT = Path(__file__).resolve().parent
GRAMATICA_POR_DEFECTO = CARPETA_SCRIPT / "gramaticas" / "ingles.txt"


def simplificar_a_cnf(g, detalle):
    """
    Aplica en orden los 4 algoritmos de simplificacion y devuelve la gramatica en CNF.
    Si detalle es True, muestra cada paso y la gramatica que va quedando.
    """
    if detalle:
        print("\n=== Eliminando producciones epsilon ===")
    g1 = eliminar_epsilon(g, detalle)
    if detalle:
        g1.mostrar("Gramatica sin producciones epsilon:")

    if detalle:
        print("\n=== Eliminando producciones unitarias ===")
    g2 = eliminar_unitarias(g1, detalle)
    if detalle:
        g2.mostrar("Gramatica sin producciones unitarias:")

    if detalle:
        print("\n=== Eliminando simbolos inutiles ===")
    g3 = eliminar_inutiles(g2, detalle)
    if detalle:
        g3.mostrar("Gramatica sin simbolos inutiles:")

    if detalle:
        print("\n=== Convirtiendo a Forma Normal de Chomsky ===")
    return convertir_a_cnf(g3, detalle)


def main():
    detalle = "--pasos" in sys.argv
    argumentos = [a for a in sys.argv[1:] if a != "--pasos"]
    ruta = argumentos[0] if argumentos else GRAMATICA_POR_DEFECTO

    # ---- 1 y 2: leer la gramatica y convertirla a CNF ----
    g = cargar_gramatica(ruta)
    print(f"Gramatica: {ruta}")
    g.mostrar("Gramatica original:")

    g4 = simplificar_a_cnf(g, detalle)
    print()
    g4.mostrar("Gramatica en CNF:")
    if esta_en_cnf(g4):
        print("  Verificacion: toda produccion es A -> B C  o  A -> a   (esta en CNF)")
    else:
        print("  Verificacion: ERROR, la gramatica NO quedo en CNF")

    # ---- 3 y 4: CYK sobre las frases que se ingresen ----
    terminales = g4.terminales()
    print("\n=== Algoritmo CYK ===")
    while True:
        try:
            frase = input("\nIngrese una frase (Enter vacio para salir): ")
        except EOFError:
            break
        if frase.strip() == "":
            break

        for signo in ".,;:!?":                       # ignora signos de puntuacion
            frase = frase.replace(signo, " ")
        palabras = frase.lower().split()             # no distingue mayusculas

        for palabra in palabras:
            if palabra not in terminales:
                print(f"  Aviso: la palabra \"{palabra}\" no esta en el vocabulario de la gramatica")

        # Se mide SOLO el algoritmo CYK (sin imprimir nada dentro del cronometro)
        inicio = time.perf_counter()
        acepta, tabla = cyk(g4, palabras, False)
        fin = time.perf_counter()

        if detalle:
            mostrar_tabla(palabras, tabla)

        if acepta:
            print("  Resultado: SÍ, la frase pertenece al lenguaje")
        else:
            print("  Resultado: NO, la frase no pertenece al lenguaje")
        print(f"  Tiempo del algoritmo CYK: {(fin - inicio) * 1000:.4f} ms")

        if acepta:
            print("\n  Parse tree:")
            raiz = construir_arbol(tabla, g4.S, len(palabras), 0)
            mostrar_arbol(raiz)
            dibujar_arbol(raiz)


main()