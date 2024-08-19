
from sympy.combinatorics import Permutation

import timeit
import numpy as np

# Función para aplicar la permutación a un conjunto
def AplicarPermConj(permutacion, conjunto):

  return conjunto[permutacion.array_form]

# Función para aplicar la permutación a un posición
def AplicarPermPos(permutacion, posicion):

  return permutacion.apply(posicion)


if __name__ == "__main__":

    # Definir permutaciones
    perm1 = Permutation([1, 0, 2]) # Definimos la posición de todos los elementos
    perm2 = Permutation([2, 1, 0])
    perm3 = Permutation(1, 2, 0)   # El ciclo define la permutación
    perm_ciclos = Permutation(1,2)(2,4)

    print("\nEJEMPLO DE COMPOSICIÓN DE PERMUTACIONES:\n")

    print("Permutación 1:", perm1)
    print("Permutación 2:", perm2)
    print("Permutación 3:", perm3)
    print("Permutación con varios ciclos:", perm_ciclos)

    # Componer permutaciones
    perm_composed = perm1 * perm2 * perm3
    print("Composición de las 3 permutaciones:", perm_composed)

    # Aplicar la permutación a un conjunto de elementos
    print("\nEJEMPLO DE APLICACIÓN DE PERMUTACIONES:\n")
    conjunto = ['rojo', 'azul', 'amarillo']
    print("Conjunto inicial:", conjunto)
    conjunto_permutado1 = [conjunto[i] for i in perm1.array_form]
    print("Conjunto tras aplicar permutación 1:", conjunto_permutado1)
    conjunto_permutado2 = [conjunto[i] for i in perm2.array_form]
    print("Conjunto tras aplicar permutación 2:", conjunto_permutado2)
    conjunto_permutado3 = [conjunto[i] for i in perm3.array_form]
    print("Conjunto tras aplicar permutación 3:", conjunto_permutado3)
    conjunto_permutado123 = [conjunto[i] for i in perm_composed.array_form]
    print("Conjunto tras aplicar permutación 123:", conjunto_permutado123)

    # Recordemos que el grupo simétrico Sn no es conmutativo
    perm4 = Permutation([1, 2, 0])
    perm5 = Permutation([0, 2, 1])
    print("\nEl grupo de simétrico no es abeliano, y además recordemos que se usa la \
la siguiente sintaxis para el orden de aplicación ( perm_i * perm_j = perm_i(perm_j) ):")
    print("Permutación 4:", perm4)
    print("Permutación 5:", perm5)

    perm45 = perm4 * perm5
    perm54 = perm5 * perm4
    print("perm4 * perm5 =", perm45)
    print("perm5 * perm4 =", perm54)

    # Inversa de una permutacion
    print("\nPERMUTACIONES INVERSAS:\n")
    print("Permutación 1:", perm1, "-->  Inversa Permutación 1:", perm1**(-1))
    print("\nPermutación 2:", perm2, "-->  Inversa Permutación 2:", perm2**(-1))
    print("\nPermutación 3:", perm3, "-->  Inversa Permutación 3:", perm3**(-1))
    print("\nPermutación 4:", perm4, "-->  Inversa Permutación 4:", perm4**(-1))
    print("\nPermutación 5:", perm5, "-->  Inversa Permutación 5:", perm5**(-1))

    
    
    # Pruebas para elegir el método para aplicar una permutación a un conjunto dado
    print("\nPRUEBAS DE EFICIENCIA PARA LA APLICACIÓN DE PERMUTACIONES SOBRE CONJUNTOS:\n")
    conjunto_largo_manual = list(range(10))
    conjunto_largo_np = np.array(conjunto_largo_manual)

    permutacion_arbitraria = Permutation(np.random.permutation(10))

    # Medimos el tiempo de ejecución de la opción de desarrollo manual de la lista
    tiempo_lista = timeit.timeit(
        "conjunto_permutado = [conjunto_largo_manual[i-1] for i in permutacion_arbitraria]",
        globals = globals(),
        number = 1  # Número de veces que se ejecuta la operación
    )

    # Medimos el tiempo de ejecución de la opción con operaciones vectorizadas de Numpy
    tiempo_numpy = timeit.timeit(
        "conjunto_permutado = conjunto_largo_np[permutacion_arbitraria.array_form]",
        globals = globals(),
        number = 1  # Número de veces que se ejecuta la operación
    )

    print("Pruebas para conjuntos pequeños y pocas permutaciones")
    print("Tiempo con lista de comprensión:", tiempo_lista)
    print("Tiempo con Numpy vectorizado:", tiempo_numpy)

    conjunto_largo_manual = list(range(10))
    conjunto_largo_np = np.array(conjunto_largo_manual)

    permutacion_arbitraria = Permutation(np.random.permutation(10))

    # Medimos el tiempo de ejecución de la opción de desarrollo manual de la lista
    tiempo_lista = timeit.timeit(
        "conjunto_permutado = [conjunto_largo_manual[i-1] for i in permutacion_arbitraria]",
        globals = globals(),
        number = 100000  # Número de veces que se ejecuta la operación
    )

    # Medimos el tiempo de ejecución de la opción con operaciones vectorizadas de Numpy
    tiempo_numpy = timeit.timeit(
        "conjunto_permutado = conjunto_largo_np[permutacion_arbitraria.array_form]",
        globals = globals(),
        number = 100000  # Número de veces que se ejecuta la operación
    )

    print("\nPruebas para conjuntos pequeños y muchas permutaciones")
    print("Tiempo con lista de comprensión:", tiempo_lista)
    print("Tiempo con Numpy vectorizado:", tiempo_numpy)

    conjunto_largo_manual = list(range(100000))
    conjunto_largo_np = np.array(conjunto_largo_manual)

    permutacion_arbitraria = Permutation(np.random.permutation(100000))

    # Medimos el tiempo de ejecución de la opción de desarrollo manual de la lista
    tiempo_lista = timeit.timeit(
        "conjunto_permutado = [conjunto_largo_manual[i-1] for i in permutacion_arbitraria]",
        globals = globals(),
        number = 1  # Número de veces que se ejecuta la operación
    )

    # Medimos el tiempo de ejecución de la opción con operaciones vectorizadas de Numpy
    tiempo_numpy = timeit.timeit(
        "conjunto_permutado = conjunto_largo_np[permutacion_arbitraria.array_form]",
        globals = globals(),
        number = 1  # Número de veces que se ejecuta la operación
    )

    print("\nPruebas para conjuntos grandes y pocas permutaciones")
    print("Tiempo con lista de comprensión:", tiempo_lista)
    print("Tiempo con Numpy vectorizado:", tiempo_numpy)

    conjunto_largo_manual = list(range(100000))
    conjunto_largo_np = np.array(conjunto_largo_manual)

    permutacion_arbitraria = Permutation(np.random.permutation(100000))

    # Medimos el tiempo de ejecución de la opción de desarrollo manual de la lista
    tiempo_lista = timeit.timeit(
        "conjunto_permutado = [conjunto_largo_manual[i-1] for i in permutacion_arbitraria]",
        globals = globals(),
        number = 100  # Número de veces que se ejecuta la operación
    )

    # Medimos el tiempo de ejecución de la opción con operaciones vectorizadas de Numpy
    tiempo_numpy = timeit.timeit(
        "conjunto_permutado = conjunto_largo_np[permutacion_arbitraria.array_form]",
        globals = globals(),
        number = 100  # Número de veces que se ejecuta la operación
    )

    print("\nPruebas para conjuntos grandes y muchas permutaciones")
    print("Tiempo con lista de comprensión:", tiempo_lista)
    print("Tiempo con Numpy vectorizado:", tiempo_numpy)

    print("\nEJEMPLOS DE APLICACIÓN\n")
    perm = Permutation(10)(1,3,5,7)
    conjunto = np.array([0,1,2,3,4,5,6,7,8,9,10])
    print("Permutacion:", perm)

    # Permutamos lista
    print("Aplicamos permutación:", AplicarPermConj(perm, conjunto))

    # Permutamos posiciones
    perm_pos = []
    for i in range(len(conjunto)):
        perm_pos.append(AplicarPermPos(perm, i))
        print("Permutamos posiciones:", perm_pos)
    print("\n")