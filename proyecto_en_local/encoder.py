"""# ENCODER

WalnutDSA firma y verifica mensajes trabajando sobre el grupo n-ésimo de trenzas. El encoder convierte un mensaje (presumiblemente $\in \{0,1\}^*$) en una palabra representante de una trenza. Con este fin se siguen los pasos siguientes:

  0. $B: M ⟶ \{0,1\}^*$
  1. $H: \{0,1\}^* ⟶ \{0,1\}^{4k}$
  2. $E: \{0,1\}^{4k} ⟶ C_{N,4}$

Consideramos fase 0 como la conversión de un mensaje formado por caracteres a formato binario. Esto puede ser opcional si por hipótesis los mensajes ya llegan al encoder en formato binario.

En la fase 1 se aplica la función Hash SHA-256 (segunda generación SHA, aún segura). Se utilizará la biblioteca `hashlib`, que mediante el método `digest()` devuelve una salida en bytes, la convertiremos a bits. Por tanto, la cadena de entra a la fase 2 tendrá una longitud de 256 bits.

En la fase 2, trabajaremos a nivel de cuarteto de bits. Necesitamos elegir 4 generadores de un subgrupo de trenzas puras, con los que se construirá la trenza codificada completa, asegurando así que esta trenza final es pura (requisito necesario para WaltnutDSA). Para ello, se proporciona una colección de N-1 posibles generadores, $\{g_{1, N}, g_{2, N}, g_{3, N}, ..., g_{N-1, N}\}$,  que describiremos más adelante, de los cuáles se elegirán 4 aleatoriamente, $\{g_{k_1, N}, g_{k_2, N}, g_{k_3, N}, g_{k_4, N}\}$. Cada cuarteto se codificará utilizando los 2 primeros bits para elegir unos de los 4 generadores y, los 2 segundos bits, para su potencia.

**FASE 0:** Convirtamos una secuencia cualquiera de caracteres en una cadena binaria.
"""
from braid import *
import random

def mensaje_a_binario(mensaje):
    # Convertir el mensaje en una cadena de bytes (usando UTF-8)
    mensaje_bytes = mensaje.encode('utf-8')

    # Convertir bytes del mensaje en cadenas binarias de 8 bits y concatenarlas
    mensaje_binario = ''.join(format(byte, '08b') for byte in mensaje_bytes)

    return mensaje_binario

"""**FASE 1:** Aplicamos función SHA-256 utilizando la biblioteca `hashlib`."""

import hashlib

# Aplica función hash SHA-256 a mensaje, convierte la salida a binario y la
# organiza en cuartetos antes de devolverla
def SHA256(mensaje):

  # Objeto que permite aplicar función Hash
  SHA_256 = hashlib.sha256()
  SHA_256.update(mensaje)

  # Obtener salida del hash como bytes
  hash_bytes = SHA_256.digest()

  # Convertir la salida del hash a binario
  hash_bin = ''.join(format(byte, '08b') for byte in hash_bytes)

  # Organizamos la lista de bits en cuartetos
  cuartetos = []
  for i in range(0, len(hash_bin), 4):
      cuarteto = hash_bin[i:i+4]
      cuartetos.append(cuarteto)

  # Devolvemos la salida hash organizada en cuartetos
  return hash_bin, cuartetos


"""**FASE 2** Implementamos la colección posibles generadores, en función del grado de $\mathbb{B}_N$, elegimos 4 y codificamos cada cuarteto en una potencia de los generadores elegidos"""

# Devuelve una lista con los gradoBn - 1 posibles generadores del subgrupo de
# trenzas puras sobre el que trabajar
def Encoder_gen_sub_pure(gradoBn):

  coleccion = []    # Almacenaremos la colección a devolver

  # Generadores construidos para la colección
  for i in range(gradoBn-1, 0, -1):

    aux = []        # Generador N-i_ésimo

    # Generadores positivos
    for j in range(gradoBn-1, i-1, -1):

      aux.append(j)

    aux.append(i)    # Elemento cuadrado central de la palabra

    # Generadores negativos
    for j in range(i+1, gradoBn):

      aux.append(-j)

    coleccion.append(aux)

  coleccion.reverse()

  return coleccion


# Extrae aleatoriamente una subcolección de n elementos de coleccion
def SubColeccion_Random(coleccion, n):

  if (len(coleccion) < n or n < 1):  # Comprobamos que n sea una longitud válida
    return Null
  else:
    sublista = random.sample(coleccion, n)
    return sublista



# Codifica una cadena binaria (organizada en cuarteros) en una trenza pura a
# partir de 4 generadores puros
def Encoder_Bin_Pure(cuartetos, CN4, gradoBn):

  palabra_final = []

  for cuarteto in cuartetos:

    # Determinamos el generador
    generador = int(cuarteto[2])*2 + int(cuarteto[3])

    # Determinamos el exponente
    exponente = int(cuarteto[0])*2 + int(cuarteto[1]) + 1

    # Codificamos el cuarteto al grupo trenzado (añadiéndolo a la palabra)
    for _ in range(exponente):
      palabra_final = palabra_final + CN4[generador]

  # Creamos formalmente la trenza representada por la palabra final
  trenza_final = Braid(gradoBn, ReduccionLibre(palabra_final))

  return trenza_final


