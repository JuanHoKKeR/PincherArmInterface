import numpy as np
import math
import roboticstoolbox as rtb
from roboticstoolbox import *
from spatialmath import SE3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from math import radians, degrees

def define_robot():
    qlim1, qlim2, qlim3, qlim4 = [-2.6, 2.6], [-2.0, 2.0], [-2.5, 2.5], [-1.8, 1.8]
    L1, L2, L3, L4 = 14.3, 10.7, 10.7, 9.0
    Link1 = rtb.DHLink(d=L1, a=0, alpha=np.pi/2, qlim=qlim1)
    Link2 = rtb.DHLink(d=0, a=L2, alpha=0, offset=np.pi/2, qlim=qlim2)
    Link3 = rtb.DHLink(d=0, a=L3, alpha=0, qlim=qlim3)
    Link4 = rtb.DHLink(d=0, a=L4, alpha=0, qlim=qlim4)
    robot = rtb.DHRobot([Link1, Link2, Link3, Link4], name='Pincher rtb')
    return robot

def IK_robot(x,y,z):
    yaw_deseado = radians(90)  # Convertir a radianes si estás trabajando con grados
    pitch = 0  # Ángulo de Pitch inicial
    # Rango de Pitch a barrer
    roll_min = radians(-150)
    roll_max = radians(150)
    roll_step = radians(5)  # Definir un paso adecuado para el barrido

    menor_error = 0.1
    mejor_solucion = None

    for roll in np.arange(roll_min, roll_max, roll_step):
        T = SE3(x, y, z) * SE3.RPY([yaw_deseado, pitch, roll], order='zyx')
        solution = robot.ikine_LM(T, [0, 0, 0, 0], 15, 10, 0.01, True)
        if solution.success and solution.residual < menor_error:
            mejor_solucion = solution
            menor_error = solution.residual
    # Procesar soluciones válidas
    if mejor_solucion is not None:
        #print(f"Mejor solución encontrada con error residual {menor_error}: {mejor_solucion.q}")
        #print(f"Ángulos en grados: {[degrees(angle) for angle in mejor_solucion.q]}")
        return mejor_solucion.q
    else:
        #print("No se encontró una solución válida.")
        return None

robot = define_robot()

# # # Inicializa las posiciones de las articulaciones
# joint_positions = [0, 0, 0, 0]


# print(f"Posición de la herramienta: {T.t}")
# print("Pasando a ikine")
# q = robot.ikine_LM(T)
# print(f"Posición de las articulaciones: {q.q}")

# robot.plot(joint_positions)

def Circle(altura, centro_x, centro_y, radio):
    # Parámetros del círculo
    t = np.linspace(0, 2*np.pi, 20)  # 10 puntos en el círculo
    r = radio  # Radio del círculo
    y = r * np.sin(t) + centro_y  # Coordenadas y
    x = r * np.cos(t) + centro_x  # Coordenadas x
    z = altura  # Coordenadas z
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Itera sobre cada punto en el círculo
    for yi, xi in zip(y, x):
        ax.scatter(xi, yi, z, s=50, c='b')  # s es el tamaño del punto

    # Mostrar el gráfico
    plt.show()
    return x, y, z


def Heart(altura, centro_x, centro_y, radio):
    # Parámetros del corazón
    t = np.linspace(0, 2*np.pi, 40)  # 100 puntos para una mejor resolución
    x = radio * (16 * np.sin(t)**3) + centro_x
    y = radio * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)) + centro_y
    z = altura
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for yi, xi in zip(y, x):
        ax.scatter(xi, yi, z, s=50, c='b')  # s es el tamaño del punto

    # Mostrar el gráfico
    plt.show()
    return x, y, z

x, y, z = Heart(10, 16, 16, 0.3)

#x, y, z =Circle(4, 8, 18, 4)


for yi, xi in zip(y,x):
    q = IK_robot(xi, yi, z)
    if q is not None:
        # robot.plot(q)
        # time.sleep(0.01)  # Esperar un poco para ver el resultado
        q_formatted = ", ".join([f"{q_:.3f}" for q_ in q])
        print(q_formatted)
    else:
        print("No se encontró una solución válida.")
        

 


