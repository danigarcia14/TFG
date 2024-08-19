
from braid import *
import random
import hashlib

def mensaje_a_binario(mensaje):
    # Convertir el mensaje en una cadena de bytes (usando UTF-8)
    mensaje_bytes = mensaje.encode('utf-8')

    # Convertir bytes del mensaje en cadenas binarias de 8 bits y concatenarlas
    mensaje_binario = ''.join(format(byte, '08b') for byte in mensaje_bytes)

    return mensaje_binario

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
    return None
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
  print("\nPRUEBA DE EJECUCIÓN de 'SHA256':\n")
  mensaje = b"HOLA"
  cuartetos = SHA256(mensaje)[1]
  print("Salida del Hash binaria organizada en cuartetos;\n", cuartetos)
  print("Cantidad de cuartetos:", len(cuartetos))
  print("Efectivamente, lo he esperado son 64 cuartertos de 4 bits (256 bits como\
  salida de SHA-256)")

  # Prueba generador colección de generadores
  print("\nPRUEBA DE EJECUCIÓN DE 'SubColeccion_Random':\n")
  gradoBn = 8
  coleccion_generadores = Encoder_gen_sub_pure(gradoBn)
  print("Colección de generadores de un subgrupo puro para grado %d:" % gradoBn)
  for i in range(gradoBn-1, 0, -1):
    print("g(%d, %d) = %s" %  (i, gradoBn, coleccion_generadores[i-1]))

  print("\nPRUEBA DE EJECUCIÓN DE 'SubColeccion_Random':\n")
  CN4 = SubColeccion_Random(coleccion_generadores, 4)
  print("4 generadores elegidos aleatoriamente para la codificación:\n")
  for i in range(len(CN4)):
    print("g(k%d, %d) = %s" %  (i, gradoBn, CN4[i]))
    
  # Prueba del Encoder
  print("\nPRUEBA DE EJECUCIÓN DE 'Encoder_Bin_Pure':\n")
  trenza_encoder = Encoder_Bin_Pure(cuartetos, CN4, gradoBn)
  print("Salida hash codificada a trenza del subgrupo puro generado:\n")
  print("Palabra:", trenza_encoder.elementos)
  print("Longitud palabra codificada:", len(trenza_encoder.elementos))
  print("Permutación proyectada por la trenza codificada:", trenza_encoder.perm)
  print("Grado del grupo trenzado al que pertenece:", trenza_encoder.grado)

  # Prueba del Encoder completo
  print("\nPRUEBA DE EJECUCIÓN DEL PROCEDIMIENTO DE EJEUCIÓN COMPLETO:\n")
  mensaje = b"Hola Mundo!"
  gradoBn = 8
  trenza_encoder = Encoder_WalnutDSA(mensaje, gradoBn)[0]
  print("Mensaje en código ASCII a codificar:", mensaje)
  print("\nSalida hash codificada a trenza del subgrupo puro generado:")
  print(" Palabra codificada:", trenza_encoder.elementos)
  print(" Longitud de la palabra codificada:", len(trenza_encoder.elementos))
  print(" Permutación proyectada por la trenza codificada:", trenza_encoder.perm)
  print(" Grado del grupo trenzado al que pertenece:", trenza_encoder.grado, "\n")