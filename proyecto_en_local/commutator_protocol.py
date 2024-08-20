
from braid import *
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

  # DATOS DEL PROTOCOLO

  print("\nDATOS PÚBLICOS DEL PROTOCOLO:\n")

  # grado del grupo trenzado sobre el que construir el protocolo
  N = 8

  # índices de los generadores de los subgrupos públicos
  S = {1, 3, 5, 7}  # subgrupo asociado a la parte A
  T = {2, 4, 6}     # subgrupo asociado a la parte B

  print("Grado del grupo trenzado elegido:", N)
  print("Generadores del subgrupo acordado para la parte A:", S)
  print("Generadores del subgrupo acordado para la parte B:", T)

  # Generación de secretos para cada parte
  secreto_a = Braid(N, GeneradorSecretoProtocolo(S, 20, False))
  secreto_b = Braid(N, GeneradorSecretoProtocolo(T, 20, False))

  print("\nSECRETOS DE CADA PARTE:\n")
  print("Secreto generado para la parte A:", secreto_a.showBraid())
  print("Secreto generado para la parte B:", secreto_b.showBraid())

  # COMPUTACIÓN DE LOS CONJUNTOS DE PARES A INTERCAMBIAR

  print("\nCOMPUTACIÓN DE LOS CONJUNTOS DE PARES A INTERCAMBIAR:\n")

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
  print("Conjunto de pares de A, que enviará a B:", Pares_A)
  print("Conjunto de pares de B, que enviará a A:", Pares_B)


  # COMPUTACIÓN DEL SECRETO COMPARTIDO TRAS EL INTERCAMBIO DE LOS CONJUNTOS DE PARES

  print("\nCOMPUTACIÓN DEL SECRETO COMPARTIDO TRAS EL INTERCAMBIO DE LOS CONJUNTOS DE PARES:\n")

  # Secretos compartidos computados por cada parte
  Secreto_Compartido_A = Braid(N, ReduccionLibre(calcular_secreto_compartido(secreto_a, Pares_B)))
  Secreto_Compartido_B = Braid(N, ReduccionLibre(calcular_secreto_compartido(secreto_b, Pares_A))).inverseBraid()

  print("Secreto compartido computado por parte A:", Secreto_Compartido_A.elementos)
  print("Secreto compartido computado por parte B:", Secreto_Compartido_B.elementos)

  print("¿Han llegado ambas partes al mismo secreto compartido?:",
        Secreto_Compartido_A.elementos == Secreto_Compartido_B.elementos, "\n")
