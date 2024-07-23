# REWRITING
"""
El último paso de la generación de la firma WalnutDSA consiste en la reescritura de la palabra representante de una trenza. El algoritmo de reescritura debe generar una nueva palabra equivalente que oculte suficientemente a la inicial.

En este caso, hemos elegido el algoritmo de reescritura estocástico descrito en ***Kayawood, a Key Agreement Protocol; Section 7***.

Se definirá un nuevo sistema de generadores del grupo $\mathbb{B_8}$, que seguirá cumpliendo la relaciones del grupo:

$$ σ_{i}σ_{i+1}σ_{i} = σ_{i+1}σ_{i}σ_{i+1} $$
$$ σ_{i}σ_{j} = σ_{j}σ_{i}, \ |i-j| > 1;  $$

(reescritas para el nuevo sistema), además de otras que emergerán de la nueva representación. Aplicando sus correspondientes equivalencias, conseguiremos ocultar la palabra en cuestión.

**PARTICIÓN $\mathcal{P}(N-1)$**

Primero, se elige una partición para el orden del anterior grupo trenzando, en este caso $8-1=7$. Por tanto, se define $\mathcal{P}(7) = \{p_1, p_2, ..., p_l\}$, con $3 \leq p_i$, de forma que:
$$ 7 = p_1 + p_2 + ... + p_l $$

Elegimos $p_1 = 3,\:\: p_2 = 4$
"""
from braid import *
import random

# Función que comprueba si el vector "particiones" define una partición válida
# de N
def ComprobadorParticion(N, particiones):

  # Se comprueba que 3 <= pi
  if (not all(parte > 2 for parte in particiones)):
    print("\nError --> Conjunto de partición elegido no válido (pi)")
    return False
  elif (sum(particiones) != N):
    print("\nError --> Conjunto de partición elegido no válido (SUM)")
    return False
  else:
    return True

# Generador de secuencia de valores R(P(N-1))
def GeneradorSecuenciaRParticion(particion):
  R = []
  R.append(1)
  for i in particion:
    R.append(R[-1] + i)    # ri = ri-1 + pi-1

  return R

"""
Para ser capaces de gestionar esto, almacenaremos todas las posibles representaciones que se obtienen directamente de la relación, como lógicas de detección. Esto se debe a que no son palabras exactas, ya que dependen de los índices $(i,j)$. La idea es almacenar las 10 posibles 2-subpalabras ($u$) aplicables por la relación, con su correspondientes 3-subpalabras ($L^{-1}R^{-1}$) por las que se sustituirán.

Presentamos dicha correspondencia en términos de $i, j$ y $\mu$:

*   1 $y_jy_i = y_iy_{j-1}y_{r_{μ+1}-1}^{-1}$       
*   2 $y_iy_{j-1} = y_jy_iy_{r_{μ+1}-1}$            
*   3 $y_{j-1}y_{r_{μ+1}-1}^{-1} = y_i^{-1}y_jy_i$  
*   4 $y_iy_{r_{μ+1}-1} = y_j^{-1}y_iy_{j-1}$       
*   5 $y_i^{-1}y_j = y_{j-1}y_{r_{μ+1}-1}^{-1}y_i^{-1}$       
*   6 $y_j^{-1}y_i = y_iy_{r_{μ+1}-1} y_{j-1}^{-1}$       
*   7 $y_{r_{μ+1}-1}^{-1}y_i^{-1} = y_{j-1}^{-1}y_i^{-1}y_j$      
*   8 $y_{r_{μ+1}-1}y_{j-1}^{-1} = y_i^{-1}y_j^{-1}y_i$       
*   9 $y_{j-1}^{-1}y_i^{-1} = y_{r_{μ+1}-1}^{-1}y_i^{-1}y_j^{-1}$       
*   10 $y_i^{-1}y_j^{-1} = y_{r_{μ+1}-1}y_{j-1}^{-1}y_i^{-1}$      

Implementamos el método `RewriteSubW` que recibirá una potencial 2-subpalabra y, en caso de corresponderse con alguna de estas 10 correspondencias, devolverá la 3-subpalabra correspondiente:
"""

# Función auxiliar para RewriteSubW - Caso Correspondencia 1
    # pasamos la correspondencia como una lista 'correspondencia_l' para simular
    # el paso por valor en python (correspondencia = correspondencia_l[0])
def RewriteSubW_C1(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (R[0] <= w[1]) and (w[1] < w[0]) and (w[0] < R[1]) ):    # y_jy_i
    correspondencia_l[0][0] = w[1]         # y_i
    correspondencia_l[0][1] = w[0] - 1     # y_{j-1}
    correspondencia_l[0][2] = -(R[1] - 1)  # r_{u+1}-1^{-1}
    correspondencia_detectada = True

  elif ( (R[1] <= w[1]) and (w[1] < w[0]) and (w[0] < R[2]) ):  # y_jy_i
    correspondencia_l[0][0] = w[1]         # y_i
    correspondencia_l[0][1] = w[0] - 1     # y_{j-1}
    correspondencia_l[0][2] = -(R[2] - 1)  # r_{u+1}-1^{-1}
    correspondencia_detectada = True

  return correspondencia_detectada

