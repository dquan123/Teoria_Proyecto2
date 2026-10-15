"""
Proyecto No. 2 - Teoria de la Computacion
Modulo: gramatica.py

Representacion de una CFG G = (V, T, P, S) y lectura desde archivo.

Formato del archivo de gramatica (el mismo de 1.txt y 1-cnf.txt):
    - Una produccion por linea:  A -> alfa | beta | gamma
    - Los simbolos del cuerpo se separan con espacios.
    - La letra "e" sola (o "ε") representa la cadena vacia (epsilon).
    - El simbolo inicial S es la cabeza de la primera linea del archivo.
    - Todo simbolo que tiene produccion propia es un NO TERMINAL (variable);
      todo simbolo que no tiene produccion propia es un TERMINAL.
"""

import sys

# Simbolo interno para la cadena vacia
EPSILON = 'ε'


class Gramatica:
    """
    G = (V, T, P, S)  (misma notacion que en el ejemplo del profesor)

    V : lista de no terminales (en el orden en que aparecen en el archivo)
    P : diccionario  cabeza -> lista de cuerpos
        Cada cuerpo es una lista de simbolos, por ejemplo ['+', 'T', 'X'].
        El cuerpo de epsilon es la lista [EPSILON].
    S : simbolo inicial
    T : se calcula a partir de P (ver metodo terminales)
    """

    def __init__(self):
        self.S = None
        self.V = []
        self.P = {}

    def agregar(self, cabeza, cuerpo):
        """Agrega la produccion cabeza -> cuerpo (sin repetir cuerpos)."""
        if cabeza not in self.P:
            self.V.append(cabeza)
            self.P[cabeza] = []
        if cuerpo not in self.P[cabeza]:
            self.P[cabeza].append(cuerpo)

    def terminales(self):
        """T = simbolos de los cuerpos que no tienen produccion propia."""
        T = []
        for cabeza in self.V:
            for cuerpo in self.P[cabeza]:
                for simbolo in cuerpo:
                    if simbolo != EPSILON and simbolo not in self.P and simbolo not in T:
                        T.append(simbolo)
        return T

    def mostrar(self, titulo=None):
        """Imprime la gramatica: una linea por no terminal."""
        if titulo:
            print(titulo)
        for cabeza in self.V:
            cuerpos = [' '.join(cuerpo) for cuerpo in self.P[cabeza]]
            print(f"  {cabeza} -> {' | '.join(cuerpos)}")


def cargar_gramatica(ruta):
    """
    Lee el archivo de gramatica y devuelve un objeto Gramatica.
    Si una linea no cumple el formato, informa cual es y termina el programa.
    """
    g = Gramatica()
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f"Error: no se encontro el archivo '{ruta}'")
        sys.exit(1)

    for numero, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if linea == '':
            continue                                   # lineas en blanco se ignoran

        if '->' not in linea:
            print(f"Error en linea {numero}: falta '->' en \"{linea}\"")
            sys.exit(1)

        cabeza, resto = linea.split('->', 1)
        cabeza = cabeza.strip()
        if cabeza == '' or ' ' in cabeza:
            print(f"Error en linea {numero}: la cabeza debe ser un solo simbolo")
            sys.exit(1)

        for alternativa in resto.split('|'):
            simbolos = alternativa.split()
            if len(simbolos) == 0:
                print(f"Error en linea {numero}: hay una alternativa vacia")
                sys.exit(1)
            if simbolos == ['e'] or simbolos == [EPSILON]:
                simbolos = [EPSILON]                   # "e" significa epsilon
            g.agregar(cabeza, simbolos)

        if g.S is None:
            g.S = cabeza                               # la primera cabeza es el inicial

    if g.S is None:
        print("Error: el archivo no contiene ninguna produccion")
        sys.exit(1)
    return g