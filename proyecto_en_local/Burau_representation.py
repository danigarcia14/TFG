"""# MATRICES DE BURAU
El grupo de trenzas puede ser representado por un conjunto de matrices conocidas como la "Representación Coloreada de Burau". Existiendo una matriz de Burau (junto con la permutación proyectada) para cada palabra que represente a una trenza, de manera que:

$$Π_{CB} : \mathbb{B}_{N} ⟶ GL(N, \mathbb{F}_{q}[t_1, t_1^{-1}, ..., t_N, t_N^{-1}]) \times \mathbb{S}_N$$
$$ \beta ⟶ \Pi_{CB} (\beta) = (CB(\beta), \sigma_{\beta}) $$

Conociendo $CB(b_i^{\pm1})$ para cualquier generador $b_i$, se extiende la representación a una trenza arbitraria  $\beta = b_{i_1}^{e_1}b_{i_2}^{e_2}...b_{i_k}^{e_k}$ de la siguiente forma:

$$ (CB(\beta), \sigma_{\beta}) = ( CB(b_{i_1}^{e_1}) ⋅ {}^{\sigma_{i_1}}\!CB(b_{i_2}^{e_2}) ... {}^{\sigma_{i_1}\sigma_{i_2} ... \sigma_{i_{k-1}}}\!CB(b_{i_k}^{e_k}) , σ_{i_1} ... \sigma_{i_k})$$

Para implementar la matriz de Burau asociada a una trenza arbitraria en $\mathbb{B}_{n}$, procederemos de manera incremental, creando la matriz de Burau asociada a:
1. Un generador positivo
2. Un generador negativo (inverso de un generador)
3. Un generador arbitrario
4. Una trenza arbitaria sin aplicar acciones de permutación (no es una representación correcta)
5. Una trenza arbitraria

**MATRIZ DE BURAU ASOCIADA A UN GENERADOR POSITIVO ($\sigma_1, \sigma_2, ..., \sigma_{n-1}$)**
"""
from sympy import *
import numpy as np
from braid import *

# Definimos los n t_values del grupo Bn
t1, t2, t3, t4, t5, t6, t7,t8,t9,t10 = symbols('t1 t2 t3 t4 t5 t6 t7 t8 t9 t10')
t_values = np.array([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10])

# Necesaria para no perder las colas invariantes de t_values tras permutar
perm_identity = Permutation(range(len(t_values)))

def MatrizBurauGenPos(generador, grado, t_values):

  # Identidad grado x grado
  Burau = eye(grado)

  # T_value a utilizar
  tv = t_values[generador-1]

  # Asignamos la matriz 3 x 3 característica de las matrices de Burau
  # en la posicion que define el generador pasado por parámetro
  if (generador == 1):
    Burau[0,0] = -tv
    Burau[0,1] = 1

  else:
    Burau[generador-1, generador-2] = tv
    Burau[generador-1, generador-1] = -tv
    Burau[generador-1, generador] = 1

  return Burau

print("Matriz de Burau asociada al generador 9 para el grupo de grado 10:\n")
MatrizBurauGenPos(9,10, t_values)

"""**MATRIZ DE BURAU ASOCIADA A UN GENERADOR NEGATIVO ($\sigma_1^{-1}, \sigma_2^{-1}, ..., \sigma_{n-1}^{-1}$)**"""

def MatrizBurauGenNeg(generador, grado, t_values):

  # Identidad grado x grado
  Burau = eye(grado)

  # T_value a utilizar
  tv = t_values[generador]

  # Asignamos la matriz 3 x 3 característica de las matrices de Burau
  # en la posicion que define el generador pasado por parámetro
  if (generador == 1):
    Burau[0,0] = -tv**-1
    Burau[0,1] = tv**-1

  else:
    Burau[generador-1, generador-2] = 1
    Burau[generador-1, generador-1] = -tv**-1
    Burau[generador-1, generador] = tv**-1

  return Burau

print("Matriz de Burau asociada al inverso del generador 9 para el grupo de\
 grado 10:\n")
MatrizBurauGenNeg(9,10, t_values)

"""**MATRIZ DE BURAU ASOCIADA A UN GENERADOR ARBITRARIO ($\sigma_1, \sigma_1^{-1}, ..., \sigma_{n-1},  \sigma_{n-1}^{-1}$)**"""

