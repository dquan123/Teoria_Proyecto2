"""
Proyecto No. 2 - Teoria de la Computacion
Modulo: arbol.py

Construccion y despliegue del parse tree a partir de la tabla de CYK.
"""


class Nodo:
    """Un nodo del arbol: una etiqueta (variable o palabra) y sus hijos."""

    def __init__(self, etiqueta, hijos=None):
        self.etiqueta = etiqueta
        self.hijos = hijos if hijos is not None else []


def construir_arbol(tabla, A, l, i):
    """
    Construye el arbol de la variable A que deriva las l palabras desde la posicion i.
    Se apoya en lo que CYK guardo en la tabla:
        - si l == 1:  A -> palabra            (hoja)
        - si l >= 2:  A -> B C con corte en k (dos hijos, cada uno se construye igual)
    """
    como = tabla[(l, i)][A]
    if l == 1:
        return Nodo(A, [Nodo(como)])                         # A -> palabra
    k, B, C = como
    izquierdo = construir_arbol(tabla, B, k, i)              # las primeras k palabras
    derecho = construir_arbol(tabla, C, l - k, i + k)        # las l-k palabras restantes
    return Nodo(A, [izquierdo, derecho])


def mostrar_arbol(nodo, prefijo="", es_ultimo=True, es_raiz=True):
    """Imprime el arbol en texto, con sangria."""
    if es_raiz:
        print("  " + nodo.etiqueta)
        extension = "  "
    else:
        print("  " + prefijo + ("`-- " if es_ultimo else "|-- ") + nodo.etiqueta)
        extension = prefijo + ("    " if es_ultimo else "|   ")
    for numero, hijo in enumerate(nodo.hijos):
        ultimo = (numero == len(nodo.hijos) - 1)
        mostrar_arbol(hijo, extension if not es_raiz else "", ultimo, False)


def dibujar_arbol(raiz, nombre_archivo="parse_tree"):
    """
    Dibuja el arbol con Graphviz (el mismo paquete del Proyecto 1) y lo guarda
    como imagen PNG. Si Graphviz no esta instalado, solo avisa.
    """
    try:
        from graphviz import Digraph
        dot = Digraph(format="png")
        dot.node("0", raiz.etiqueta)
        pendientes = [(raiz, "0")]
        siguiente_id = 1
        while pendientes:
            nodo, id_nodo = pendientes.pop()
            for hijo in nodo.hijos:
                id_hijo = str(siguiente_id)
                siguiente_id += 1
                if len(hijo.hijos) == 0:
                    dot.node(id_hijo, hijo.etiqueta, shape="plaintext")   # palabra
                else:
                    dot.node(id_hijo, hijo.etiqueta)                      # variable
                dot.edge(id_nodo, id_hijo)
                pendientes.append((hijo, id_hijo))
        dot.render(nombre_archivo, cleanup=True)
        print(f"  Imagen del parse tree: {nombre_archivo}.png")
    except Exception as error:
        print(f"  (No se pudo generar la imagen del parse tree: {error})")