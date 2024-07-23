"""# PERMUTACIONES

El grupo $\mathbb{S}_{n}$ de permutaciones se utiliza en dos casos principales:

1. Representación de Burau: Además de la matriz de Burau, la representación de Burau de una trenza $b$ incluye  la permutación $s$ asociada a la trenza, dándose $\phi(b) = s$ para $\phi : \mathbb{B}_{n} ⟶ \mathbb{S}_{n}$ la proyección natural de trenzas.

2. Matriz de Burau de una trenza de longitud mayor a 1: Las matrices de Burau de trenzas arbitrarias se definen mediante el "producto" recursivo de las matrices asociadas a los generadores de la trenza. Este "producto" $B_1 * B_2$ aplica previamente la permutación del primer generador a $B_2$, definiéndose como $\mathbb{B}_1 * \mathbb{B}_2 = \mathbb{B}_1 \cdot {}^{s_1}\!\mathbb{B}_2$. La permutación se aplica sobre el conjunto de t-values considerados en las matrices. Para una palabra de longitud arbitraria, se compone recursivamente dicho producto.

3. E-Multiplication: El mismo procedimiento explicado en el punto anterior, se utiliza para definir inductivamente la E-Multiplication con trenzas de longitud mayor a 1.

Está claro que estos puntos nos inducen a almacenar la permutación asociada a una trenza. También se podría considerar la opción de tener un método para las trenzas que calcule su permutación asociada en un momento dado:

1. Si añadimos la permutación asociada a la trenza como atributo del objeto, mantendríamos y actualizaríamos tal objeto operando sobre las propias permutaciones, estando la posibilidad de que el grupo de permutaciones ya esté resuelto por alguna biblioteca.
2. Si implementamos la recuperación de la permutación a partir de la trenza, evitamos "duplicar" información pero corremos el riesgo de no acceder a la permutación eficientemente en las múltiples ocasiones que será necesario.

Nos decantamos por la primera opción.
"""

from sympy.combinatorics import Permutation

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

    print("Permutación 1:", perm1)
    print("Permutación 2:", perm2)
    print("Permutación 3:", perm3)
    print("Permutación con varios ciclos:", perm_ciclos)

    # Componer permutaciones
    perm_composed = perm1 * perm2 * perm3
    print("Composición de las 3 permutaciones:", perm_composed)

    # Aplicar la permutación a un conjunto de elementos
    conjunto = ['rojo', 'azul', 'amarillo']
    print("\nConjunto inicial:", conjunto)
    conjunto_permutado1 = [conjunto[i] for i in perm1.array_form]
    print("Conjunto permutado 1:", conjunto_permutado1)
    conjunto_permutado2 = [conjunto[i] for i in perm2.array_form]
    print("Conjunto permutado 2:", conjunto_permutado2)
    conjunto_permutado3 = [conjunto[i] for i in perm3.array_form]
    print("Conjunto permutado 3:", conjunto_permutado3)
    conjunto_permutado123 = [conjunto[i] for i in perm_composed.array_form]
    print("Conjunto permutado 123:", conjunto_permutado123)

    # Recordemos que el grupo simétrico Sn no es conmutativo
    perm4 = Permutation([1, 2, 0])
    perm5 = Permutation([0, 2, 1])
    print("\nEl grupo de simétrico no es abeliano, y además recordemos que el\
    orden de \naplicación es igual que con las funciones\
    ( perm_i * perm_j = perm_i(perm_j) ):")
    print("Permutación 4:", perm4)
    print("Permutación 5:", perm5)

    perm45 = perm4 * perm5
    perm54 = perm5 * perm4
    print("perm4 * perm5 =", perm45)
    print("perm5 * perm4 =", perm54)

    # Inversa de una permutacion
    print("\nPERMUTACIONES INVERSAS:")
    print("\nPermutación 1:", perm1, "-->  Inversa Permutación 1:", perm1**(-1))
    print("\nPermutación 2:", perm2, "-->  Inversa Permutación 2:", perm2**(-1))
    print("\nPermutación 3:", perm3, "-->  Inversa Permutación 3:", perm3**(-1))
    print("\nPermutación 4:", perm4, "-->  Inversa Permutación 4:", perm4**(-1))
    print("\nPermutación 5:", perm5, "-->  Inversa Permutación 5:", perm5**(-1))

    """Consideramos dos opciones para aplicar una permutación sobre un conjunto:

    1. Desarrollo manual de la permutación:

            conjunto_permutado = [conjunto_manual[i-1] for i in permutacion_arbitraria]

    2. Operaciones vectorizadas Numpy:
        
            conjunto_permutado = conjunto_np[permutacion_arbitraria.array_form]

    Estudiemos que opción es más eficiente con distintos tamaños de conjuntos y cantidad de permutaciones:
    """

    import timeit
    import numpy as np

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

    """Las operaciones vectorizadas Numpy han demostrado ser más eficientes que el desarrollo manual en todos los casos, excepto en conjuntos pequeños y pocas permutaciones, donde la diferencia es mínima. Sin embargo, el caso más representativo es el de conjuntos pequeños y muchas permutaciones, donde Numpy es casi el doble rápido. Considerando además que el código de esta opción es mucho más amigable y replicable, podemos concluir que la mejor opción para aplicar permutacion a conjuntos es trabajar con `Numpy`."""

    # Ejemplos de aplicación
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