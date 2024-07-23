"""## SIGNATURE GENERATION

Para generar la firma de un mensaje $m \in \{0,1\}^*$, una vez fijada la función Hash a utilizar (SHA-256), necesitaremos:

1. Cloak Elements:
  1. $v$ oculta $(Id_N, Id_{\mathbb{S}_N})$
  2. $v_1$ oculta $\mathcal{P}(w)$
  3. $v_2$ oculta $\mathcal{P}(w')$

2. Calcular $H(m)$
3. Codificar $m$ a $\mathbb{B}_N$: $E(H(m))$
4. Calcular $Sig = \mathcal{R}(v_1 \cdot w^{-1} \cdot v \cdot E(H(m)) \cdot w' \cdot v_2)$
5. La firma generada es $(H(m), Sig)$
"""

from cloaking_elements import *
from E_Multiplication import *
from encoder import *
from rewriting import *

# Generamos los datos descritos

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
print("Palabra de la primera trenza de la clave privada:", w.showBraid())
print("Palabra de la segunda trenza de la clave privada:", w_.showBraid())

# Clave pública
# E-Multiplicación para M y permM identidad
Pw = E_Multiplicacion_P(w.elementos, N, q, t_values, eval)
Pw_ = E_Multiplicacion_P(w_.elementos, N, q, t_values, eval)
print("\nP(w):\nMatriz:\n ", np.array(Pw[0]), "\n\nPermutación: ", Pw[1])
print("\nP(w'):\nMatriz:\n ", np.array(Pw_[0]), "\n\nPermutación: ", Pw_[1])

# Generamos los 3 Cloak Elements
start_time_cloaking_elements = time.time()
v = Cloaking_Element(Permutation(range(N)), eval, 3, N)
v1 = Cloaking_Element(Pw[1], eval, 3, N)
v2 = Cloaking_Element(Pw_[1], eval, 3, N)
end_time_cloaking_elements = time.time()

print("Cloak Elements Signature Generation:")
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

# Aplicamos función Hash SHA-256
m = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras congue \
tincidunt lectus, vitae tempus sem consequat eu. Fusce vehicula quam a neque \
viverra facilisis. Sed ullamcorper, arcu non tristique vulputate, lectus nulla \
fermentum arcu, nec pulvinar lectus turpis eget nunc. Fusce varius convallis \
urna id accumsan. Duis volutpat congue enim, a aliquam dolor sagittis \
tristique. Suspendisse potenti. Nulla accumsan eros odio, non faucibus ipsum \
tincidunt id. Mauris eget felis ultrices, mollis arcu ultricies, dictum urna. \
Etiam vitae maximus diam."

# Se introduce mensaje por línea de comandos
import argparse
import os

parser = argparse.ArgumentParser(description='Aplicar firma a contenido pasado por línea de comandos.')
parser.add_argument('--mensaje', type=str, help='El mensaje para el algoritmo de firma digital.')
parser.add_argument('--archivo', type=str, help='Ruta al archivo cuyo contenido se usará como mensaje.')

args = parser.parse_args()

if args.archivo and os.path.isfile(args.archivo):
    with open(args.archivo, 'rb') as file:
        m = file.read()
elif args.mensaje:
    m = args.mensaje.encode()

print("MENSAJE A FIRMAR", m)

start_time_hash = time.time()
Hm, cuartetos = SHA256(m)
end_time_hash = time.time()
print("\n\nSalida del Hash binaria\n", Hm)

# Codificamos m a BN
start_time_encoder = time.time()
EHm, CN4 = Encoder_WalnutDSA(m, N)
end_time_encoder = time.time()
print("\n\nSalida hash codificada a trenza del subgrupo puro generado:\n")
print("Palabra:", EHm.elementos)
print("Longitud palabra codificada:", len(EHm.elementos))
print("Permutación proyectada por la trenza codificada:", EHm.perm)

# Calculamos Sig
start_time_sig = time.time()
palabraSig0 = ReduccionLibre(v1.elementos + w.inverseBraid().elementos + \
                      v.elementos + EHm.elementos + w_.elementos + v2.elementos)

palabraSig = StochasticRewriting(palabraSig0, ArtinGen_p, yGen_p)
print("¿SE HA APLICADO ALGÚN CAMBIO?", palabraSig != palabraSig0)

Sig = Braid(N, palabraSig)
end_time_sig = time.time()

