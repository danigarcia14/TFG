"""## Protocolo conjugador - Ko-Lee-Cheon

Se comienza fijando un grupo trenzado $\mathbb{B}_{2N}$ y dos subgrupos públicos , de la forma

\begin{align*}
	& L\mathbb{B}_{2N} = <b_1, ..., b_{N_1}>  \;\subset \mathbb{B}_{2N}\\
	& U\mathbb{B}_{2N} = <b_{N+1}, ..., b_{2N-1}> \; \subset \mathbb{B}_{2N}\\
\end{align*}

correspondiendo a las partes de la comunicación $A$ y $B$, respectivamente.
"""

from commutator_protocol import *

# grado del grupo trenzado sobre el que construir el protocolo
N = 8

# índices de los generadores de los subgrupos públicos
S = {1, 2, 3}  # subgrupo asociado a la parte A
T = {5, 6, 7}     # subgrupo asociado a la parte B

"""Se utiliza el método "GeneradorSecretoProtocolo" para elegir un secreto por subgrupo, perteneciente a cada parte. Además, se genera una trenza $x$ compartida, presumiblemente complicada."""

# Secreto generados para cada parte
secreto_parte_A = Braid(N, GeneradorSecretoProtocolo(S, 20, True))
secreto_parte_B = Braid(N, GeneradorSecretoProtocolo(T, 20, True))
trenza_compartida_x = Braid(N, GeneradorSecretoProtocolo({1,2,3,4,5,6,7}, 20, True))

print("Secreto a:", secreto_parte_A.showBraid())
print("Secreto b:", secreto_parte_B.showBraid())
print("Trenza compartida x:", trenza_compartida_x.showBraid())

"""Cada parte debe conjugar la trenza compartida con su secreto generado, intercambiándose tales conjugados, de forma que:


1.   Parte A calcula y envía a B el conjugado: $y_a = axa^{-1}$
2.   Parte B calcula y envía a A el conjugado: $y_b = bxb^{-1}$


"""

# Conjugado que calcula la parte A
conjugado_parte_A = secreto_parte_A.concatenateBraid(trenza_compartida_x).concatenateBraid(secreto_parte_A.inverseBraid())

# Conjugado que calcula la parte B
conjugado_parte_B = secreto_parte_B.concatenateBraid(trenza_compartida_x).concatenateBraid(secreto_parte_B.inverseBraid())

print("Conjugado de la parte A:", conjugado_parte_A.showBraid())
print("Conjugado de la parte B:", conjugado_parte_B.showBraid())

"""El protocolo de establecimiento de secreto compartido finaliza con cada parte computando tal secreto, de la siguiente forma:


1.   Cómputo del secreto compartido por parte de A: $SecretoCompartidoA = ay_ba^{-1} = abx^{-1}b^{-1}a^{-1}$
2.   Cómputo del secreto compartido por parte de B: $SecretoCompartidoB = by_ab^{-1} = baxa^{-1}b^{-1}$

Dado que los subgrupos $L\mathbb{B}_{2N}$ y $U\mathbb{B}_{2N}$ conmutan, se
obtiene que:

$$SecretoCompartidoB = baxa^{-1}b^{-1} = abx^{-1}b^{-1}a^{-1} =  SecretoCompartido$$  

Computemos el secreto compartido asociado a cada parte, comprando finalmente que ambas partes cuentan con el mismo secreto.
"""

# Secretos compartidos computados por cada parte
Secreto_Compartido_A = secreto_parte_A.concatenateBraid(conjugado_parte_B).concatenateBraid(secreto_parte_A.inverseBraid())
Secreto_Compartido_B = secreto_parte_B.concatenateBraid(conjugado_parte_A).concatenateBraid(secreto_parte_B.inverseBraid())

print("Secreto compartido computado por parte A:", Secreto_Compartido_A.elementos)
print("Secreto compartido computado por parte B:", Secreto_Compartido_B.elementos)

print("¿Han llegado ambas partes al mismo secreto compartido?:",
      Secreto_Compartido_A.elementos == Secreto_Compartido_B.elementos)

print("Aunque no coincidan las palabras, está demostrado que son equivalentes. \
Para poder verificarlo habría que implementar la forma canónica de Garside, que \
      es única para cada trenza salvo equivalencias")

"""Aunque no coincidan las palabras, está demostrado que son equivalentes.
Para poder verificarlo habría que implementar la forma canónica de Garside, que
es única para cada trenza salvo equivalencias.
"""