#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

def jointCommand(joint_name, position):
    # Crear el publicador fuera del bucle
    pub = rospy.Publisher(f'/{joint_name}/command', Float64, queue_size=10)
    rospy.sleep(0.5)  # Dar tiempo para que el publicador se establezca

    # Publicar un único comando
    pub.publish(position)
    rospy.loginfo(f"Comando enviado a {joint_name}: {position}")

if __name__ == "__main__":
    rospy.init_node('joint_position_commander', anonymous=True)

    articulaciones = ["arm_shoulder_pan_joint", "arm_shoulder_lift_joint", "arm_elbow_flex_joint", "arm_wrist_flex_joint", "gripper_joint"]
    input_joint = int(input("Ingrese el índice del servo a mover (empezando por 0): "))
    position = float(input("Ingrese la posición deseada: "))

    if 0 <= input_joint < len(articulaciones):
        jointCommand(articulaciones[input_joint], position)
    else:
        print("Índice de articulación inválido.")
