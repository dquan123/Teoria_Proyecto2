"""
Proyecto No. 2 - Teoria de la Computacion
Modulo: simplificacion.py

Algoritmos de simplificacion de gramaticas (en el orden del ejemplo del profesor):
    Paso 2: eliminar producciones epsilon
    Paso 3: eliminar producciones unitarias   (pendiente)
    Paso 4: eliminar simbolos inutiles        (pendiente)
    Paso 5: convertir a Forma Normal de Chomsky (pendiente)
"""

from gramatica import Gramatica, EPSILON


#ELIMINAR PRODUCCIONES EPSILON

def encontrar_anulables(g, verbose=True):
    anulables = []
    cambio = True
    while cambio:
        cambio = False
        for cabeza in g.V:
            if cabeza in anulables:
                continue
            for cuerpo in g.P[cabeza]:
                # Un cuerpo "anula" a la cabeza si todos sus simbolos son
                # epsilon o ya son anulables.
                todos_anulables = True
                for simbolo in cuerpo:
                    if simbolo != EPSILON and simbolo not in anulables:
                        todos_anulables = False
                        break
                if todos_anulables:
                    anulables.append(cabeza)
                    cambio = True
                    if verbose:
                        print(f"    {cabeza} -> {' '.join(cuerpo)}  =>  {cabeza} es anulable")
                    break
    return anulables


def variantes_sin_anulables(cuerpo, anulables):
    """
    Dado un cuerpo, devuelve TODAS las formas de escribirlo eligiendo, para cada
    simbolo anulable, si esta presente o ausente. Si hay m simbolos anulables
    se generan 2^m formas (incluida la forma en la que todos estan ausentes).

    Se construye de izquierda a derecha: cada vez que aparece un anulable, cada
    forma parcial se duplica (una con el simbolo y otra sin el).
    """
    formas = [[]]                                  # empezamos con una forma vacia
    for simbolo in cuerpo:
        nuevas = []
        for forma in formas:
            nuevas.append(forma + [simbolo])       # simbolo presente
            if simbolo in anulables:
                nuevas.append(forma)               # simbolo ausente
        formas = nuevas
    return formas


def eliminar_epsilon(g, verbose=True):
    """
    Construye G1 sin producciones epsilon, tal que L(G1) = L(G) - {epsilon}.

    Paso 1: encontrar los anulables.
    Paso 2: por cada produccion A -> X1...Xk de G, agregar a G1 todas las formas
            con los anulables presentes o ausentes, EXCEPTO la forma vacia
            (eso seria A -> epsilon, que es justo lo que se quiere eliminar).
    """
    if verbose:
        print("  Paso 1 - Encontrando anulables:")
    anulables = encontrar_anulables(g, verbose)
    if verbose:
        print(f"    Anulables = {anulables}")
        print("  Paso 2 - Construyendo producciones de G1:")

    g1 = Gramatica()
    g1.S = g.S
    for cabeza in g.V:                             # se conservan todas las variables
        g1.agregar_variable(cabeza)

    for cabeza in g.V:
        for cuerpo in g.P[cabeza]:
            if cuerpo == [EPSILON]:
                if verbose:
                    print(f"    {cabeza} -> ε   se elimina")
                continue

            m = 0                                  # cantidad de simbolos anulables
            for simbolo in cuerpo:
                if simbolo in anulables:
                    m += 1

            for forma in variantes_sin_anulables(cuerpo, anulables):
                if len(forma) > 0:                 # la forma vacia no se agrega
                    g1.agregar(cabeza, forma)

            if verbose and m > 0:
                print(f"    {cabeza} -> {' '.join(cuerpo)}   m = {m}  =>  2^{m} = {2 ** m} formas")

    if verbose and g.S in anulables:
        print(f"    Nota: {g.S} es anulable, entonces epsilon estaba en L(G) y ya no estara en L(G1).")
    return g1