"""**PROCEDIMIENTO COMPLETO**"""

# Aplica el procedimento completo de codificación WalnutDSA
  # (está la opción de pasar por parámetro CN4 los 4 generadores del grupo libre
  # de trenzas puras con el que codificar. Si no se elige aleatoriamente)
def Encoder_WalnutDSA(mensaje, gradoBn, CN4 = []):

  cuartetos = SHA256(mensaje)[1]     # Aplica función Hash al mensaje

  # Posibles generadores del subgrupo CN4
  coleccion_generadores = Encoder_gen_sub_pure(gradoBn)

  # Se eligen aleatoriamente los 4 generadores de CN4
  if (CN4 == []):
    CN4 = SubColeccion_Random(coleccion_generadores, 4)


  # Codifica el mensaje a una trenza pura
  trenza_encoder = Encoder_Bin_Pure(cuartetos, CN4, gradoBn)

  return trenza_encoder, CN4

# Versión del encoder pasando por parámetro el resumen Hash directamente
def Encoder_WalnutDSA_Hash(hash, gradoBn, CN4 = []):

  # Organizamos la lista de bits en cuartetos
  cuartetos = []
  for i in range(0, len(hash), 4):
      cuarteto = hash[i:i+4]
      cuartetos.append(cuarteto)

  # Posibles generadores del subgrupo CN4
  coleccion_generadores = Encoder_gen_sub_pure(gradoBn)

  # Se eligen aleatoriamente los 4 generadores de CN4
  if (CN4 == []):
    CN4 = SubColeccion_Random(coleccion_generadores, 4)

  # Codifica el mensaje a una trenza pura
  trenza_encoder = Encoder_Bin_Pure(cuartetos, CN4, gradoBn)

  return trenza_encoder, CN4

if __name__ == "__main__":

  # Prueba de función Hash
  mensaje = b"HOLA"
  cuartetos = SHA256(mensaje)[1]
  print("\nSalida del Hash binaria organizada en cuartetos;\n", cuartetos)
  print("Cantidad de cuartetos:", len(cuartetos))
  print("Efectivamente, lo he esperado son 64 cuartertos de 4 bits (256 bits como\
  salida de SHA-256)")





  gradoBn = 8
  coleccion_generadores = Encoder_gen_sub_pure(gradoBn)
  print("Colección de generadores de un subgrupo puro para grado %d:" % gradoBn)
  for i in range(gradoBn-1, 0, -1):
    print("g(%d, %d) = %s" %  (i, gradoBn, coleccion_generadores[i-1]))

  # Prueba generador colección de generadores
  CN4 = SubColeccion_Random(coleccion_generadores, 4)

  print("4 generadores elegidos aleatoriamente para la codificación:\n")
  for i in range(len(CN4)):
    print("g(k%d, %d) = %s" %  (i, gradoBn, CN4[i]))
    
  # Prueba del Encoder
  trenza_encoder = Encoder_Bin_Pure(cuartetos, CN4, gradoBn)
  print("Salida hash codificada a trenza del subgrupo puro generado:\n")
  print("Palabra:", trenza_encoder.elementos)
  print("Longitud palabra codificada:", len(trenza_encoder.elementos))
  print("Permutación proyectada por la trenza codificada:", trenza_encoder.perm)
  print("Grado del grupo trenzado al que pertenece:", trenza_encoder.grado)


  # Prueba del Encoder completo
  mensaje = b"Hola Mundo!"
  gradoBn = 8
  trenza_encoder = Encoder_WalnutDSA(mensaje, gradoBn)[0]
  print("Mensaje en código ASCII a codificar:", mensaje)
  print("\nSalida hash codificada a trenza del subgrupo puro generado:")
  print(" Palabra codificada:", trenza_encoder.elementos)
  print(" Longitud de la palabra codificada:", len(trenza_encoder.elementos))
  print(" Permutación proyectada por la trenza codificada:", trenza_encoder.perm)
  print(" Grado del grupo trenzado al que pertenece:", trenza_encoder.grado)

  """El resultado es el esperado, como podemos ver, la trenza obtenida es pura. Además, aunque la palabra no es de longitud fija, ya que dependiendo de los exponentes de cada cuarteto puede variar, si que está acotada por $(2*N-1) * 4 * 64$

  1. $(2*(N-1))$ es la longitud máxima de un generador de CN4
  2. $4$ es el exponente máximo de un generador de CN4
  3. 64 es el número de cuartetos que forman la salida Hash

  Como la salida Hash sí que siempre es 256 bits, podemos acotar con esta expresión la salida del Encoder_WalnutDSA para cualquier entrada. En este caso, para $\mathbb{B_8}$ la longitud máxima es de 3584 generadores.
  """