def MatrizBurauGen(generador, grado, t_values):

  if (generador < 0):
    return MatrizBurauGenNeg(-generador, grado, t_values)

  elif (generador == 0):
    return zeros(grado, grado)

  else:
    return MatrizBurauGenPos(generador, grado, t_values)

print("Matriz de Burau asociada al generador 9 para el grupo de grado 10:\n")
pprint(MatrizBurauGen(9, 10, t_values))
print("\nMatriz de Burau asociada al inverso del generador 9 para el grupo de\
 grado 10:\n")
pprint(MatrizBurauGen(-9, 10,t_values))

"""**MATRIZ DE BURAU ASOCIADA A UNA TRENZA ARBITRARIA ($\sigma_{i_1} \sigma_{i_2} ... \sigma_{i_k}$) SIN TENER EN CUENTA LA ACCIÓN SOBRE LOS T_VALORES**"""

# El parámetros "palabra" y "grado" se corresponderán con los atributos
# "elementos" y "grado" de la trenza a representar, respectivamente
def MatrizBurauSinAccion(palabra, grado, t_values):

  Burau = eye(grado)           # Para poder iterar sobre el producto de matrices

  # Multiplicamos las sucesivas matrices de Burau simples
  for i in palabra:
    Burau = Burau * MatrizBurauGen(i, grado, t_values)

  return Burau

# Definimos trenza a representar como matriz de Burau
b = Braid(5, [1,-3])
print("Trenza b representada por sus generadores:")
print(b.showBraid())

# La representamos como una matriz de Burau
Burau0 = MatrizBurauGen(1,5,t_values)
print("\nMatriz de Burau asociada al generador 1 para el grupo de grado 5:\n")
pprint(Burau0)
Burau1 = MatrizBurauGen(-3,5,t_values)
print("\nMatriz de Burau asociada al inverso del generador 3 para el grupo de\
 grado 5:\n")
pprint(Burau1)

# Calculamos manualmente el producto de ambas matrices
Burau01 = MatrizBurauSinAccion(b.elementos,b.grado, t_values)
print("\nMatriz de Burau asociada a la trenza b:\n")
pprint(Burau01)

"""**MATRIZ DE BURAU ASOCIADA A UNA TRENZA ARBITRARIA ($\sigma_{i_1} \sigma_{i_2} ... \sigma_{i_k}$)**

Presentamos dos versiones de la implementación de la matriz de Burau general: iterando los productos de izquierda a derecha y de derecha izquierda. Así, testeando los tiempos, podremos elegir la más rápida para nuestro problema.
"""

import time   # Para medir tiempos

# El parámetros "palabra" y "grado" se corresponderán con los atributos
# "elementos" y "grado" de la trenza a representar, respectivamente
def MatrizBurauID(palabra, grado, t_values):

  Burau = eye(grado)          # Para poder iterar sobre el producto de matrices
  ciclo_gen = Permutation(0)  # Almacenamos el ciclo del generador actual
  perm_actual = Permutation(0)# Almacenamos la permutación a aplicar actual
  t_values_perm = t_values    # Almacenamos t_values a aplicar actuales

  # Multiplicamos las sucesivas matrices de Burau simples de izquierda a derecha
  # (tras aplicar acciones)
  k=0
  print("\n")
  for i in palabra:
    start_time = time.time()
    k+=1
    if (k%10 == 9 or k%10 == 4):
      # Expandiendo cada x iteraciones conseguimos mejores tiempo de ejecuciones
      Burau = expand(Burau)
    Burau = Burau * MatrizBurauGen(i, grado, t_values_perm)
    ciclo_gen = ProyectarSn([i], grado)
    perm_actual = ciclo_gen * perm_actual
    t_values_perm = AplicarPermConj(perm_actual, t_values)
    end_time = time.time()
    execution_time_ID = end_time - start_time
    print("Tiempo Versión ID, Iteración:", k,  execution_time_ID, "segundos")

  return expand(Burau)

