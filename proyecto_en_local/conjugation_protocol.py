
from commutator_protocol import *

# DATOS DEL PROTOCOLO

print("\nDATOS PÚBLICOS DEL PROTOCOLO:\n")

# grado del grupo trenzado sobre el que construir el protocolo
N = 8

# índices de los generadores de los subgrupos públicos
S = {1, 2, 3}  # subgrupo asociado a la parte A
T = {5, 6, 7}     # subgrupo asociado a la parte B

print("Grado del grupo trenzado elegido:", N)
print("Generadores del subgrupo acordado para la parte A:", S)
print("Generadores del subgrupo acordado para la parte B:", T)
trenza_compartida_x = Braid(N, GeneradorSecretoProtocolo({1,2,3,4,5,6,7}, 20, True))
print("Trenza compartida x:", trenza_compartida_x.showBraid())


# Secreto generados para cada parte
secreto_parte_A = Braid(N, GeneradorSecretoProtocolo(S, 20, True))
secreto_parte_B = Braid(N, GeneradorSecretoProtocolo(T, 20, True))
print("\nSECRETOS DE CADA PARTE:\n")
print("Secreto a:", secreto_parte_A.showBraid())
print("Secreto b:", secreto_parte_B.showBraid())

# COMPUTACIÓN DEL CONJUGADO A ENVIAR POR CADA PARTE

print("\nCOMPUTACIÓN DEL CONJUGADO A ENVIAR POR CADA PARTE:\n")

# Conjugado que calcula la parte A
conjugado_parte_A = secreto_parte_A.concatenateBraid(trenza_compartida_x).concatenateBraid(secreto_parte_A.inverseBraid())

# Conjugado que calcula la parte B
conjugado_parte_B = secreto_parte_B.concatenateBraid(trenza_compartida_x).concatenateBraid(secreto_parte_B.inverseBraid())

print("Conjugado de la parte A:", conjugado_parte_A.showBraid())
print("Conjugado de la parte B:", conjugado_parte_B.showBraid())

# COMPUTACIÓN DEL SECRETO COMPARTIDO TRAS EL INTERCAMBIO DE CONJUGADOS

print("\nCOMPUTACIÓN DEL SECRETO COMPARTIDO TRAS EL INTERCAMBIO DE CONJUGADOS:\n")

# Secretos compartidos computados por cada parte
Secreto_Compartido_A = secreto_parte_A.concatenateBraid(conjugado_parte_B).concatenateBraid(secreto_parte_A.inverseBraid())
Secreto_Compartido_B = secreto_parte_B.concatenateBraid(conjugado_parte_A).concatenateBraid(secreto_parte_B.inverseBraid())

print("Secreto compartido computado por parte A:", Secreto_Compartido_A.elementos)
print("Secreto compartido computado por parte B:", Secreto_Compartido_B.elementos)

print("¿Han llegado ambas partes al mismo secreto compartido?:",
      Secreto_Compartido_A.elementos == Secreto_Compartido_B.elementos, "\n")