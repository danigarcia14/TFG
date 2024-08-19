
from cloaking_elements import *
from E_Multiplication import *
from encoder import *
from rewriting import *
# Se introduce mensaje por línea de comandos
import argparse
import os

# GENERACIÓN DE PARÁMETROS Y CLAVES

# Orden del grupo trenzado Bn
N = 8

# Campo finito
q = 5 # Realmente q = 2^5, pero FField requiere del exponente
F32 = ffield.FField(q)

# T_Values
t1, t2, t3, t4, t5, t6, t7, t8 = symbols('t1 t2 t3 t4 t5 t6 t7 t8')
t_values = np.array([t1, t2, t3, t4, t5, t6, t7, t8]) # t_values
eval = np.array([6, 1, 1, 9, 19, 14, 29, 30])

# T_Unos
t_unos = Comprobador_cloak_t_unos(eval, N)  # posiciones en el vector
a = t_unos[0] + 1                           # índices en los t_values
b = t_unos[1] + 1

# Clave privada
w = Braid(N, ReduccionLibre(Palabra_aleatoria(N, 25, 50)))
w_ = Braid(N, ReduccionLibre(Palabra_aleatoria(N, 25, 50)))

# Clave pública
# E-Multiplicación para M y permM identidad
Pw = E_Multiplicacion_P(w.elementos, N, q, t_values, eval)
Pw_ = E_Multiplicacion_P(w_.elementos, N, q, t_values, eval)

print("\nPARÁMETROS PÚBLICOS DEL SISTEMA:\n")
print("Grado del grupo trenzado:", N)
print("Algoritmo de reescritura: Algoritmo de estocásito de Kayawood")
print("Grado del campo finito:", q)
print("Índices de los t-valores con valor 1:", a, b)
print("T-valores que definen la E-Multiplicación:", t_values)

print("\nCLAVES DEL SISTEMA:\n")
print("Palabra de la primera trenza de la clave privada:", w.showBraid())
print("Palabra de la segunda trenza de la clave privada:", w_.showBraid())
print("\nP(w):\nMatriz:\n")
pprint(Pw[0])
print("\n\nPermutación: ", Pw[1])
print("\nP(w'):\nMatriz:\n ") 
pprint(Pw_[0])
print("\n\nPermutación: ", Pw_[1])


# GENERACIÓN DE LA FIRMA

print("\nGENERACIÓN DE LA FIRMA:\n")

# PASO 1 - GENERACIÓN DE LOS ELEMENTOS DE OCULTACIÓN

# Generamos los 3 Cloak Elements
start_time_cloaking_elements = time.time()
v = Cloaking_Element(Permutation(range(N)), eval, 3, N)
v1 = Cloaking_Element(Pw[1], eval, 3, N)
v2 = Cloaking_Element(Pw_[1], eval, 3, N)
end_time_cloaking_elements = time.time()

print("PASO 1 - GENERACIÓN DE LOS ELEMENTOS DE OCULTACIÓN:\n")
print("\nv =", v.showBraid())
print("v1 =", v1.showBraid())
print("v2 =", v2.showBraid())

print("\nComprobaciones de Cloak Elements")
print("\nID * v =", E_Multiplicacion(eye(N), Permutation(range(N)),
                                     v.elementos, N, q, t_values, eval))
print("\nP(w) * v1 =", E_Multiplicacion(Pw[0], Pw[1], v1.elementos, N, q,
                                        t_values, eval))
print("\nP(w') * v2 =", E_Multiplicacion(Pw_[0], Pw_[1], v2.elementos, N, q,
                                         t_values, eval))
                                         

# PASO 2 - CÁLCULO DEL HASH DEL MENSAJE

# Aplicamos función Hash SHA-256

