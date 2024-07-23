## Protocolo Conmutador - Anshel and Goldfeld
"""
Se comienza fijando un grupo trenzado $\mathbb{B}_N$ y dos subgrupos públicos , de la forma

\begin{align*}
	& S = < s_1, ..., s_{n_1}> \; \subseteq \mathbb{B}_N\\
	& T = < t_1, ..., t_{n_2}> \; \subseteq \mathbb{B}_N,
\end{align*}

correspondiendo a las partes de la comunicación $A$ y $B$, respectivamente.
"""
from braid import *

"""Cada parte debe generar una trenza secreta perteneciente a su subgrupo público correspondiente (utilizando solo generadores positivos):


1.   Secreto A: $a = s_{i_1}, ..., s_{i_{k_1}}$
2.   Secreto B: $b = t_{i_1}, ..., t_{i_{k_2}}$

Para ello, se ha implementado el método "GeneradorSecretoProtocolo(generadores_permitidos, longitud_max)", que genera aleatoriamente una palabra a partir de los generadores pasados por parámetros, y con una longitud entre longitud_max // 2 y longitud_max.
"""

import random

def GeneradorSecretoProtocolo(generadores_subgrupo, longitud_max, permiteInv):
  """
  Genera una cadena de enteros con valoreen generadores_subgrupo y
  con longitud máxima longitud_max.

  Args:
    generadores_subgrupo: Lista de enteros (en valor absoluto) permitidos.
    longitud_max: Longitud máxima de la cadena.
    permiteInv: Variable booleana que indica si te utilizan generadores inversos

  Returns:
    Una cadena de enteros que cumple con las condiciones especificadas.
  """

  # Generamos una lista con los posibles valores (positivos y negativos)
  posibles_valores = []
  for valor in generadores_subgrupo:
    posibles_valores.append(valor)
    if (permiteInv):
      posibles_valores.append(-valor)

  # Generamos una cadena aleatoria con los posibles valores
  longitud = random.randint(longitud_max//2, longitud_max)
  cadena = random.choices(posibles_valores, k=longitud)

  return cadena

def calcular_secreto_compartido(secreto, conjunto_pares):
  """
  Calcula el secreto compartido a partir de una palabra secreto y un set
  conjunto_pares que mapea generadores a palabras.

  Args:
    secreto: Trenza que representa el secreto de la parte en cuestión
    conjunto_pares: Un set que mapea generadores (enteros) a palabras
    (listas de enteros).

  Returns:
    Una lista de enteros representando el secreto compartido.
  """
  secreto_compartido = []   # Palabra donde almacenar secreto compartido
  palabra = secreto.elementos  # Palabra del secreto

  # Se iteran los generadores del secreto
  for gen in palabra:
    # Se busca cada generador en el set, concatenando su conjugado asociado
    if gen in conjunto_pares:
      secreto_compartido += conjunto_pares[gen]

  # Último elemento del secreto
  secreto_compartido += secreto.inverseBraid().elementos

  return secreto_compartido

if __name__ == "__main__":


  # grado del grupo trenzado sobre el que construir el protocolo
  N = 8

  # índices de los generadores de los subgrupos públicos
  S = {1, 3, 5, 7}  # subgrupo asociado a la parte A
  T = {2, 4, 6}     # subgrupo asociado a la parte B


  # Ejemplo de uso
  generadores_subgrupo = [2, 3, 4, 5]
  longitud_max = 30

  cadena_generada = GeneradorSecretoProtocolo(generadores_subgrupo, longitud_max,
    False)
  print(cadena_generada)

  """Una vez implementado "GeneradorSecretoProtocolo", lo empleamos para generar el par de secretos $secreto_a$ y $secreto_b$ asociados a las partes $A$ y $B$, respectivmente,"""

  # Generación de secretos para cada parte
  secreto_a = Braid(N, GeneradorSecretoProtocolo(S, 20, False))
  secreto_b = Braid(N, GeneradorSecretoProtocolo(T, 20, False))

  print("Secreto a:", secreto_a.showBraid())
  print("Secreto b:", secreto_b.showBraid())

  """El siguiente paso del protocolo es computar los siguientes conjuntos de pares, de nuevo uno por parte implicada en la comunicación:


  1.   Conjunto de pares de A: $Pares_A = \{(t_1, at_1a^{-1}), ..., (t_n, at_na^{-1})\}$
  2.   Conjunto de pares de B: $Pares_B = \{(s_1, bs_1b^{-1}), ..., (s_n, bs_nb^{-1})\}$


  """

  # Inicializamos una lista vacía para almacenar los mensajes
  Pares_A = {}
  Pares_B = {}

  # La parte A computa su conjunto de partes, conjungando cada generador del
  # subgrupo público de B por su secreto a
  for gen in T:
    #aux = [gen, secreto_a.elementos + [gen] + secreto_a.inverseBraid().elementos]
    #Pares_A.add(aux)  # Agregamos el par al conjunto de pares de A
    Pares_A [gen] = secreto_a.elementos + [gen] + secreto_a.inverseBraid().elementos

  # La parte B computa su conjunto de partes, conjungando cada generador del
  # subgrupo público de A por su secreto b
  for gen in S:
    #aux = [gen, secreto_b.elementos + [gen] + secreto_b.inverseBraid().elementos]
    #Pares_B.append(aux)  # Agregamos el par al conjunto de pares de B
    Pares_B [gen] = secreto_b.elementos + [gen] + secreto_b.inverseBraid().elementos


  # Ahora la lista 'mensajes' contiene todos los pares [gen, sec + gen + sec^{-1}]
  print("Conjunto de pares de A:", Pares_A)
  print("Conjunto de pares de B:", Pares_B)

  """A continuación, las partes se intercambian sus conjuntos de partes, y cada una concluye computando el secreto compartido, el cual se obtiene escogiendo los pares que se corresponden con los generadores que forman su secreto, de la siguiente forma:


  1.   Secreto Compartido A: $SecretoCompartidoA = (bs_{i_1}b^{-1}), ..., (bs_{i_1}b^{-1})a^{-1}$
  2.   Secreto Compartido B: $SecretoCompartidoB = ((as_{i_1}a^{-1}), ..., (as_{i_1}a^{-1})b^{-1})^{-1}$

  Fácilmente se ve que:
  $$SecretoCompartidoA = bab^{-1}a^{-1} = (aba^{-1}b^{-1})^{-1} = SecretoCompartidoB$$
  """

  # prompt: implementa un método con los siguientes parámetros: P1 palabra formada por generadores P2 conjunto clave valor donde cada generaodr tiene una palabra asignada



  # Ejemplo de uso
  P1 = Braid(N, [2, 4, 6])
  P2 = {2: [1, 2, 3], 4: [4, 5, 6], 6: [7, 8, 9]}

  secreto_compartido = calcular_secreto_compartido(P1, P2)
  print(secreto_compartido)  # Salida: [1, 2, 3, -6, -5, -4, 7, 8, 9]

  """Computemos utilizando el método "calcular_secreto_compartido" el secreto compartido asociado a cada parte, comprando finalmente que ambas partes cuentan con el mismo secreto.


  """

  # Secretos compartidos computados por cada parte
  Secreto_Compartido_A = Braid(N, ReduccionLibre(calcular_secreto_compartido(secreto_a, Pares_B)))
  Secreto_Compartido_B = Braid(N, ReduccionLibre(calcular_secreto_compartido(secreto_b, Pares_A))).inverseBraid()

  print("Secreto compartido computado por parte A:", Secreto_Compartido_A.elementos)
  print("Secreto compartido computado por parte B:", Secreto_Compartido_B.elementos)

  print("¿Han llegado ambas partes al mismo secreto compartido?:",
        Secreto_Compartido_A.elementos == Secreto_Compartido_B.elementos)
