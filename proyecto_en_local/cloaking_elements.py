"""# CLOAKING ELEMENTS

Una vez definida la E-Multiplicación, para cada $(M, \sigma) \in GL(N, \mathbb{F}_q) \times \mathbb{S}_N $ se puede definir el subgrupo $Cloak_{(M, \sigma)} ⊂ \mathbb{B}_N$ formado por las trenzas $\beta$ que verifican

$$ (M, \sigma) \ast \beta = (M, \sigma)$$

para una $\ast$ E-Multiplicación fijada (= conjunto de t_values fijados).

Aplicaremos el siguiente procedimiento para calcular Cloaking Elements de $(M, \sigma)$, dado un conjunto de t-values definitorios de la E-Multiplicación, en el que al menos 2, obviando el primero y el último, son igual 1:

1. Fijamos $a, b$ con $ 1 < a < b < N$ y $t_a = 1 = t_b$
2. Tomamos un generador $b_i$ cualquiera de $B_n$
3. Tomamos $w \in \mathbb{B}_N$ verificando $\pi_{w}(i) = \sigma^{-1}(a), \space \pi_{w}(i+1) = \sigma^{-1}(b)$
4. La trenza $ v = wb_{i}^{2}w^{-1} \in Cloak_{(M, \sigma)}$
"""

import random
from E_Multiplication import *

# Comprueba si los t_values contienen al menos 2 t_unos (principio y final no
# cuentan como t_unos) siendo exactamente gradoBn t_values
def Comprobador_cloak_t_unos(t_eval, gradoBn):

  # Comprobemos que hay exactamente gradoBn t_values
  if (len(t_eval) == gradoBn):

    # Comprobemos que al menos hay 2 t_values (a parte del primero y el último)
    # con valor 1 (t_unos) y nos quedamos con los 2 primeros
    count = 0           # Contador de t_values == 1
    t_unos = [-1, -1]   # Almacenará las posiciones de los t_unos
    for i in range(gradoBn):
      if (count == 2):  # Paramos de iterar cuando encontremos 2 t_unos
        break
      else :
        if (i != (gradoBn - 1)): # Obviamos el primero y el último
          if (t_eval[i] == 1):
            count += 1
            t_unos[count-1] = i   # Guardamos la posicion de los t_values

    if (count == 2):
      return t_unos
    else:
      print("\nEl procedimiento no es aplicable para este conjunto de t_values\
      \n")
      return None

  # Si no cumple el requisito de ser exactamente gradoBn no son t_unos válidos
  else:
    print("\nEl procedimiento no es aplicable para este conjunto de t_values\n")
    return None

# Función auxiliar que genera una palabra aleatoria (trenza) del grupo n-ésimo
# de longitud  mínima l1  y máxima l2
def Palabra_aleatoria(n, l1, l2):

  # Crea una lista aleatoria de números entre -(n-1) y n-1 (excluido el 0)
  numeros = list(range(-n+1,n))
  numeros.remove(0)

  # Genera la longitud aleatoriamente entre 1 y l
  longitud = random.randint(l1,l2)

  # Genera los elementos de la palabra
  palabra = []
  for _ in range(longitud):
    numero = random.choice(numeros)
    palabra.append(numero)

  return palabra

# Genera la trenza que junto a "generador" define el Cloak Element
def Generador_trenza_cloak(generador, permutacionM, t_unos, gradoBn):

  # Generamos aleatoriamente la potencial trenza junto con su permutacion
  # aplicada a generador y generador + 1 a comparar con (*)
  palabra_generada = Palabra_aleatoria(gradoBn, gradoBn*5, gradoBn*10)
  permutacion_generada = ProyectarSn(palabra_generada, gradoBn)

  # Repetimos el proceso hasta que se den las condiciones para los t_unos
  while ((AplicarPermPos(permutacion_generada,generador-1) != AplicarPermPos(permutacionM**(-1),t_unos[0])) or
         (AplicarPermPos(permutacion_generada, generador) != AplicarPermPos(permutacionM**(-1),t_unos[1]))):
    palabra_generada = Palabra_aleatoria(gradoBn, gradoBn*5, gradoBn*10)
    permutacion_generada = ProyectarSn(palabra_generada, gradoBn)

  # Una vez encontrada la palabra cuya permutacion proyeccion cumple los 2
  # requisitos del procedimiento, creamos formalmente la trenza asociada
  trenza_Cloak = Braid(gradoBn, palabra_generada)

  return trenza_Cloak