# Mensaje por defecto en caso de no introducir ningún mensaje durante la ejecución
m = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras congue \
tincidunt lectus, vitae tempus sem consequat eu. Fusce vehicula quam a neque \
viverra facilisis. Sed ullamcorper, arcu non tristique vulputate, lectus nulla \
fermentum arcu, nec pulvinar lectus turpis eget nunc. Fusce varius convallis \
urna id accumsan. Duis volutpat congue enim, a aliquam dolor sagittis \
tristique. Suspendisse potenti. Nulla accumsan eros odio, non faucibus ipsum \
tincidunt id. Mauris eget felis ultrices, mollis arcu ultricies, dictum urna. \
Etiam vitae maximus diam."


# Entrada del mensaje a firmar como argumento del programa
parser = argparse.ArgumentParser(description='Aplicar firma a contenido pasado por línea de comandos.')
parser.add_argument('--mensaje', type=str, help='El mensaje para el algoritmo de firma digital.')
parser.add_argument('--archivo', type=str, help='Ruta al archivo cuyo contenido se usará como mensaje.')

args = parser.parse_args()

if args.archivo and os.path.isfile(args.archivo):
    with open(args.archivo, 'rb') as file:
        m = file.read()
elif args.mensaje:
    m = args.mensaje.encode()


print("\nCÁLCULO DEL HASH DEL MENSAJE A FIRMAR:\n")
print("Mensaje a firmar:", m)

start_time_hash = time.time()
Hm, cuartetos = SHA256(m)
end_time_hash = time.time()
print("\n\nSalida binaria del Hash del mensaje:", Hm)

# PASO 3 - CODIFICACIÓN DEL HASH AL GRUPO TRENZADO ACORDADO

print("\nCODIFICACIÓN DEL HASH AL GRUPO TRENZADO ELEGIDO:\n")

# Codificamos m a BN
start_time_encoder = time.time()
EHm, CN4 = Encoder_WalnutDSA(m, N)
end_time_encoder = time.time()
print("Salida hash codificada a trenza del subgrupo puro generado:\n")
print("Palabra:", EHm.elementos)
print("Longitud palabra codificada:", len(EHm.elementos))
print("Permutación proyectada por la trenza codificada:", EHm.perm)


# PASO 4 - CÁLCULO DE LA FIRMA

print("\nCÁLCULO DE LA FIRMA:\n")

# Calculamos Sig
start_time_sig = time.time()
palabraSig0 = ReduccionLibre(v1.elementos + w.inverseBraid().elementos + \
                      v.elementos + EHm.elementos + w_.elementos + v2.elementos)

palabraSig = StochasticRewriting(palabraSig0, ArtinGen_p, yGen_p)
print("Como se puede ver comprobar, el algoritmo de reescritura \
efectivamente genera una nueva palabra:")
print("\nPalabra original representante de la firma:", palabraSig0)

Sig = Braid(N, palabraSig)
end_time_sig = time.time()

execution_time_cloaking_elements = end_time_cloaking_elements - \
start_time_cloaking_elements
execution_time_hash = end_time_hash - start_time_hash
execution_time_encoder = end_time_encoder - start_time_encoder
execution_time_sig = end_time_sig - start_time_sig
execution_time_signature = execution_time_cloaking_elements + \
execution_time_hash + execution_time_encoder + execution_time_sig

print("\nTrenza Sig que actúa como firma:")
print("Palabra:", Sig.elementos)
print("Longitud palabra:", len(Sig.elementos))
print("Permutación proyectada:", Sig.perm)

# PASO 5 - FIRMA GENERADA POR WALNUTDSA
WalnutDSA_Signature = Hm, Sig

# DESGLOSE DE LOS TIEMPOS DE EJECUCIÓN EMPLEADOS

print("\nDESGLOSE DE LOS TIEMPO DE EJECUCIÓN EMPLEADOS:\n")

print("\nTiempo de Ejecución de la firma: ",  execution_time_signature,
      "segundos")
print("\n\nTiempo de Ejecución de la generación de Cloak Elements: ",
      execution_time_cloaking_elements, "segundos")
print("\n\nTiempo de Ejecución del Hash: ",  execution_time_hash,
      "segundos")
print("\n\nTiempo de Ejecución del Encoder: ",  execution_time_encoder,
      "segundos")
print("\n\nTiempo de Ejecución del cómputo de la firma: ",  execution_time_sig,
      "segundos")

