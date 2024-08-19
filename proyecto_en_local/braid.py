# TRENZAS


from permutation import *
#from sympy.combinatorics import Permutation

# Clase que representará a las trenzas
class Braid:

  # Constructor
  def __init__(self, grado = 1, elementos = []):
    if (elementos == []):
      self.grado = grado          # Grado del grupo al que pertenecen
      self.elementos = elementos  # Palabra que representa a la trenza
      self.perm = Permutation(0)  # Permutación identidad

    # En cualquier momento una trenza que fue definida para el grupo i-ésimo
    # podrá utilizarse como trenza del grupo j-ésimo, para i < j,
    # actualizándose el grupo (atributo grado) al que pertenece. Este
    # comportamiento se da en su propia definición, como ocurre justo aquí
    else:
      self.grado = grado if grado > max(abs(x) for x in elementos) + 1\
                        else max(abs(x) for x in elementos) + 1
      self.elementos = elementos
      self.perm = ProyectarSn(elementos, grado)  # proyección de la trenza sobre Sn

  # Visualizamos las trenzas con el formato [g1, g2, g3]
  def showBraid(self):
    indices = [str(self.elementos[i]) for i in range(len(self.elementos))]
    palabra  = "[" + " ".join(indices) + "]"
    return palabra

  # Concatenamos 2 trenzas (operación del grupo trenzado)
  def concatenateBraid(self, trenza):

    resultado = Braid()

    # Permitimos multiplicar 2 trenzas pertenecientes a grupos de distinto
    # orden, simplemente incluimos el resultado en el grupo de orden mayor
    # (los generadores del grupo menor pertenecen al grupo mayor)
    resultado.grado = self.grado if self.grado > trenza.grado else trenza.grado

    # Concatenamos generadores de ambas trenzas
    resultado.elementos = self.elementos + trenza.elementos

    # Multiplicamos sus permutaciones asociadas
    resultado.perm = self.perm * trenza.perm

    return resultado

  # Calculamos la trenza inversa
  def inverseBraid(self):

    #elementos_invertidos = [-elem for elem in reversed(self.elementos)]
    elementos_invertidos = InverseWord(self.elementos)
    trenza_inversa = Braid(self.grado, elementos_invertidos)

    return trenza_inversa

  # Reducimos la trenza (se eliminan gen*gen^(-1))
  def ReduccionLibre(self):

    i = 0
    while i < len(self.elementos) - 1:
      # Si dos consecutivos son opuestos
      if self.elementos[i] == -self.elementos[i + 1]:
          del self.elementos[i:i+2]   # Se eliminan gen*gen^(-1)
          i -= 1                      # Han podido generarse nuevos gen*gen^(-1)
      else:
          i += 1

  # Calcula una representación (palabra) de la trenza fundamental del grupo
  # trenzando n-ésimo (n pasado por parámetro) tomando el generador i-esimo
  # como primer cruce
  @classmethod
  def TrenzaFundamental(cls, n, i=1):
    trenzaFundamental = []
    aux1 = []
    aux2 = []

    # Primera parte --> (ri)(ri+1 ri)...(rn-1 ... ri)
    for it in range(i, n):
      aux1 = [it] + aux1
      trenzaFundamental = trenzaFundamental + aux1
      aux2 = aux1

    # Segunda parte --> (ri-1 ... rn-1)...(r1 ... rn-1)
    aux1 = list(range(i-1, n))
    for it in range(i-1):
      trenzaFundamental = trenzaFundamental + aux1
      aux2 = [i - (it + 2)] # Elemento que añadimos para la siguiente subpalabra
      aux1 = aux2 + aux1

    return trenzaFundamental

# Método auxiliar (fuera de la clase Braid) para la calcular la palabra
# representante de la trenza (representanda por 'palabra') inversa
def InverseWord(palabra):

    # Invertimos orden de la palabra y calculamos el opuesto de cada elemento
    elementos_invertidos = [-elem for elem in reversed(palabra)]
    return elementos_invertidos


