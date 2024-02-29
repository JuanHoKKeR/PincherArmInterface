#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState


# Lista de las articulaciones de interés
joint_names_of_interest = [
    'gripper_joint',
    'arm_wrist_flex_joint',
    'arm_elbow_flex_joint',
    'arm_shoulder_lift_joint',
    'arm_shoulder_pan_joint'
]

def joint_states_callback(message):
    # Crear una lista para guardar las articulaciones de interés que están presentes en el mensaje
    filtered_joints = [(name, position) for name, position in zip(message.name, message.position) if name in joint_names_of_interest]

    # Solo imprimir si hay articulaciones de interés en el mensaje
    if filtered_joints:
        print("Joint States:")
        for name, position in filtered_joints:
            print(f"  {name}: {position}")


def jointCommand(joint_name, position):
    pub = rospy.Publisher(f'/{joint_name}/command', Float64, queue_size=10)
    pub.publish(position)
    rospy.sleep(1)

def move_servo():
    # Solicitar la selección del servo
    input_joint = int(input("Ingrese el índice del servo a mover (empezando por 0, o -1 para salir): "))
    if input_joint == -1:
        return  # Salir de la función si se ingresa -1

    if input_joint >= 0 and input_joint < len(articulaciones):
        position = float(input("Ingrese la posición deseada: "))
        jointCommand(articulaciones[input_joint], position)  # Mover el servo seleccionado
        #joint_states_callback(rospy.wait_for_message("/joint_states", JointState))  # Mostrar posiciones después de la acción
    else:
        print("Índice de articulación inválido.")

    # Llamar recursivamente a la función para solicitar la selección del servo nuevamente
    move_servo()

if __name__ == "__main__":
    rospy.init_node('joint_position_commander', anonymous=True)
    rospy.Subscriber("/joint_states", JointState, joint_states_callback)

    articulaciones = ["arm_shoulder_pan_joint", "arm_shoulder_lift_joint", "arm_elbow_flex_joint", "arm_wrist_flex_joint", "gripper_joint"]
    
    # Mostrar posiciones actuales de los servos una vez al inicio
    
    #joint_states_callback(rospy.wait_for_message("/joint_states", JointState))

    # Comenzar la selección y movimiento del servo
    move_servo()