# VERIFICACIÓN DE LA FIRMA

print("\nVERIFICACIÓN DE LA FIRMA:\n")

# PASO 1 - CODIFICACIÓN DEL HASH AL GRUPO TRENZADO ACORDADO
print("PASO 1 - CODIFICACIÓN DEL HASH AL GRUPO TRENZADO ACORDADO:\n")

# Codificamos resumen a BN
start_time_encoderV = time.time()
EHm = Encoder_WalnutDSA_Hash(Hm, N, CN4)[0]
end_time_encoderV = time.time()
print("Salida hash codificada a trenza del subgrupo puro generado:\n")
print("Palabra:", EHm.elementos)
print("Longitud palabra codificada:", len(EHm.elementos))
print("Permutación proyectada por la trenza codificada:", EHm.perm)

# PASO 2 - EVALUACIÓN DE P(E(H(m)))
print("\nPASO 2 - EVALUACIÓN DE P(E(H(m))):\n")

# Evaluamos P(E(H(m)))
start_time_PEHm = time.time()
PEHm = E_Multiplicacion_P(EHm.elementos, N, q, t_values, eval)
end_time_PEHm = time.time()
print("P(E(H(m))):\nMatriz =\n ")
pprint(PEHm[0])
print("\n\nPermutación = ", PEHm[1])

# PASO 3 - EVALUACIÓN Y CÁLCULO DE P(w) * Sig
print("\nPASO 3 - EVALUACIÓN Y CÁLCULO DE P(w) * Sig:\n")

# E-Multiplicamos P(w) * Sig
start_time_PwSig = time.time()
Pw_Sig = E_Multiplicacion(Pw[0], Pw[1], Sig.elementos, N, q, t_values, eval)
end_time_PwSig = time.time()
print("E-Multiplicación para P(w) y Sig arbitrarias = \n")
pprint(Pw_Sig[0])
print("\nPermutación final:", Pw_Sig[1])


# PASO 4 - COMPROBACIÓN DE IGUALDAD QUE VERIFICA SI Y SOLO SI LA FIRMA
print("\nPASO 4 - COMPROBACIÓN DE IGUALDAD QUE VERIFICA SI Y SOLO SI LA FIRMA:\n")

# Calculamos el miembro derecho de la igualdad
start_time_Comp = time.time()
Producto_Verificacion = Mult_Matrix_CF(PEHm[0], Pw_[0], q)

# Comprobamos si se verifica la igualdad (y, por tanto, la firma)
Igualdad_Verificacion = np.array_equal(np.array(Pw_Sig[0]), np.array(Producto_Verificacion))
end_time_Comp = time.time()

print("Miembro izquierdo de la igualdad:\n")
pprint(Pw_Sig[0])
print("\n")
print("Miembro derecho de la igualdad:\n")
pprint(Producto_Verificacion)

print("\n¿Se verifica la identidad del firmante?", Igualdad_Verificacion)


# DESGLOSE DE LOS TIEMPOS DE EJECUCIÓN

execution_time_encoderV = end_time_encoderV - start_time_encoderV
execution_time_PEHm = end_time_PEHm - start_time_PEHm
execution_time_PwSig = end_time_PwSig - start_time_PwSig
execution_time_Comp = end_time_Comp - start_time_Comp
execution_time_verification = execution_time_encoderV + execution_time_PEHm + \
execution_time_PwSig + execution_time_Comp

print("\n\nDESGLOSE DE LOS TIEMPSO DE EJECUCIÓN:\n")

print("\nTiempo de Ejecución de la Verificación: ",
      execution_time_verification, "segundos")
print("\n\nTiempo de Ejecución de la Codificación: ",
      execution_time_encoderV, "segundos")
print("\n\nTiempo de Ejecución de la P-Evaluación: ",
      execution_time_PEHm, "segundos")
print("\n\nTiempo de Ejecución de la E-Multiplicación: ",
      execution_time_PwSig, "segundos")
print("\n\nTiempo de Ejecución de la comprobación: ",
      execution_time_Comp, "segundos\n")
