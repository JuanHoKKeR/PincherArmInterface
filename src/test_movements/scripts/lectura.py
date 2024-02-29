#!/usr/bin/env python
import rospy
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

def listener():
    rospy.init_node('joint_states_listener', anonymous=True)
    rospy.Subscriber("/joint_states", JointState, joint_states_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