# Genera el Cloak Element para (M, permutacionM), los t_values fijados
# y con generador como semilla (replicable el procedimiento para cualquier otro
# generador, obteniendo nuevos elementos del subgrupo Cloak)
def Cloaking_Element(permutacionM, t_values, generador, gradoBn):

  #Calculamos los dos primeros t_unos (si no los hay devolvemos error)
  t_unos = Comprobador_cloak_t_unos(t_values, gradoBn)
  if (t_unos == None):
    return None
  else:

    # Generamos la trenza w que cumpla ambas restricciones para los t_unos
    w = Generador_trenza_cloak(generador, permutacionM, t_unos, gradoBn)

    # Generamos la trenza asociada al generador elegido
    trenza_generador = Braid(gradoBn, [generador])

    # Construimos la trenza Cloak Element
    palabra_final = w.elementos + trenza_generador.elementos + \
    trenza_generador.elementos + w.inverseBraid().elementos

    Cloak_Element = Braid(gradoBn, palabra_final)

    return Cloak_Element

if __name__ == "__main__":

  # Prueba comprobador t_unos
  gradoBn = 10
  t_values = np.array([1,4,-1,1,1,4,1,7,9,1])
  t_unos = Comprobador_cloak_t_unos(t_values, gradoBn)
  print("COMPROBADOR T_UNOS:")
  print("T_values donde buscar t_unos: ", t_values)
  print("Posiciones de los 2 primeros t_unos: ",
        t_unos)

  # Prueba generador trenza auxiliar Cloak
  generador = 6
  permutacionM = ProyectarSn([2,5,4,8,5,-2], gradoBn)
  print("\nGENERADOR PERMUTACION PARA T_UNOS:")
  print("Permutacion M:", permutacionM)
  # w es la trenza auxiliar que buscabamos para construir el Cloak Element
  w = Generador_trenza_cloak(generador, permutacionM, t_unos, 10)
  print("Permutacion aleatoria que cumple las restricciones definidas por los\
  t_unos:", Generador_trenza_cloak(generador, permutacionM, t_unos, 10).perm)
  print("Efectivamente: \n\
  \t rw(generador) = ", w.perm.apply(generador-1))
  print("\t rw(generador + 1) = ", w.perm.apply(generador))
  print("\t r-1(t_unos[0]) = ", (permutacionM**(-1)).apply(t_unos[0]))
  print("\t r-1(t_unos[1]) = ", (permutacionM**(-1)).apply(t_unos[1]))

  # Prueba generador Cloak Element
  Cloak_Element = Cloaking_Element(permutacionM, t_values, generador, gradoBn)
  print("\nCloak Element para (M, r) y los t_values fijados:\n",
        Cloak_Element.elementos)

  """Comprobemos ahora que efectivamente cualquier $\beta$ Cloak Element que generamos mediante la función Cloaking_Element() desaparece al multiplicarse por la derecha para los $(M, \sigma)$ y la E-Multiplicación fijados:

  $$ (M, \sigma) \ast \beta = (M, \sigma)$$

  """

  # M y permM arbitrarias
  gradoBn = 8
  gradoCF = 5
  M = Matrix(np.random.randint(0, 32, size = (gradoBn, gradoBn)))
  permutacionM = Permutation.random(gradoBn)
  t1, t2, t3, t4, t5, t6, t7,t8 = symbols('t1 t2 t3 t4 t5 t6 t7 t8')
  t_values = np.array([t1, t2, t3, t4, t5, t6, t7, t8])
  eval = np.array([20,1,3,4,4,17,1,10])

  # Calculamos un Cloak Element para M, permM y los t_values elejidos
  print("NOTA: PARA CONSEGUIR QUE CALCULE UN CLOACK ELEMENT EN TODAS LAS\
  EJECUCIONES EN UN \nTIEMPO RAZONABLE, HEMOS TENIDO QUE PERMITIR UNA LONGITUD \
  PARA TRENZA AUXILIAR DE \nHASTA 10*gradoBN. \nSupononemos que para longitudes \
  menores es más difícil combinar los generadores satisfaciendo los requisitos\
  . Al aumentar la longitud \nestos requisitos se vuelven equiprobables con el \
  resto de posibilidades.\n\n")

  Cloak_Element = Cloaking_Element(permutacionM, eval, 3, gradoBn)

  print("Matriz M:\n", np.array(M))
  print("\nPermutación_M:", permutacionM)
  print("\nT_values:", eval)
  print("\nCloak Element generado:", Cloak_Element.elementos)
  print("\nLongitud Cloak Element generado:", len(Cloak_Element.elementos))
  print("\nPermutación Cloak Element:", Cloak_Element.perm)

  # Aplicamos la E-Multiplicación para validar procedimiento
  print("T_VALUES", t_values)
  print("EVAL", eval)
  E_mult_Cloaking_Element0 = E_Multiplicacion(M, permutacionM,
    Cloak_Element.elementos, gradoBn, gradoCF, t_values, eval)
  print("\nE-Multiplicación para M y permM:\n", np.array(E_mult_Cloaking_Element0[0]))
  print("\nPermutación final:", E_mult_Cloaking_Element0[1])