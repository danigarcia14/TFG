
from sympy import *
import numpy as np
from braid import *
import time   # Para medir tiempos

# MATRIZ DE BURAU ASOCIADA A UN GENERADOR POSITIVO 
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

# MATRIZ DE BURAU ASOCIADA A UN GENERADOR NEGATIVO 
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

# MATRIZ DE BURAU ASOCIADA A UN GENERADOR ARBITRARIO
def MatrizBurauGen(generador, grado, t_values):

  if (generador < 0):
    return MatrizBurauGenNeg(-generador, grado, t_values)

  elif (generador == 0):
    return zeros(grado, grado)

  else:
    return MatrizBurauGenPos(generador, grado, t_values)
  
# MATRIZ DE BURAU ASOCIADA A UNA TRENZA ARBITRARIA 
  # El parámetros "palabra" y "grado" se corresponderán con los atributos
  # "elementos" y "grado" de la trenza a representar, respectivamente
def MatrizBurauSinAccion(palabra, grado, t_values):

  Burau = eye(grado)  # Para poder iterar sobre el producto de matrices

  # Multiplicamos las sucesivas matrices de Burau simples
  for i in palabra:
    Burau = Burau * MatrizBurauGen(i, grado, t_values)

  return Burau

# MATRIZ DE BURAU ASOCIADA A UNA TRENZA ARBITRARIA
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
    #print("Tiempo Versión ID, Iteración:", k,  execution_time_ID, "segundos")

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
    #print("Tiempo Versión DI, Iteración:", k,  execution_time_ID, "segundos")

  return expand(Burau)

if __name__ == "__main__":

  # Definimos los n t_values del grupo Bn
  t1, t2, t3, t4, t5, t6, t7,t8,t9,t10 = symbols('t1 t2 t3 t4 t5 t6 t7 t8 t9 t10')
  t_values = np.array([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10])
  # Necesaria para no perder las colas invariantes de t_values tras permutar
  perm_identity = Permutation(range(len(t_values)))

  print("\nEJEMPLOS DE CÁLCULO DE MATRICES DE BURAU CON LOS DISTINTOS MÉTODOS IMPLEMENTADOS:\n")

  print("Matriz de Burau asociada al generador 9 para el grupo de grado 10:\n")
  pprint(MatrizBurauGenPos(9,10, t_values))

  print("\nMatriz de Burau asociada al inverso del generador 9 para el grupo de\
  grado 10:\n")
  pprint(MatrizBurauGenNeg(9,10, t_values))

  print("\nMatriz de Burau asociada al generador 9 para el grupo de grado 10:\n")
  pprint(MatrizBurauGen(9, 10, t_values))

  print("\nMatriz de Burau asociada al inverso del generador 9 para el grupo de\
  grado 10:\n")
  pprint(MatrizBurauGen(-9, 10,t_values))


  # Definimos trenza a representar como matriz de Burau
  b = Braid(5, [1,-3])
  print("\nTrenza b representada por sus generadores:")
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
  print("\n'Matriz de Burau' asociada a la trenza b sin tener en cuenta la aplicación de acciones:\n")
  pprint(Burau01)


  print("\nPRUEBAS DE EJECUCIÓN DEL CÁLCULO DE LA MATRIZ DE BURAU:\n")

  # Definimos trenza a representar como matriz de Burau
  b = Braid(5, [-2,1,3,4,2,-2,1])
  print("Trenza representada por sus generadores:", b.showBraid())
  print("Permutación asociada:", b.perm)

  # Calculamos inductivamente la matriz de Burau de la trenza completa (I-D)
  start_time = time.time()
  BurauID = MatrizBurauID(b.elementos, b.grado, t_values)
  end_time = time.time()
  execution_time = end_time - start_time
  print("Matriz de Burau asociada a la trenza b, calculada mediante 'MatrizBurauID' en ",execution_time,
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
  print("\nMatriz de Burau asociada a la trenza b, calculada mediante 'MatrizBurauDI' en ",execution_time,
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

  print("\nPRUEBAS DE EFICIENCIA ENTRE LOS MÉTODOS 'MatrizBurauID' y 'MatrizBurauDI':")

  # Generamos una palabra más larga
  elementos = [1,2,3,4,5,-5,-5,-4,-5,-5]
  elementos_final = []
  for i in range(5):
    elementos_final = elementos_final + elementos

  start_time = time.time()
  BurauID = MatrizBurauID(elementos_final, 8, t_values)
  end_time = time.time()
  execution_time_ID = end_time - start_time
  print("Tiempo TOTAL Versión ID:", execution_time_ID, "segundos")
  del BurauID

  start_time = time.time()
  BurauDI = MatrizBurauDI(elementos_final, 8, t_values)
  end_time = time.time()
  execution_time_DI = end_time - start_time
  print("\nTiempo TOTAL Versión DI:", execution_time_DI, "segundos\n")
  del BurauDI
