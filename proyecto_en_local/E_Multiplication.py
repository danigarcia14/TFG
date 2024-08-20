
from Burau_representation import *
from pyfinite import ffield


# Función evaluadora E-Multiplicación
def Eval_CB_EMult(generador, gradoBn, gradoCF, permutacion, t_values, eval):

  # Aplicamos la permutación a los t_values
  t_values = AplicarPermConj(permutacion, t_values)
  eval = AplicarPermConj(permutacion, eval)

  # En primer lugar, calculamos la Matriz de Burau asociada al generador
  CB = MatrizBurauGen(generador, gradoBn, t_values)

  # Evaluamos CB con los t_values (considerándolos enteros)
  CB = CB.subs({t_values[i] : eval[i] for i in range(len(t_values))})

  CB = abs(CB) # Podemos obviar los 'signos -' al trabajar en Z2


  if (generador < 0): # Solo en este caso ha habido inversiones

    # Creamos el campo finito de grado 2^gradoCF
    CF = ffield.FField(gradoCF)

    # Buscamos los elementos no enteros (los que hay que corregir su inversión)
    for i in range(CB.rows):
      for j in range(CB.cols):
        if not CB[i,j].is_integer:
          CB[i,j] = CF.Inverse(int(1 / CB[i,j]))

  return CB

# Función multiplicadora de matrices sobre el campo CF(2^n)
def Mult_Matrix_CF(matriz1, matriz2, gradoCF):

  # Creamos el campo finito de grado 2^gradoCF
  CF = ffield.FField(gradoCF)

  # Matriz donde devolveremos el resultado
  filas_res = matriz1.rows        # Coinciden las filas de matriz1 y resultado
  columnas_res = matriz2.cols     # Igual para las columnas de matriz2
  resultado = Matrix.zeros(filas_res, columnas_res)

  for i in range(filas_res):
    for j in range(columnas_res):
      for k in range(matriz1.cols):
        resultado[i,j] = CF.Add(resultado[i,j],
          int(CF.Multiply(int(matriz1[int(i),int(k)]),
                          int(matriz2[int(k),int(j)]))))

  return resultado

# Función para E-Multiplicar (M, permutacionM)*(palabra, permutacionPalabra)
def E_Multiplicacion(M, permutacionM, palabra,
                    gradoBn, gradoCF, t_values, eval):

  # Una E-Multiplicación (acumulada) para cada generador de la palabra
  for gen in palabra:

    # Calculamos la evaluación de la r->CB(gen)
    Eval_aux = Eval_CB_EMult(gen, gradoBn,gradoCF, permutacionM, t_values, eval)

    # Multiplicamos las matrices (acumulativamente) en CF(2^gradoCF)
    M = Mult_Matrix_CF(Matrix(M), Matrix(Eval_aux), gradoCF)

    # Actualizamos permutación/acción
    permutacionM = ProyectarSn([gen], gradoBn) * permutacionM

  return (M, permutacionM)

# E-Multiplicación trivial
def E_Multiplicacion_P(palabra, gradoBn, gradoCF, t_values, eval):

  return E_Multiplicacion(np.eye(gradoBn), Permutation(range(gradoBn)), palabra,
                          gradoBn, gradoCF, t_values, eval)