# Función auxiliar para RewriteSubW - Caso Correspondencia 2
def RewriteSubW_C2(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (R[0] <= w[0]) and (w[0] < w[1]+1) and (w[1]+1 < R[1]) ): # y_iy_{j-1}
    correspondencia_l[0][0] = w[1] + 1     # y_j
    correspondencia_l[0][1] = w[0]         # y_i
    correspondencia_l[0][2] = (R[1] - 1)   # r_{u+1}-1
    correspondencia_detectada = True

  elif ( (R[1] <= w[0]) and (w[0] < w[1]+1) and (w[1]+1 < R[2]) ):# y_iy_{j-1}
    correspondencia_l[0][0] = w[1] + 1     # y_j
    correspondencia_l[0][1] = w[0]         # y_i
    correspondencia_l[0][2] = (R[2] - 1)   # r_{u+1}-1
    correspondencia_detectada = True

  return correspondencia_detectada

# Función auxiliar para RewriteSubW - Caso Correspondencia 3
def RewriteSubW_C3(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (-w[1] + 1 == R[1]) and (R[0] < w[0]+1) and (w[0]+1 < R[1]) ): # y_{j-1}y_{r_{μ+1}-1}^{-1}
    i = random.randint(R[0], w[0])         # R[0] <= i < j
    correspondencia_l[0][0] = -i           # y_i^{-1}
    correspondencia_l[0][1] = w[0] + 1     # y_j
    correspondencia_l[0][2] = i            # y_i
    correspondencia_detectada = True

  elif ( (-w[1] + 1 == R[2]) and (R[1] < w[0]+1) and (w[0]+1 < R[2]) ): # y_{j-1}y_{r_{μ+1}-1}^{-1}
    i = random.randint(R[1], w[0])         # R[1] <= i < j
    correspondencia_l[0][0] = -i           # y_i^{-1}
    correspondencia_l[0][1] = w[0] + 1     # y_j
    correspondencia_l[0][2] = i            # y_i
    correspondencia_detectada = True

  return correspondencia_detectada

# Función auxiliar para RewriteSubW - Caso Correspondencia 4
def RewriteSubW_C4(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (w[1] + 1 == R[1]) and (R[0] <= w[0]) and (w[0] < R[1] - 1) ): # y_iy_{r_{μ+1}-1}
    j = random.randint(w[0] + 1, R[1] - 1) # i < j < R[1]
    correspondencia_l[0][0] = -j           # y_j^{-1}
    correspondencia_l[0][1] = w[0]         # y_i
    correspondencia_l[0][2] = j-1          # y_{j-1}
    correspondencia_detectada = True

  elif ( (w[1] + 1 == R[2]) and (R[1] <= w[0]) and (w[0] < R[2] - 1) ): # y_iy_{r_{μ+1}-1}
    j = random.randint(w[0] + 1, R[2] - 1) # i < j < R[2]
    correspondencia_l[0][0] = -j           # y_j^{-1}
    correspondencia_l[0][1] = w[0]         # y_i
    correspondencia_l[0][2] = j-1          # y_{j-1}
    correspondencia_detectada = True

  return correspondencia_detectada

# Función auxiliar para RewriteSubW - Caso Correspondencia 5
def RewriteSubW_C5(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (R[0] <= -w[0]) and (-w[0] < w[1]) and (w[1] < R[1]) ):   # y_i^{-1}y_j
    correspondencia_l[0][0] = w[1] - 1     # y_{j-1}
    correspondencia_l[0][1] = -(R[1] - 1)  # y_{r_{μ+1}-1}^{-1}
    correspondencia_l[0][2] = w[0]         # y_i^{-1}
    correspondencia_detectada = True

  elif ( (R[1] <= -w[0]) and (-w[0] < w[1]) and (w[1] < R[2]) ):   # y_i^{-1}y_j
    correspondencia_l[0][0] = w[1] - 1     # y_{j-1}
    correspondencia_l[0][1] = -(R[2] - 1)  # y_{r_{μ+1}-1}^{-1}
    correspondencia_l[0][2] = w[0]         # y_i^{-1}
    correspondencia_detectada = True

  return correspondencia_detectada

# Función auxiliar para RewriteSubW - Caso Correspondencia 6
def RewriteSubW_C6(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (R[0] <= w[1]) and (w[1] < -w[0]) and (-w[0] < R[1]) ):   # y_j^{-1}y_i
    correspondencia_l[0][0] = w[1]         # y_i
    correspondencia_l[0][1] = R[1] - 1     # y_{r_{μ+1}-1}
    correspondencia_l[0][2] = w[0] + 1     # y_{j-1}^{-1}
    correspondencia_detectada = True

  elif ( (R[1] <= w[1]) and (w[1] < -w[0]) and (-w[0] < R[2]) ):   # y_j^{-1}y_i
    correspondencia_l[0][0] = w[1]         # y_i
    correspondencia_l[0][1] = R[2] - 1     # y_{r_{μ+1}-1}
    correspondencia_l[0][2] = w[0] + 1     # y_{j-1}^{-1}
    correspondencia_detectada = True

  return correspondencia_detectada