def MatrizBurauDI(palabra, grado, t_values):

  Burau = eye(grado)          # Para poder iterar sobre el producto de matrices
  ciclo_gen = Permutation(0)  # Almacenamos el ciclo del generador actual
  perm_actual = ProyectarSn(palabra, grado)  # Almacenamos la perm a aplicar
  t_values_perm = []          # Almacenamos t_values a aplicar actuales

  # Multiplicamos las sucesivas matrices de Burau simples de derecha a izquierda
  # (tras aplicar acciones)
  k=0
  print("\n")
  for i in reversed(palabra):
    start_time = time.time()
    k+=1
    if (k%10 == 9 or k%10 == 4):
      # Expandiendo cada x iteraciones conseguimos mejores tiempo de ejecuciones
      Burau = expand(Burau)
    ciclo_gen = ProyectarSn([i], grado)
    perm_actual = ciclo_gen * perm_actual # Eliminamos primer ciclo de la perm
    t_values_perm = AplicarPermConj(perm_actual, t_values)
    Burau = MatrizBurauGen(i, grado, t_values_perm) * Burau
    end_time = time.time()
    execution_time_ID = end_time - start_time
    print("Tiempo Versión DI, Iteración:", k,  execution_time_ID, "segundos")

  return expand(Burau)

if __name__ == "__main__":

  # Las aplicaciones de la función expand facilitan la cancelación de los
  # elementos de los polinomios de Laurent, al ser expandidos. Esto ayuda a
  # gestionar su almacenamiento más eficientemente, reflejándose esto tan en los
  # tiempos de ejecución como en la representación final (la cual es más amigable)
  # de la matriz

  """**Pruebas de Ejecución del cálculo de la Matriz de Burau**"""

  # Definimos trenza a representar como matriz de Burau
  b = Braid(5, [-2,1,3,4,2,-2,1])
  print("Trenza representada por sus generadores:", b.showBraid())
  print("Permutación asociada:", b.perm)

  # Calculamos inductivamente la matriz de Burau de la trenza completa (I-D)
  start_time = time.time()
  BurauID = MatrizBurauID(b.elementos, b.grado, t_values)
  end_time = time.time()
  execution_time = end_time - start_time
  print("\nMatriz de Burau asociada a la trenza b, calculada en ",execution_time,
        "segundos:\n")
  pprint(BurauID)

  # Evaluamos matriz de Burau
  eval = np.array([10,1,2,3,4,5,6,7,8,9])
  start_time = time.time()
  BurauID_evalID = BurauID.subs({t_values[i] : eval[i]
                              for i in range(len(t_values))})
  end_time = time.time()
  execution_time = end_time - start_time
  print("\nMatriz de Burau asociada a la trenza b, evaluada en", execution_time,
        "segundos:\n")
  pprint(BurauID_evalID)

  # Calculamos inductivamente la matriz de Burau de la trenza completa (D-I)
  start_time = time.time()
  BurauDI = MatrizBurauDI(b.elementos, b.grado, t_values)
  end_time = time.time()
  execution_time = end_time - start_time
  print("\nMatriz de Burau asociada a la trenza b, calculada en ",execution_time,
        "segundos:\n")
  pprint(BurauDI)

  # Evaluamos matriz de Burau
  eval = np.array([10,1,2,3,4,5,6,7,8,9])
  start_time = time.time()
  Burau_evalDI = BurauDI.subs({t_values[i] : eval[i]
                              for i in range(len(t_values))})
  end_time = time.time()
  execution_time = end_time - start_time
  print("\nMatriz de Burau asociada a la trenza b, evaluada en", execution_time,
        "segundos:\n")
  pprint(Burau_evalDI)

  """**Pruebas de eficiencia en cálculo de Matriz de Burau**"""

  # Generamos una palabra larga
  elementos = [1,2,3,4,5,-5,-5,-4,-5,-5]
  elementos_final = []
  for i in range(5):
    elementos_final = elementos_final + elementos
  print(len(elementos_final))

  start_time = time.time()
  BurauID = MatrizBurauID(elementos_final, 8, t_values)
  end_time = time.time()
  execution_time_ID = end_time - start_time
  print("\n\nTiempo TOTAL Versión ID:", execution_time_ID, "segundos\n\n")
  del BurauID

  start_time = time.time()
  BurauDI = MatrizBurauID(elementos_final, 8, t_values)
  end_time = time.time()
  execution_time_DI = end_time - start_time
  print("\n\nTiempo TOTAL Versión DI:", execution_time_DI, "segundos\n\n")
  del BurauDI

  """Para una palabra con 50 elementos, los resultados son ligeramente mejores con la versión ID. Sin embargo, al duplicar la longitud de la palabra, ambos métodos se vuelven insostenibles para el cálculo. Afortunadamente, la E-Multiplicación, la función principal que se utilizará en el algoritmo, se puede definir de manera iterativa sin necesidad de construir la representación de Burau para la palabra completa. Esto nos tranquiliza respecto a los problemas de eficiencia.
  """