if __name__ == "__main__":

  print("\nEJEMPLO DE EJECUCIÓN DE 'Eval_CB_EMult':\n")

  # Creamos el campo finito de 32 elementos (2^5)
  F32 = ffield.FField(5)

  generador = -9
  gradoBn = 10
  gradoCF = 5
  permutacion = ProyectarSn([1,2,3,4,5,6,7,8,9], 10)
  print("Permutación aplicada a los t_values:\n", permutacion)
  t1, t2, t3, t4, t5, t6, t7,t8,t9,t10 = symbols('t1 t2 t3 t4 t5 t6 t7 t8 t9 t10')
  t_values = np.array([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10])
  eval = np.array([15,10,1,1,4,17,8,7,21,7])

  CB_prueba = Eval_CB_EMult(generador, gradoBn, gradoCF, permutacion, t_values,
                            eval)
  print(f"\nCB evaluada del generador {generador} tras aplicar la corrección de \
  inversión:\n", np.array(CB_prueba))




  print("\nEJEMPLO DE EJECUCIÓN DE 'Mult_Matrix_CF':\n")

  # Ejemplo de multiplicación para 2 matrices de Burau ya permutadas y evaluadas
  # (preparadas como términos de la E-Multiplicación)
  generador1 = 9
  generador2 = -9
  gradoBn = 10
  gradoCF = 5
  permutacion1 = ProyectarSn([], 10)
  permutacion2 = ProyectarSn([generador2], 10)
  t1, t2, t3, t4, t5, t6, t7,t8,t9,t10 = symbols('t1 t2 t3 t4 t5 t6 t7 t8 t9 t10')
  t_values = np.array([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10])
  eval = np.array([15,10,1,1,4,17,8,7,21,7])

  CB_prueba1 = Eval_CB_EMult(generador1, gradoBn, gradoCF, permutacion1, t_values,
                            eval)
  CB_prueba2 = Eval_CB_EMult(generador2, gradoBn, gradoCF, permutacion2, t_values,
                            eval)
  # Multiplicamos CB_prueba1 y CB_prueba2 en el cuerpo CF(2^gradoCF)
  resultado = Mult_Matrix_CF(CB_prueba1, CB_prueba2, gradoCF)

  print(f"\nCB_prueba1 (=CB evaluada del generador {generador1}):\n", np.array(CB_prueba1))
  print(f"\nCB_prueba2 (=CB evaluada del generador {generador2}):\n", np.array(CB_prueba2))
  print(f"\n'Multiplicación' en CF(2^{gradoCF}) de CB_prueba1 y CB_prueba2:\n",
        np.array(resultado))

  
  print("\n\nEJEMPLO DE EJECUCIÓN DE LA E-MULTIPLICACION COMPLETA:\n") 

  print("Datos de la E-Multiplicación:\n")
  gradoBn = 4
  gradoCF = 5
  M = Matrix(np.random.randint(0, 32, size = (gradoBn, gradoBn)))
  #M = Matrix([[5,18,0,0], [0,0,0,1],[0,2,0,0],[1,0,9,1]])
  permutacionM = Permutation.random(gradoBn)
  #permutacionM = Permutation(0,3,1,2)
  trenza = Braid(gradoBn, [-2, 1, 3])
  t1, t2, t3, t4 = symbols('t1 t2 t3 t4')
  t_values = np.array([t1, t2, t3, t4])
  eval = np.array([1, 26, 21, 19])

  # E-Multiplicación para M y permM arbitrarias
  E_mult = E_Multiplicacion(M, permutacionM, trenza.elementos, gradoBn, gradoCF,
                            t_values, eval)
  print("M =", np.array(M))
  print("\npermutacionM = ", permutacionM)
  print("\nPalabra trenza = ", trenza.elementos)
  print("\nPermutación trenza = ", trenza.perm)

  print("\n\nE-Multiplicación para los datos elegidos:\n")
  print("Matriz final:\n")
  pprint(E_mult[0])
  print("\nPermutación final:", E_mult[1])

  print("\n\nEJEMPLO DE EJECUCIÓN DE LA E-MULTIPLICACION TRIVIAL:\n") 


  # E-Multiplicación para M y permM identidad
  E_mult_P = E_Multiplicacion_P(trenza.elementos, gradoBn, gradoCF, t_values,
                                eval)
  print("E-Multiplicación trivial para los datos elegidos:\n")
  print("Matriz resultado:\n")
  pprint(E_mult_P[0])
  print("\nPermutación resultado:", E_mult_P[1], "\n")
