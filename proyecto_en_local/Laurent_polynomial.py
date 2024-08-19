
# Instalamos la biblioteca `SymPy`, la cual permite la manipulación de expresiones 
# algebraicas. Como alternativa, consideramos `SciPy`, una biblioteca adecuada 
# para integrar algoritmos matemáticos de alta velocidad en Python, y no descartamos 
# su inclusión en el trabajo más adelante.
from sympy import *
import numpy as np

if __name__ == "__main__":

    print("\nOPERACIONES BÁSICAS SOBRE POLINOMIOS DE LAURENT:\n")

    # Definimos variables
    x, y, z = symbols('x y z')
    print("Variables definidas:", x, y, z)

    # Definimos polinimios de Laurent
    f1 = x**2 - 1/4
    f2 = y**-1 + 3
    f3 = z**4 - 1
    f = f1 + f2 + f3
    print("\nPolinomios de Laurent:")
    print("f1 =", f1)
    print("f2 =", f2)
    print("f3 =", f3)
    print("f = f1 + f2 + f3 =", f)

    # Factorizamos los polinomios (por defecto factoriza en Z)
    print("\nPolinomios factorizados:")
    f1_fact = factor(f1)
    print("f1 =", f1_fact)
    f2_fact = factor(f2)
    print("f2 =", f2_fact)
    f3_fact = factor(f3)
    print("f3 =", f3_fact)

    # Expandimos (acción inversa a la factorización)
    print("\nPolinomios expandidos:")
    f1_exp = expand(f1_fact)
    print("f1 =", f1_exp)
    f2_exp = expand(f2_fact)
    print("f2 =", f2_exp)
    f3_exp = expand(f3_fact)
    print("f3 =", f3_exp)

    # Evaluaciones de las variables en los polinomios definidos
    f1_eval = f1.subs(x,1)
    f2_eval = f2.subs(y,2)
    f3_eval = f3.subs(z,3)
    f_eval = f.subs({x:1, y:2})   # Se pueden dejar variables sin evaluar
    print("\nEvaluaciones de polinomios:")
    print("f1(1) =", f1_eval)
    print("f2(2) =", f2_eval)
    print("f3(3) =", f3_eval)
    print("f(1,2) =", f_eval)

    # Variables y evaluaciones
    x, y = symbols('x y')
    var = np.array([x,y])
    eval = np.array([2,3])

    # Matriz variable no Numpy
    matriz = Matrix([[x,y], [2*x, x-y]])
    print("\nMatrix variable:\n",matriz)
    matriz_eval = matriz.subs({var[i]: eval[i] for i in range(len(var))})
    print("\nMatrix evaluada:\n", matriz_eval)

    # Matriz variables Numpy
    diag = np.array([x,y,x,y,x])
    matriz_diag = np.diag(diag)
    print("\nMatriz Numpy variable:\n", matriz_diag)
    matriz_diag_eval = Matrix(matriz_diag).subs({var[i]: eval[i]
                                                for i in range(len(var))})
    print("\nMatriz Numpy evaluada\n",np.array(matriz_diag_eval))
    print("\n")

    # Cambiamos el campo sobre el que trabajamos a F32
    #f_CFinito = F32.ShowPolynomial(f)
    #f123 = F32.Add(10,x)

    # ESTOS INTENTOS DE INTERGAR PYFINITE EN SYMPY FALLAN