# Función auxiliar para RewriteSubW - Caso Correspondencia 7
def RewriteSubW_C7(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (R[1] == -w[0] + 1) and (R[0] <= -w[1]) and (-w[1] < R[1] - 1) ):   # y_{r_{μ+1}-1}^{-1}y_i^{-1}
    j = random.randint(-w[1] + 1, R[1] - 1) # i < j < R[1]
    correspondencia_l[0][0] = -(j-1)        # y_{j-1}^{-1}
    correspondencia_l[0][1] = w[1]          # y_i^{-1}
    correspondencia_l[0][2] = j             # y_j
    correspondencia_detectada = True

  elif ( (R[2] == -w[0] + 1) and (R[1] <= -w[1]) and (-w[1] < R[2] - 1) ):   # y_{r_{μ+1}-1}^{-1}y_i^{-1}
    j = random.randint(-w[1] + 1, R[2] - 1) # i < j < R[2]
    correspondencia_l[0][0] = -(j-1)        # y_{j-1}^{-1}
    correspondencia_l[0][1] = w[1]          # y_i^{-1}
    correspondencia_l[0][2] = j             # y_j
    correspondencia_detectada = True

  return correspondencia_detectada

# Función auxiliar para RewriteSubW - Caso Correspondencia 8
def RewriteSubW_C8(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (R[1] == w[0] + 1) and (R[0] < -w[1]+1) and (-w[1]+1 < R[1]) ):   # y_{r_{μ+1}-1}y_{j-1}^{-1}
    i = random.randint(R[0], -w[1])        # R[0] <= i < j
    correspondencia_l[0][0] = -i           # y_i^{-1}
    correspondencia_l[0][1] = w[1] - 1     # y_j^{-1}
    correspondencia_l[0][2] = i            # y_i
    correspondencia_detectada = True

  elif ( (R[2] == w[0] + 1) and (R[1] < -w[1]+1) and (-w[1]+1 < R[2]) ):   # y_{r_{μ+1}-1}y_{j-1}^{-1}
    i = random.randint(R[1], -w[1])        # R[1] <= i < j
    correspondencia_l[0][0] = -i           # y_i^{-1}
    correspondencia_l[0][1] = w[1] - 1     # y_j^{-1}
    correspondencia_l[0][2] = i            # y_i
    correspondencia_detectada = True

  return correspondencia_detectada

# Función auxiliar para RewriteSubW - Caso Correspondencia 9
def RewriteSubW_C9(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (R[0] <= -w[1]) and (-w[1] < -w[0]+1) and (-w[0]+1 < R[1]) ):   # y_{j-1}^{-1}y_i^{-1}
    correspondencia_l[0][0] = -(R[1] - 1)  # y_{r_{μ+1}-1}^{-1}
    correspondencia_l[0][1] = w[1]         # y_i^{-1}
    correspondencia_l[0][2] = w[0] - 1     # y_j^{-1}
    correspondencia_detectada = True

  elif ( (R[1] <= -w[1]) and (-w[1] < -w[0]+1) and (-w[0]+1 < R[2]) ):   # y_{j-1}^{-1}y_i^{-1}
    correspondencia_l[0][0] = -(R[2] - 1)  # y_{r_{μ+1}-1}^{-1}
    correspondencia_l[0][1] = w[1]         # y_i^{-1}
    correspondencia_l[0][2] = w[0] - 1     # y_j^{-1}
    correspondencia_detectada = True

  return correspondencia_detectada

# Función auxiliar para RewriteSubW - Caso Correspondencia 10
def RewriteSubW_C10(w, R, correspondencia_l):

  correspondencia_detectada = False

  if ( (R[0] <= -w[0]) and (-w[0] < -w[1]) and (-w[1] < R[1]) ):   # y_i^{-1}y_j^{-1}
    correspondencia_l[0][0] = R[1] - 1     # y_{r_{μ+1}-1}
    correspondencia_l[0][1] = w[1] + 1     # y_{j-1}^{-1}
    correspondencia_l[0][2] = w[0]         # y_i^{-1}
    correspondencia_detectada = True

  elif ( (R[1] <= -w[0]) and (-w[0] < -w[1]) and (-w[1] < R[2]) ):   # y_i^{-1}y_j^{-1}
    correspondencia_l[0][0] = R[2] - 1     # y_{r_{μ+1}-1}
    correspondencia_l[0][1] = w[1] + 1     # y_{j-1}^{-1}
    correspondencia_l[0][2] = w[0]         # y_i^{-1}
    correspondencia_detectada = True

  return correspondencia_detectada

