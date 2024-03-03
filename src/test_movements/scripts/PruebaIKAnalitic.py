import numpy as np
import math
import roboticstoolbox as rtb
from roboticstoolbox import *
from spatialmath import SE3, SO3
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


def ikinematics(T_des):
    L1, L2, L3, L4 = 14.3, 10.7, 10.7, 9.0
    R = T_des.R
    # Extrae el ángulo de pitch (θ) usando arco seno
    translation = T_des.translation
    x = translation[0]
    y = translation[1]
    z = translation[2]
    theta = np.arcsin(R[2, 1]) 
    
    
    
    q1 = np.arctan2(y,x)
    
    MTH6 = SE3.Trans(x, y, z)*SE3.RPY(pi/2,theta,q1)
    print("MTH6")
    print(MTH6)

    wrist_center = MTH6*SE3.Trans(-L4, 0, 0)
    pos_wrist_center =wrist_center.t

    x_c = pos_wrist_center[0]
    y_c = pos_wrist_center[1]
    z_c = pos_wrist_center[2]

    L = np.sqrt((z_c-L1)**2 + x_c**2 +y_c**2)
    
    # elbow up
    
    c_q3 = (L**2-(L2**2 + L3**2) )/(2*L2*L3)
    s_q3 = -np.sqrt(1 - c_q3**2)
    q3 = np.arctan2(s_q3,c_q3)
    
    alpha = np.arctan2(L3*c_q3 , L2 + L3*s_q3)
    gamma = np.arctan2(np.sqrt(x_c**2+y_c**2), z_c-L1  )
    
    q2 =  -gamma - alpha  #-pi/2
    
    
    q4 = q2-q3-theta

    #q_offset =np.array([0,pi/2,0,0])
    q = np.array([q1,q2,q3,q4])
    return q
    
    
yaw_deseado = radians(90)  # Convertir a radianes si estás trabajando con grados
pitch = 0  # Ángulo de Pitch inicial
# Rango de Pitch a barrer
roll_min = radians(-150)
roll_max = radians(150)
roll_step = radians(5)  # Definir un paso adecuado para el barrido

menor_error = 0.1
mejor_solucion = None
x,y,z = 10, 10, 10

for roll in np.arange(roll_min, roll_max, roll_step):
    T = SE3(x, y, z) * SE3.RPY([yaw_deseado, pitch, roll], order='zyx')
    R = T.R
    rot = SO3(R)

# Obtener el ángulo y eje de la matriz de rotación
    theta, axis = rot.angle_axis()

    print(theta)
    # solution = 
    # if solution.success and solution.residual < menor_error:
    #     mejor_solucion = solution
    #     menor_error = solution.residual
