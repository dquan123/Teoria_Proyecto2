# Proyecto No. 2 — Teoría de la Computación

Conversión de una gramática a Forma Normal de Chomsky (CNF) y algoritmo CYK para determinar si una frase pertenece al lenguaje de la gramática, con construcción del parse tree.

## Integrantes
- [Diego Quan] — [24336]
- [Alejandro Pérez] — [24136]

## Presentación (Video)
https://youtu.be/uwzrs03aaTU

## Descripción

El programa lee una gramática independiente del contexto desde un archivo, la simplifica y la convierte a CNF. Luego pide una frase y aplica el algoritmo CYK. Por cada frase muestra:

1. **SÍ / NO**: si la frase pertenece al lenguaje de la gramática.
2. **Tiempo** que tardó el algoritmo CYK.
3. **Parse tree** de la frase (en texto y como imagen `parse_tree.png`).

La simplificación se hace en este orden: eliminar producciones ε, eliminar producciones unitarias, eliminar símbolos inútiles y convertir a CNF.

## Estructura del repositorio

```
.
├── README.md
├── main.py              programa principal
├── gramatica.py         representación de la gramática y lectura del archivo
├── simplificacion.py    ε, unitarias, inútiles y CNF
├── cyk.py               algoritmo CYK
├── arbol.py             construcción y dibujo del parse tree
└── gramaticas/
    ├── ingles.txt       gramática del enunciado (se usa por defecto)
    ├── 1.txt            expresiones aritméticas, no está en CNF
    └── 1-cnf.txt        la misma gramática ya en CNF (referencia)
```

## Requisitos

- Python 3.
- Opcional, solo para la imagen del árbol:
  - paquete de Python: `python -m pip install graphviz`
  - programa Graphviz instalado en el sistema (en Windows: `winget install graphviz`, o el instalador de [graphviz.org](https://graphviz.org/download/) marcando "Add Graphviz to the system PATH").

  Sin Graphviz el programa funciona igual y muestra el árbol en texto.

## Cómo ejecutar

Desde la carpeta del proyecto:

```
python main.py                                  # usa gramaticas/ingles.txt
python main.py gramaticas/1.txt                 # usa otra gramática
python main.py gramaticas/ingles.txt --pasos    # muestra además cada paso de la simplificación y la tabla CYK
```

El programa pide una frase y vuelve a pedir otra hasta que se presione Enter vacío. No distingue mayúsculas e ignora signos de puntuación. Con `1.txt` las palabras de la frase se separan con espacios: `( id * id ) + id`.

## Formato del archivo de gramática

- Una producción por línea: `A -> alfa | beta`, con los símbolos separados por espacios.
- La letra `e` sola representa la cadena vacía (ε).
- El símbolo inicial es la cabeza de la primera línea.
- Todo símbolo que tiene producciones propias es una variable; el que no tiene, es un terminal.

Ejemplo (`gramaticas/1.txt`):
```
E -> T X
X -> + T X | e
T -> F Y
Y -> * F Y | e
F -> ( E ) | id
```

## Ejemplo de ejecución

Con `python main.py` y la frase `She eats a cake with a fork`:

```
=== Algoritmo CYK ===

Ingrese una frase (Enter vacio para salir): She eats a cake with a fork
  Resultado: SÍ, la frase pertenece al lenguaje
  Tiempo del algoritmo CYK: 0.1441 ms

  Parse tree:
  S
  |-- NP
  |   `-- she
  `-- VP
      |-- VP
      |   |-- V
      |   |   `-- eats
      |   `-- NP
      |       |-- Det
      |       |   `-- a
      |       `-- N
      |           `-- cake
      `-- PP
          |-- P
          |   `-- with
          `-- NP
              |-- Det
              |   `-- a
              `-- N
                  `-- fork
  Imagen del parse tree: parse_tree.png
```

Con una frase que no pertenece al lenguaje, por ejemplo `the cat eats the dragon`, el programa avisa de las palabras que no están en la gramática, responde NO y no genera árbol.

## Algoritmos implementados

| Algoritmo | Función | Archivo |
|---|---|---|
| Lectura de la gramática | `cargar_gramatica` | `gramatica.py` |
| Eliminar producciones ε | `eliminar_epsilon` | `simplificacion.py` |
| Eliminar producciones unitarias | `eliminar_unitarias` | `simplificacion.py` |
| Eliminar símbolos inútiles | `eliminar_inutiles` | `simplificacion.py` |
| Convertir a CNF | `convertir_a_cnf` | `simplificacion.py` |
| CYK | `cyk` | `cyk.py` |
| Parse tree | `construir_arbol` | `arbol.py` |