# Devuelve la correspondiente 3-subpalabra para w y la R-Coleccion R
def RewriteSubW(w, R):

  correspondencia = [0, 0, 0]    # Correspondencia a devolver

  if (len(w) != 2):
    return w

  # Correspondencia 1
      # [correspondencia] para simular paso por valor
  if (RewriteSubW_C1(w, R, [correspondencia])):
    pass
  # Correspondencia 2
  elif (RewriteSubW_C2(w, R, [correspondencia])):
    pass
  # Correspondencia 3
  elif (RewriteSubW_C3(w, R, [correspondencia])):
    pass
  # Correspondencia 4
  elif (RewriteSubW_C4(w, R, [correspondencia])):
    pass
  # Correspondencia 5
  elif (RewriteSubW_C5(w, R, [correspondencia])):
    pass
  # Correspondencia 6
  elif (RewriteSubW_C6(w, R, [correspondencia])):
    pass
  # Correspondencia 7
  elif (RewriteSubW_C7(w, R, [correspondencia])):
    pass
  # Correspondencia 8
  elif (RewriteSubW_C8(w, R, [correspondencia])):
    pass
  # Correspondencia 9     # NO LA HE VISTO APLICAR EN WALNUT
  elif (RewriteSubW_C9(w, R, [correspondencia])):
    pass
  # Correspondencia 10
  elif (RewriteSubW_C10(w, R, [correspondencia])):
    pass
  else:
    correspondencia = w

  return correspondencia

# Devuelve la subpalabra tras aplicar conmutación 1 (bibj = bjbi |i-j| > 1)
def RewriteConm1(w):

  correspondencia = [0, 0]    # Correspondencia a devolver

  # Comprobamos si la conmutación 1 es aplicable

  if (len(w) != 2):           # Obligatorio longitud 2 para ser estudiable
    return w

  if (abs(abs(w[0]) - abs(w[1])) > 1):
    correspondencia[0] = w[1]
    correspondencia[1] = w[0]

  else:
    correspondencia = w

  return correspondencia

# Devuelve la subpalabra tras aplicar conmutación 2 (bibi+1bi = bi+1bibi+1)
def RewriteConm2(w):

  correspondencia = [0, 0, 0]    # Correspondencia a devolver

  # Comprobamos si la conmutación 2 es aplicable

  if (len(w) != 3):           # Obligatorio longitud 3 para ser estudiable
    return w

  # Estas condiciones abarcan también inversos de generadores
  if (w[0] == w[2] and (abs(w[0] - w[1]) == 1)):   # bibi+1bi ó bi+1bibi+1
    correspondencia[0] = w[1]               # bi+1 ó bi
    correspondencia[1] = w[0]               # bi   ó bi+1
    correspondencia[2] = w[1]               # bi+1 ó bi

  else:
    correspondencia = w

  return correspondencia

# Expresa una palabra formada por generadores de Artin en el sistema yGen(P)
def ArtinGenToYGen(w, ArtinGen_p):

  w_yGenP = []     # Palabra expresada en el sistema yGen(P)

  # Recorremos la palabra expresada en generadores de Artin
  for i in w:
    if (i > 0):
      w_yGenP.extend(ArtinGen_p[i-1])
    else:
      w_yGenP.extend(InverseWord(ArtinGen_p[-i-1]))

  w_yGenP = ReduccionLibre(w_yGenP)     # Reducimos antes de devolver

  return w_yGenP

# Expresa una palabra formada por generadores de yGen(P) con generadores de
# Artin
def YGenToArtinGen(w, yGen_p):

  w_ArtinGen = []    # Palabra expresada con generadores de Artin

  # Recorremos la palabra expresada en el sistema yGen(P)
  for i in w:
    if (i > 0):
      w_ArtinGen.extend(yGen_p[i-1])
    else:
      w_ArtinGen.extend(InverseWord(yGen_p[-i-1]))


  w_ArtinGen = ReduccionLibre(w_ArtinGen)     # Reducimos antes de devolver

  return w_ArtinGen

# Divide la palabra en bloques de longitud perteneciente al intervalo [a, b]
def DivisionPalabraEnBloques(palabra, a, b):

  bloques = []      # Almacenaremos una lista de bloques
  pos = 0           # Posición actual en la palabra

  #  Recorremos la palabra dando saltos de longitud aleatoria en [a,b]
  while (pos < len(palabra)):

    i = random.randint(a,b)   # Longitud del bloque actual (aleatoria en [a,b])
    bloque_aux = palabra[pos:pos+i]   # Bloque actual a añadir
    bloques.append(bloque_aux)        # Añadimos bloque actual
    pos += i                  # Nos posicionamos al final del último bloque

  return bloques

