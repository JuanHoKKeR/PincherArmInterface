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

robot = define_robot()

# # # Inicializa las posiciones de las articulaciones
# joint_positions = [0, 0, 0, 0]

# # T = robot.fkine(joint_positions)
# T = SE3([
#     [0.1226, -0.7932, 0.5965, 12],
#     [0.09115, -0.5895, -0.8026, 9],
#     [0.9883, 0.1528, 0, 30],
#     [0, 0, 0, 1]
# ])
# print(f"Posición de la herramienta: {T.t}")
# print("Pasando a ikine")
# q = robot.ikine_LM(T)
# print(f"Posición de las articulaciones: {q.q}")

# robot.plot(joint_positions)

# # Parámetros del semicírculo
# t = np.linspace(0, np.pi, 10)  # 10 puntos en el semicírculo
# r = 3  # Radio del semicírculo
# x = r * np.cos(t)  # Coordenadas x
# y = r * np.sin(t) + 9 # Coordenadas y
# z = 30  # Coordenadas z
# # robot.plot([0, 0, 0, 0])
# # fig = plt.figure()
# # ax = fig.add_subplot(111, projection='3d')
# # # Itera sobre cada punto en el semicírculo
# # for yi, xi in zip(y, x):
# #     ax.scatter(xi, yi, z, s=100, c='b')  # s es el tamaño del punto

# # # Mostrar el gráfico
# # plt.show(block=True)







# for yi, xi in zip(y,x):
#     # Crea la transformación homogénea para el punto objetivo
#     Tm = SE3(xi, yi, z) #* SE3.RPY([0, 0, 0], unit='rad')  # Ajusta la orientación si es necesario
#     #print(f"Matriz de transformación homogénea {Tm}")
#     #Calcula la cinemática inversa para encontrar las posiciones de las articulaciones
#     solucion = robot.ikine_LM(Tm, joint_positions, 70, 120,1.3, True, None, None) # Usa ikine_LM o cualquier otro método de cinemática inversa adecuado
#     if solucion.success:
#         print(solucion.q)
#         robot.plot(solucion.q)
#         time.sleep(0.01)
#     else:
#         print("No se encontró solución")
 


# Suponiendo que ya tienes definido tu robot en 'robot'
# Y las posiciones X, Y, Z y el ángulo Yaw deseados
x_deseado, y_deseado, z_deseado = 8.8, 4.5, 30.7  # Ejemplo de posición deseada
yaw_deseado = radians(90)  # Convertir a radianes si estás trabajando con grados
pitch = 0  # Ángulo de Pitch inicial
# Rango de Pitch a barrer
roll_min = radians(-150)
roll_max = radians(150)
roll_step = radians(5)  # Definir un paso adecuado para el barrido

menor_error = 2
mejor_solucion = None
# Lista para almacenar soluciones válidas
soluciones_validas = []

for roll in np.arange(roll_min, roll_max, roll_step):
    T_deseada = SE3(x_deseado, y_deseado, z_deseado) * SE3.RPY([yaw_deseado, pitch, roll], order='zyx')
    solucion = robot.ikine_LM(T_deseada, [0, 0, 0, 0], 20, 10, 0.2, True)
    print(f"Solución: {solucion}")

    # Verificar si la solución es válida y cumple con los criterios de error
    if solucion.success and solucion.residual < menor_error:
        mejor_solucion = solucion
        menor_error = solucion.residual
        if menor_error < 30e-3:
            break

# Procesar soluciones válidas
if mejor_solucion is not None:
    print(f"Mejor solución encontrada con error residual {menor_error}: {mejor_solucion.q}")
    print(f"Ángulos en grados: {[degrees(angle) for angle in mejor_solucion.q]}")
else:
    print("No se encontró una solución válida.")