execution_time_cloaking_elements = end_time_cloaking_elements - \
start_time_cloaking_elements
execution_time_hash = end_time_hash - start_time_hash
execution_time_encoder = end_time_encoder - start_time_encoder
execution_time_sig = end_time_sig - start_time_sig
execution_time_signature = execution_time_cloaking_elements + \
execution_time_hash + execution_time_encoder + execution_time_sig

print("\n\nSignature:\n")
print("Palabra:", Sig.elementos)
print("Longitud palabra:", len(Sig.elementos))
print("Permutación proyectada:", Sig.perm)

# Firma generada por WalnutDSA (con reescritura)
WalnutDSA_Signature = Hm, Sig

print("\n\nTiempo de Ejecución de la firma: ",  execution_time_signature,
      "segundos")
print("\n\nTiempo de Ejecución de la generación de Cloak Elements: ",
      execution_time_cloaking_elements, "segundos")
print("\n\nTiempo de Ejecución del Hash: ",  execution_time_hash,
      "segundos")
print("\n\nTiempo de Ejecución del Encoder: ",  execution_time_encoder,
      "segundos")
print("\n\nTiempo de Ejecución del cómputo de la firma: ",  execution_time_sig,
      "segundos")
"""## SIGNATURE VERIFICATION

Para verificar la firma generada por WalnutDSA $(H(m), Sig)$, procedemos así:

1.  Codificamos el resumen $H(m)$ a $\mathbb{B}_N: \; E(H(m))$
2. Evaluamos $\mathcal{P}(E(H(m)))$
3. Evaluamos $\mathcal{P}(w) \star Sig$
4. Comprobamos la igualdad:
  $$ Matrix(\mathcal{P}(w) \star Sig) = Matrix(\mathcal{P}(E(H(m)))) \cdot Matrix(\mathcal{P}(w'))$$
"""

# Codificamos resumen a BN
start_time_encoderV = time.time()
EHm = Encoder_WalnutDSA_Hash(Hm, N, CN4)[0]
end_time_encoderV = time.time()
print("\n\nSalida hash codificada a trenza del subgrupo puro generado:\n")
print("Palabra:", EHm.elementos)
print("Longitud palabra codificada:", len(EHm.elementos))
print("Permutación proyectada por la trenza codificada:", EHm.perm)

# Evaluamos P(E(H(m)))
start_time_PEHm = time.time()
PEHm = E_Multiplicacion_P(EHm.elementos, N, q, t_values, eval)
end_time_PEHm = time.time()
print("\nP(E(H(m))):\nMatriz:\n ", np.array(PEHm[0]), "\n\nPermutación: ", PEHm[1])

# E-Multiplicamos P(w) * Sig
start_time_PwSig = time.time()
Pw_Sig = E_Multiplicacion(Pw[0], Pw[1], Sig.elementos, N, q, t_values, eval)
end_time_PwSig = time.time()
print("\n\nE-Multiplicación para P(w) y Sig arbitrarias:\n",
      np.array(Pw_Sig[0]))
print("\nPermutación final:", Pw_Sig[1])

# Calculamos el miembro derecho de la igualdad
start_time_Comp = time.time()
Producto_Verificacion = Mult_Matrix_CF(PEHm[0], Pw_[0], q)

# Comprobamos si se verifica la igualdad (y, por tanto, la firma)
Igualdad_Verificacion = np.array_equal(np.array(Pw_Sig[0]), np.array(Producto_Verificacion))
end_time_Comp = time.time()

pprint(Pw_Sig[0])
print("\n")
pprint(Producto_Verificacion)
print("\n¿Se verifica la identidad del firmante?", Igualdad_Verificacion)

execution_time_encoderV = end_time_encoderV - start_time_encoderV
execution_time_PEHm = end_time_PEHm - start_time_PEHm
execution_time_PwSig = end_time_PwSig - start_time_PwSig
execution_time_Comp = end_time_Comp - start_time_Comp
execution_time_verification = execution_time_encoderV + execution_time_PEHm + \
execution_time_PwSig + execution_time_Comp


print("\n\nTiempo de Ejecución de la Verificación: ",
      execution_time_verification, "segundos")
print("\n\nTiempo de Ejecución de la Codificación: ",
      execution_time_encoderV, "segundos")
print("\n\nTiempo de Ejecución de la P-Evaluación: ",
      execution_time_PEHm, "segundos")
print("\n\nTiempo de Ejecución de la E-Multiplicación: ",
      execution_time_PwSig, "segundos")
print("\n\nTiempo de Ejecución de la comprobación: ",
      execution_time_Comp, "segundos")