def AplicarSRelP(bloques, regla=0):

  nuevos_bloques = []   # Nueva lista de bloques para no sobreescribir

  # Se trata de aplicar Conmutador 1
  if (regla == 1):
    # Recorremos los bloques
    for bloque in bloques:
      bloque_copy = bloque.copy()   # Copiamos bloques para no sobreescribir
      # Extraemos 2-subpalabra y pos_ini
      subpalabra = ExtraeSubPalabra(bloque_copy, 2)

      # Si ha tenido éxito la extracción
      if (subpalabra[1] != -1):
        correspondencia = RewriteConm1(subpalabra[0])

        # Eliminamos subpalabra extraída
        del bloque_copy[subpalabra[1]:subpalabra[1]+2]

        # Añadimos su correspondencia en su lugar para completar sustitución
        for i in reversed(correspondencia):
          bloque_copy.insert(subpalabra[1], i)

      # Añadimos bloque modificado a nueva lista de bloques
      nuevos_bloques.append(bloque_copy)

  # Se trata de aplicar Conmutador 2
  elif (regla == 2):
    # Recorremos los bloques
    for bloque in bloques:
      bloque_copy = bloque.copy()   # Copiamos bloques para no sobreescribir
      # Extraemos 2-subpalabra y pos_ini
      subpalabra = ExtraeSubPalabra(bloque_copy, 3)

      # Si ha tenido éxito la extracción
      if (subpalabra[1] != -1):
        correspondencia = RewriteConm2(subpalabra[0])
        # Eliminamos subpalabra extraída
        del bloque_copy[subpalabra[1]:subpalabra[1]+3]

        # Añadimos su correspondencia en su lugar para completar sustitución
        for i in reversed(correspondencia):
          bloque_copy.insert(subpalabra[1], i)

      # Añadimos bloque modificado a nueva lista de bloques
      nuevos_bloques.append(bloque_copy)

  # Se trata de SRel(P)
  else:
    # Recorremos los bloques
    for bloque in bloques:
      bloque_copy = bloque.copy()   # Copiamos bloques para no sobreescribir
      # Extraemos 2-subpalabra y pos_ini
      subpalabra = ExtraeSubPalabra(bloque_copy, 2)

      # Si ha tenido éxito la extracción
      if (subpalabra[1] != -1):
        correspondencia = RewriteSubW(subpalabra[0], R) # Aplicamos SRel(P)
        # Eliminamos subpalabra extraída
        del bloque_copy[subpalabra[1]:subpalabra[1]+2]

        # Añadimos su correspondencia en su lugar para completar sustitución
        for i in reversed(correspondencia):
          bloque_copy.insert(subpalabra[1], i)

      # Añadimos bloque modificado a nueva lista de bloques
      nuevos_bloques.append(bloque_copy)

  return nuevos_bloques

# Extrae aleatoriamente de 'palabra' una subpalabra de longitud 'l'
# Además de la subpalabra devuelve su posición inicial para una posterior
# substitución (o palabra y -1 en caso de no conseguir extraer la subpalabra)
def ExtraeSubPalabra(palabra, l):

  # Se necesita que len(palabra >= l)
  if (len(palabra) < l):
    return palabra, -1

  else:
    # Posición inicial de subpalabra aleatoria en [0, finalPalabra - l]
    inicio_subP = random.randint(0, len(palabra) - l)
    sub_palabra = palabra[inicio_subP:inicio_subP + l]

    return sub_palabra, inicio_subP

# Concatena los bloques modificados para construir una nueva palabra, a la que
# posteriormente se trata de aplicar reducción libre
def ConcatenarYRLibre(bloques_modificados):

  # Concatenar bloques para formar nueva palabra
  palabra_reescrita = []
  [palabra_reescrita.extend(bloque) for bloque in bloques_modificados]

  # Se trata de aplicar Reducción Libre
  palabra_reescrita = ReduccionLibre(palabra_reescrita)

  return palabra_reescrita

# Reescribe una palabra 'w' mediante el Algoritmo de Reescritura Estocástico
# ocultando la palabra original
def StochasticRewriting(w_ArtinGen, ArtinGen_p, yGen_p):

  # Se expresa w en el sistema yGen(P)
  w_yGen = ArtinGenToYGen(w_ArtinGen, ArtinGen_p)
  w_final = w_yGen

  # Repetimos el proceso lo suficiente para ocultar la palabra original
  for i in range(3):

    # Se divide en bloques
    bloques_w_yGen = DivisionPalabraEnBloques(w_yGen, 5,10)

    # Extrae una 2-subpalabra para cada bloque y la sustituye por su
    # correspondencia en SRel(P), si es posible
    bloques_SRelP = AplicarSRelP(bloques_w_yGen)

    # Se concatenan los nuevos bloques y se trata de aplicar Reducción Libre a la
    # nueva palabra
    w_yGen = ConcatenarYRLibre(bloques_SRelP)

  # Se expresa la palabra final en términos de generadores de Artin
  w_ArtinGen = YGenToArtinGen(w_yGen, yGen_p)
  w_ArtinGen = ReduccionLibre(w_ArtinGen)   # Reducimos palabra

  # PRIMERA CONMUTACIÓN
  for i in range(3):

    bloques_w_ArtinGen = DivisionPalabraEnBloques(w_ArtinGen, 5,10)

    # Extrae una 2-subpalabra para cada bloque y la trata de conmutar
    bloques_Conm1 = AplicarSRelP(bloques_w_ArtinGen, 1)

    # Se concatenan los nuevos bloques y se trata de aplicar Reducción Libre a la
    # nueva palabra
    w_ArtinGen = ConcatenarYRLibre(bloques_Conm1)

  # SEGUNDA CONMUTACIÓN
  for i in range(3):

    bloques_w_ArtinGen = DivisionPalabraEnBloques(w_ArtinGen, 5,10)

    # Extrae una 3-subpalabra para cada bloque y la trata de conmutar
    bloques_Conm2 = AplicarSRelP(bloques_w_ArtinGen, 2)

    # Se concatenan los nuevos bloques y se trata de aplicar Reducción Libre a la
    # nueva palabra
    w_ArtinGen = ConcatenarYRLibre(bloques_Conm2)

  w_final = ReduccionLibre(w_ArtinGen)   # Reducimos palabra

  return w_final




