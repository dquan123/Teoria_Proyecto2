"""
Proyecto No. 2 - Teoria de la Computacion
Modulo: cyk.py

Algoritmo CYK (Cocke-Younger-Kasami) para decidir si una frase pertenece al
lenguaje de una gramatica que YA esta en Forma Normal de Chomsky.
"""


def cyk(g, palabras, verbose=True):
    """
    g        : Gramatica en CNF
    palabras : lista de palabras (la frase ya separada)
    Devuelve (acepta, tabla).
    """
    n = len(palabras)
    if n == 0:
        return False, {}

    tabla = {}

    # ---- BASE: subcadenas de longitud 1 ----
    for i in range(n):
        celda = {}
        for A in g.V:
            for cuerpo in g.P[A]:
                if len(cuerpo) == 1 and cuerpo[0] == palabras[i]:
                    if A not in celda:
                        celda[A] = palabras[i]               # A -> palabra
        tabla[(1, i)] = celda

    # ---- INDUCCION: subcadenas de longitud 2, 3, ..., n ----
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            celda = {}
            for k in range(1, l):                            # corte: k palabras a la izquierda
                izquierda = tabla[(k, i)]                    # w[i] ... w[i+k-1]
                derecha = tabla[(l - k, i + k)]              # w[i+k] ... w[i+l-1]
                for A in g.V:
                    for cuerpo in g.P[A]:
                        if len(cuerpo) == 2 and cuerpo[0] in izquierda and cuerpo[1] in derecha:
                            if A not in celda:
                                celda[A] = (k, cuerpo[0], cuerpo[1])   # A -> B C, corte en k
            tabla[(l, i)] = celda

    acepta = g.S in tabla[(n, 0)]

    if verbose:
        mostrar_tabla(palabras, tabla)
    return acepta, tabla


def mostrar_tabla(palabras, tabla):
    """Imprime la tabla de CYK, de las subcadenas mas cortas a las mas largas."""
    n = len(palabras)
    print("  Tabla CYK (celda (l, i) = variables que derivan las l palabras desde la posicion i):")
    for l in range(1, n + 1):
        for i in range(n - l + 1):
            subcadena = ' '.join(palabras[i:i + l])
            variables = ', '.join(tabla[(l, i)])
            print(f"    ({l},{i})  \"{subcadena}\"  ->  {{{variables}}}")