# Método auxiliar para proyectar una trenza sobre Sn
def ProyectarSn(palabra, grado):

  proyeccion = Permutation(0)
  # Necesaria para no perder las colas de elementos invariantes tras aplicarla
  perm_identity = Permutation(range(grado))

  # Recorremos los generadores que forman la palabra
  for i in reversed(palabra):
    # Permutación que describe los cruces ri y ri^-1
    perm_aux = Permutation(abs(i)-1, abs(i))
    proyeccion = proyeccion * perm_aux

  proyeccion = proyeccion * perm_identity

  return proyeccion

# Método auxiliar para aplicar la reducción libre a una palabra
def ReduccionLibre(palabra):

  i = 0
  while i < len(palabra) - 1:
    if palabra[i] == -palabra[i + 1]: # Si dos consecutivos son opuestos
        del palabra[i:i+2]            # Se eliminan gen*gen^(-1)
        i = i - 2 if i >= 2 else 0    # Han podido generarse nuevos gen*gen^(-1)
    else:
        i += 1
  return palabra


if __name__ == "__main__":

  print("\nOPERACIONES BÁSICAS CON TRENZAS:\n")

  # Ejemplos de construcción, concatenación y visualización
  trenza = Braid(5, [-8, 1,2,3])
  print("Trenza 1:", trenza.showBraid(), "--> Grado:", trenza.grado)

  trenza2 = Braid(elementos = [1,-2, -6])
  print("Trenza 2:", trenza2.showBraid(), "--> Grado:", trenza2.grado)

  trenza_concatenada = trenza.concatenateBraid(trenza2)
  print("\nTrenza concantenada:", trenza_concatenada.showBraid(), "--> Grado:",
        trenza_concatenada.grado)

  trenza_sin_inversion = Braid(5, [2, -3, 2, 1])
  print("\nTrenza sin invertir:", trenza_sin_inversion.elementos)
  trenza_inversa = trenza_sin_inversion.inverseBraid()
  print("Trenza invertida:", trenza_inversa.elementos)

  print("\nPERMUTACIONES ASOCIADAS")
  print("\nPermutación de la trenza 1:", trenza.perm)
  print("Permutación de la trenza 2:", trenza2.perm)
  print("Permutación de la trenza concantenada:", trenza_concatenada.perm)

  print("\nTRENZAS FUNDAMENTALES:\n")  
  trenzaFundamental_4_1 = Braid(10, Braid.TrenzaFundamental(4, 1))
  print("Trenza fundamental de grado 4 (\"pivotando\" desde el generador 1):")
  print(trenzaFundamental_4_1.showBraid())

  trenzaFundamental_4_2 = Braid(10, Braid.TrenzaFundamental(4, 2))
  print("\nTrenza fundamental de grado 4 (\"pivotando\" desde el generador 2):")
  print(trenzaFundamental_4_2.showBraid())

  trenzaFundamental_4_3 = Braid(10, Braid.TrenzaFundamental(4, 3))
  print("\nTrenza fundamental de grado 4 (\"pivotando\" desde el generador 3):")
  print(trenzaFundamental_4_3.showBraid())

  # Trenzas fundamentales de grado 10
  trenzaFundamental_10_5 = Braid(10, Braid.TrenzaFundamental(10, 5))
  print("\nTrenza fundamental de grado 10 (\"pivotando\" desde el generador 5):")
  print(trenzaFundamental_10_5.showBraid())

  trenzaFundamental_10_8 = Braid(10, Braid.TrenzaFundamental(10, 8))
  print("\nTrenza fundamental de grado 10 (\"pivotando\" desde el generador 8):")
  print(trenzaFundamental_10_8.showBraid())

  trenzaFundamental_10_1 = Braid(10, Braid.TrenzaFundamental(10, 1))
  print("\nTrenza fundamental de grado 10 (\"pivotando\" desde el generador 1):")
  print(trenzaFundamental_10_1.showBraid())

  trenzaFundamental_10_9 = Braid(10, Braid.TrenzaFundamental(10, 9))
  print("\nTrenza fundamental de grado 10 (\"pivotando\" desde el generador 9):")
  print(trenzaFundamental_10_9.showBraid())
  print("\n")