# Elegimos partición P(8)
particion = [3,4]
print("¿La partición elegida es adecuada?", ComprobadorParticion(7, particion))

"""Se sigue definiendo una colección $R = \{r_1, r_2, ..., r_{l+1}\}$ ($r_1 = 1, \:\:r_i = r_{i-1} + p_{i-1}$), en nuestro caso $R_{\mathcal{P(7)}} = \{r_1, r_2, r_3\}$:


*   $ r_1 = 1 $
*   $ r_2 = r_1 + p_1 = 4 $
*   $ r_3 = r_2 + p_2 = 8 $
"""

R = GeneradorSecuenciaRParticion(particion)
print("La secuencia de valores R generadores a partir de", particion, "es:\nR =",
      R)

"""Esta colección nos permite definir $yGen(\mathcal{P})$, el nuevo conjunto de generadores:

*   $y_1 = b_1b_2 \cdots  b_{r_2-1}$
*   $y_2 = b_2 \cdots b_{r_2-1}$
*   $\cdots$
*   $y_{r_2-1} = b_{r_2-1}$
*   $y_{r_2} = b_{r_2}b_{r_2+1} \cdots b_{r_3-1}$
*   $y_{r_2+1} = b_{r_2+1} \cdots b_{r_3-1}$
*   $\cdots$
*   $y_{r_3-1} = b_{r_3-1}$
*   $y_{r_3} = b_{r_3}b_{r_3+1} \cdots b_{r_4-1}$
*   $\cdots$
*   $y_{r_{l+1}-1} = y_{N-1} = b_{r_{l+1}-1} = b_{N-1}$

Para nuestra partición $\mathcal{P(7)}$:

*   $y_1 = b_1b_2b_3$
*   $y_2 = b_2b_3$
*   $y_3 = b_3$
*   $y_4 = b_4b_5b_6b_7$
*   $y_5 = b_5b_6b_7$
*   $y_6 = b_6b_7$
*   $y_7 = b_7$

Implementemos la colección de generadores como trenzas:
"""

# Colección de palabras que representan los yGeneradores(P(8))
y1_p = [1,2,3]
y2_p = [2,3]
y3_p = [3]
y4_p = [4,5,6,7]
y5_p = [5,6,7]
y6_p = [6,7]
y7_p = [7]
yGen_p = [y1_p, y2_p, y3_p, y4_p, y5_p, y6_p, y7_p]

# Colección de yGeneradores(P(8))
y1 = Braid(8, yGen_p[0])
y2 = Braid(8, yGen_p[1])
y3 = Braid(8, yGen_p[2])
y4 = Braid(8, yGen_p[3])
y5 = Braid(8, yGen_p[4])
y6 = Braid(8, yGen_p[5])
y7 = Braid(8, yGen_p[6])
yGen = [y1, y2, y3, y4, y5, y6, y7]

print("Colección de y-Generadores:")
for i in range(7):
  print("y{} = {}".format(i+1, yGen[i].showBraid()))

"""Nos será útil expresar los generadores de Artin en el nuevo sistema implmentado, permitiendo así también fácilmente el paso de generadores de Artin al nuevo sistema:

*   $b_1 = y_1y_2^{-1}$
*   $b_2 = y_2y_3^{-1}$
*   $b_3 = y_3$
*   $b_4 = y_4y_5^{-1}$
*   $b_5 = y_5y_6^{-1}$
*   $b_6 = y_6y_7^{-1}$
*   $b_7 = y_7$

Implementemos la colección de generadores como palabras:
"""

# Generadores de Artin en función del nuevo sistema de generadores
b1_yp = [1, -2]
b2_yp = [2, -3]
b3_yp = [3]
b4_yp = [4, -5]
b5_yp = [5, -6]
b6_yp = [6, -7]
b7_yp = [7]
ArtinGen_p = [b1_yp, b2_yp, b3_yp, b4_yp, b5_yp, b6_yp, b7_yp]
print("Colección de generadores de Artin expresados en el nuevo sistema:")
for i in range(7):
  print("y{} = {}".format(i+1, ArtinGen_p[i]))

