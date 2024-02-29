#!/usr/bin/env python
import rospy
import numpy as np
import roboticstoolbox as rtb
from sensor_msgs.msg import JointState
from roboticstoolbox import *

from numpy import pi

from spatialmath import SE3
from spatialmath.base import tr2rpy


# Definición de la matriz DH del robot
def define_robot():
    qlim1, qlim2, qlim3, qlim4 = [-2.6, 2.6], [-2.0, 2.0], [-2.5, 2.5], [-1.8, 1.8]
    #L1, L2, L3, L4 = 138, 108, 108, 110
    L1, L2, L3, L4 = 14.3, 10.7, 10.7, 9.0
    #L1, L2, L3, L4 = 14.5, 10.7, 10.7, 9

    # Creación de los eslabones y del robot
    Link1 = rtb.DHLink(d=L1, a=0, alpha=np.pi/2, qlim=qlim1)
    Link2 = rtb.DHLink(d=0, a=L2, alpha=0, offset=np.pi/2, qlim=qlim2)
    Link3 = rtb.DHLink(d=0, a=L3, alpha=0, qlim=qlim3)
    Link4 = rtb.DHLink(d=0, a=L4, alpha=0, qlim=qlim4)
    robot = rtb.DHRobot([Link1, Link2, Link3, Link4], name='Pincher rtb')
    return robot

# Inicializa el robot
robot = define_robot()

# Inicializa las posiciones de las articulaciones
joint_positions = [0, 0, 0, 0]

# Nombres de las articulaciones de interés
joint_names_of_interest = [
    'arm_shoulder_pan_joint',
    'arm_shoulder_lift_joint',
    'arm_elbow_flex_joint',
    'arm_wrist_flex_joint'
]

# Callback para actualizar las posiciones de las articulaciones
def joint_state_callback(data):
    global joint_positions
    try:
        positions = [data.position[data.name.index(joint)] for joint in joint_names_of_interest]
        if len(positions) == 4:
            joint_positions = positions

            # Calcula la matriz de transformación homogénea
            T = robot.fkine(joint_positions)
            print("Matriz de transformación homogénea:\n", T)
            # print("Pasando la matriz de transformación homogénea a ikine")
            # q_out = robot.ikine_LM(T)
            # print(f"q_out: {q_out.q}")
            # print("Comporbacíon de q_out")
            # T_out = robot.fkine(q_out.q)
            # print(T_out)
            x, y, z = T.t
            rpy = tr2rpy(T.A, unit='deg')  # Asume que deseas los ángulos en grados. Usa 'rad' para radianes.
            roll, pitch, yaw = rpy
            print(f"Posición: ({x}, {y}, {z})")
            print(f"Orientación: ({roll}, {pitch}, {yaw})")
            print(f'RPY: {rpy}')
            
    except ValueError:
        pass  # Ignora si algún nombre de articulación no se encuentra

# Inicialización del nodo de ROS
def listener():
    rospy.init_node('robot_fkine_calculator', anonymous=True)
    rospy.Subscriber("/joint_states", JointState, joint_state_callback)
    rospy.spin()  # Mantiene el nodo ejecutándose
    
    

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
