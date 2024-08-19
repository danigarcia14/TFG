# Instalamos la biblioteca `pyfinite`, que maneja campos finitos y sus 
# operaciones subyacentes. Esta será necesaria para trabajar con campos finitos
# al definir las matrices de Burau y la E-Multiplication asociadas al grupo de 
# trenzas

#!pip install pyfinite

# Esta biblioteca ofrece la clase `FField` del módulo `pyfinite.ffield`, la cual 
# implementa toda la estructura de campos finitos.

from pyfinite import ffield

import numpy as np


if __name__ == "__main__":

  # Creamos el campo finito de 32 elementos (2^5)
  F32 = ffield.FField(5)

  # Veamos como se construye dicho campo, visualizando la correspondencia entre el
  # elemento n-ésimo del campo y el polinomio asociado en el anillo cociente
  # considerado
  print("\nCORRESPONDENCIA ENTRE ELEMENTO I-ÉSIMO Y POLINOMIO EN EL COCIENTE:\n")
  for i in range(32):
    print("Elemento: {}  -->   Representación polinómica: {}".format(
        str(i).ljust(2), F32.ShowPolynomial(i)))

  # Realizamos operaciones aritméticas básicas
  suma_10_5 = F32.Add(30,31)
  resta_2_27 = F32.Subtract(2,27)
  producto_12_19 = F32.Multiply(12,19)
  division_20_10 = F32.Divide(20,10)

  print("\nOPERACIONES ARITMÉTICAS BÁSICAS:\n")
  print("Suma de los elementos 10 y 5:", F32.ShowPolynomial(suma_10_5))
  print("Resta de los elementos 2 y 27:", F32.ShowPolynomial(resta_2_27))
  print("Producto de los elementos 12 y 19:", F32.ShowPolynomial(producto_12_19))
  print("División de los elementos 20 y 10:", F32.ShowPolynomial(division_20_10))

  # Listamos los inversos de cada elemento (exceptuando el 0,
  # que no es invertible)
  print("\nLISTA DE INVERSOS DE CADA ELEMENTO:\n")
  for i in range(32):
    if(i != 0):
      inverso = F32.Inverse(i)
      print("Elemento {}: {}  -->   Inverso {} : {}".format(str(i).rjust(2),
              F32.ShowPolynomial(i).ljust(25), str(inverso).rjust(2),
              F32.ShowPolynomial(inverso)))

  print("\nLA SUMA Y LA RESTA DEL CUERPO SE EXTIENDEN A ARRAYS:\n")

  # Definimos dos matrices sobre el campo finito F32 (realmente definimos su
  # su representación mediante la matriz de sus identificadores)
  m1 = np.array([[1,2],[1,3]])
  m2 = np.array([[15,0],[1,1]])

  m_sum = F32.Add(m1,m2) # Sumamos ambas matrices en el campo
  print("Matrices  M1 y M2 a operar:")
  print("", m1)
  print("\n", m2)
  print("\nSuma de matrices en F32:\n", m_sum)

  # Definimos dos vectores sobre el campo finito F32 (análogamente, se definen 
  # sus identificadores)
  v1 = np.array([1,2,3])
  v2 = np.array([4,5,6])

  v_sub = F32.Subtract(v1, v2)  # Restamos ambos vectores en el campo
  print("\nVectores v1 y v2 a operar:")
  print("V1 = ", v1, "V2 =", v2)
  print("\nResta de vectores en F32:\n", v_sub)

  print("\nLos métodos 'Multiply' y 'Divide' no soportan la entrada de \
vectores/matrices como parámetros.\n\n")