"""El siguiente paso es dominar la detección de la relación emergente de la nueva representación:
$$y_jy_i = y_iy_{j-1}y_{r_{μ+1}-1}^{-1}, \:\:\:\: r_\mu \leq i < j < r_{\mu+1}, \:\: \mu \in \{1, ..., l\}  $$

El algoritmo estocástico de reescritura deberá detectar cuándo es aplicable esta relación. Para ello, seleccionará algunas potenciales subpalabras $u$ de longitud 2, de forma que si en la relación (una de sus representaciones) se admite el caso $LuR = 1$, se sustituirá $u$ por $L^{-1}R^{-1}$.
"""

if __name__ == "__main__":

  subpalabra = [-3, -3, -2, -1]
  print(subpalabra)
  correspondencia = RewriteSubW(subpalabra, R)
  print(correspondencia)

  """A esta relación emergente (ya dominada) de la nueva representación, hay que sumarle las 2 relaciones definitorias del grupo trenzado:

  $$ σ_{i}σ_{i+1}σ_{i} = σ_{i+1}σ_{i}σ_{i+1} $$
  $$ σ_{i}σ_{j} = σ_{j}σ_{i}, \ |i-j| > 1;  $$

  Ambas relaciones se añadirán a la ya implementada emergente, aunque estas se aplicarán tras completar la reescritura sobre el sistema $yGen(\mathcal{P})$, una vez vuelto a los generadores de Artin. Esto se propone así debido a que no obtenemos ninguna ganancia por intentar detectar estas dos relaciones reescritas en el nuevo sistema, mientras que su implementación sí que aumentaría en dificultad.

  Implementamos sus métodos de detección y reescritura:
  """



  print("Ejemplos de correspondecias a la 2-subpalabras:\n")
  subpalabra1 = [2, 4]
  print("Subpalabra 1:", subpalabra1)
  correspondencia1 = RewriteConm1(subpalabra1)
  print("Correspondencia 1:", correspondencia1)

  subpalabra2 = [-2, -3, -2]
  print("Subpalabra 2:", subpalabra2)
  correspondencia2 = RewriteConm2(subpalabra2)
  print("Correspondencia 2:", correspondencia2)

  """Una vez implementados tanto el nuevo sistema generador como la detección de las 2-subpalabras susceptibles de ser aplicadas por la relación
  $$y_jy_i = y_iy_{j-1}y_{r_{μ+1}-1}^{-1}, \:\:\:\: r_\mu \leq i < j < r_{\mu+1}, \:\: \mu \in \{1, ..., l\},  $$
  y sus equivalencias, podemos implementar el algoritmo estocástico de escritura.

  Se siguen secuencialmente los siguientes pasos para reescribir una palabra $w$:

  1.   Se expresa $w$ en el sistema $yGen(\mathcal{P})$, $w ⟼ w_{yGen(\mathcal{P})}$
  2.   Se divide $w_{yGen(\mathcal{P})}$ en bloques $Block_1, Block_2, ..., Block_k$, con $5 \leq length(Block_i) \leq 10$  
  3.   Para cada $Block_i$, se elige una 2-subpalabra $u_i$
  4.   Para cada 2-subpalabra $u_i$, se trata de aplicar alguna relación $SRel(\mathcal(P))$, intercambiándose por su correspondencia si es posible y, manteniéndose invariante $u_i$, en caso de que no.
  5.   Se concantenan los nuevos bloques modificados y se aplica reducción libre en el sistema $yGen(\mathcal{P})$.
  6.   Se repite la secuencia de pasos 2-5 lo necesario, expresando la palabra final $w_{yGen(\mathcal{P})}'$ final en generadores de Artin, $w_{yGen(\mathcal{P})}' ⟼ w'$
  7.  Se repiten los pasos 2-5 en el sistema de generadores de Artin, tratando de aplicar la primera conmutación a 2-subpalabras
  8. Se repiten los pasos 2-5 en el sistema de generadores de Artin, tratando de aplicar la primera conmutación a 3-subpalabras

  **Conversión del sistema generador**
  """



  print("CONVERSIÓN: Generadores de Artin --> yGen(P)")
  print("\nGenedores de Artin expresados en el sistema yGen(P)")
  for i in range(7):
    print("Generador de Artin {} --> Generadores yGen(P) {}".format(i+1,
                                  ArtinGenToYGen([i+1], ArtinGen_p)))
  w = [1,-2,7,4,5]
  print("\nPalabra en generadores de Artin:", w)
  print("w expresada en el sistema yGen(P)", ArtinGenToYGen(w, ArtinGen_p))

  print("\n\nCONVERSIÓN: yGen(P) --> Generadores de Artin ")
  print("\nGenedores del sistema yGen(P) expresados con generadores de Artin")
  for i in range(7):
    print("Generador del sistema yGen(P)  {} --> Generadores de Artin {}".format(
        i+1, YGenToArtinGen([i+1], yGen_p)))
  w = [-3,-2]
  print("\nPalabra expresada en el sistema yGen(P):", w)
  print("w en generadores de Artin ", YGenToArtinGen(w, yGen_p))

  print("\nComprobamos que ambas funciones actúan como inversas recíprocamente,\
  (aplicando posteriormente reducción libre):")
  print("Artin --> YGen(P) --> Artin (R.Libre)   -->",
        ReduccionLibre(ArtinGenToYGen(YGenToArtinGen(w, yGen_p), ArtinGen_p)))
  print("YGen(P) --> Artin --> YGen(P) (R.Libre) -->",
        ReduccionLibre(YGenToArtinGen(ArtinGenToYGen(w, ArtinGen_p), yGen_p)))

  """**División de $w_{yGen(\mathcal{P})}$ en bloques**"""



  palabra_sin_dividir = list(range(20,0, -1))
  palabra_en_bloques = DivisionPalabraEnBloques(palabra_sin_dividir, 5,10)
  print("Palabra original:", palabra_sin_dividir)
  print("Palabra dividida en bloques de longitud en [5,10]:", palabra_en_bloques)

  """**Extracción aleatoria de 2-subpalabra por bloque**"""



  palabra_inicial = [1, -1, 2, 7, -4, 5]
  longitud = 2
  palabra_extraida = ExtraeSubPalabra(palabra_inicial, longitud)
  print("Palabra inicial:", palabra_inicial)
  print("Palabra extraida de longitud {}: {}".format(longitud,
                                                    palabra_extraida[0]))
  print("Posición inIcial de la palabra extraída:", palabra_extraida[1])

  """**Aplicación de $SRel(\mathcal(P))$**"""

  # Recorre los bloques que dividen la palabra, extrae para cada uno una
  # 2-subpalabra, trata de aplicar S(Rel(P)), Conmutación1 o Conmutación 2 y, en
  # caso éxito, sustituye dentro del bloque la 2-subpalabra por su correspondencia
    # Si regla == 1 --> Se trata de aplicar la primera conmutación bibj = bjbi
    # Si regla == 2 --> Se trata de aplicar la segunda conmutación bibi+1bi = bi+1bibi+1
    # Por defecto   --> Se trata de aplicar S(Rel(P))

  palabra_sin_dividir = list(range(7,0, -1)) + list(range(7, 0, -1))
  palabra_en_bloques = DivisionPalabraEnBloques(palabra_sin_dividir, 5, 10)
  print("Palabra dividida en bloques sin aplicar SRel(P) a 2-subpalabras:\n",
        palabra_en_bloques)
  bloques_SRelP = AplicarSRelP(palabra_en_bloques)
  print("\nPalabra dividida en bloques tras aplicar SRel(P) a 2-subpalabras:\n",
        bloques_SRelP)

  palabra_sin_dividir1 = [1,-7]
  palabra_en_bloques1 = DivisionPalabraEnBloques(palabra_sin_dividir1, 5, 10)
  print("\nPalabra dividida en bloques sin aplicar Conmutador1 a 2-subpalabras:\n",
        palabra_en_bloques1)
  bloques_Conm1 = AplicarSRelP(palabra_en_bloques1,1)
  print("\nPalabra dividida en bloques tras aplicar Conmutador1 a 2-subpalabras:\n",
        bloques_Conm1)

  palabra_sin_dividir2 = [-1,-2,-1]
  palabra_en_bloques2 = DivisionPalabraEnBloques(palabra_sin_dividir2, 5, 10)
  print("\nPalabra dividida en bloques sin aplicar Conmutador2 a 3-subpalabras:\n",
        palabra_en_bloques2)
  bloques_Conm2 = AplicarSRelP(palabra_en_bloques2,2)
  print("\nPalabra dividida en bloques tras aplicar Conmutador2 a 3-subpalabras:\n",
        bloques_Conm2)

  """**Concatenación y Reducción Libre de bloques modificados**"""



  print("Palabra dividida en bloques tras aplicar SRel(P) a 2-subpalabras:\n",
        bloques_SRelP)

  palabra_reescrita = ConcatenarYRLibre(bloques_SRelP)
  print("\nSe concatenan los bloques y se reduce libremente la palabra\
  reescrita:\n", palabra_reescrita)

  palabra = [7,-7,-6,-5]
  palabray= ArtinGenToYGen(palabra, ArtinGen_p)
  print(palabray)
  RewriteSubW(palabray, R)

  """**ALGORITMO DE REESCRITURA ESTOCÁSTICO**"""



  import random

  # Generaramos una palabra aleatoria de longitud 100
  #palabra_original = ReduccionLibre([random.choice([-7, -6, -5, -4, -3, -2, -1, 1,
                                        #2, 3, 4, 5, 6, 7]) for _ in range(100)])
  palabra_original = [-1, -2, -1]
  print("Palabra original:", palabra_original)
  print("Longitud palabra original:", len(palabra_original))
  palabra_reescrita = StochasticRewriting(palabra_original, ArtinGen_p, yGen_p)
  print("Palabra reescrita por Algoritmo Estocástico:", palabra_reescrita)
  print("Longitud palabra reescrita:", len(palabra_reescrita))

  print("¿SE HA APLICADO ALGÚN CAMBIO?", palabra_original != palabra_reescrita)

