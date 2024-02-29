#!/usr/bin/env python
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

def create_joint_trajectory_goal():
    # Crear el objetivo de trayectoria
    goal = FollowJointTrajectoryGoal()
    trajectory = JointTrajectory()

    # Especificar los nombres de las articulaciones
    trajectory.joint_names = [
        "arm_shoulder_pan_joint",
        "arm_shoulder_lift_joint",
        "arm_elbow_flex_joint",
        "arm_wrist_flex_joint",
        "gripper_joint"
    ]

    # Definir los puntos de la trayectoria
    # Asegúrate de que los valores estén dentro de los límites definidos en el archivo YAML
    points = [
        # JointTrajectoryPoint(positions=[0.0, 0.0, 0.0, 0.0, 0.0], time_from_start=rospy.Duration(2.0)),
        # JointTrajectoryPoint(positions=[0.1, -1, 1.0, 0.8, 0.6], time_from_start=rospy.Duration(5.0)),
        # JointTrajectoryPoint(positions=[-1.6, 1.10, 1.50, 1.9, 0.0], time_from_start=rospy.Duration(8.0)),
        # JointTrajectoryPoint(positions=[0.0, 0.0, 0.0, 0.0, 0.0], time_from_start=rospy.Duration(11.0)),
        # JointTrajectoryPoint(positions=[-1.6, 1.60, 0.0, 1.3, 0.0], time_from_start=rospy.Duration(14.0)),
        # JointTrajectoryPoint(positions=[0.0, 0.0, 0.0, 0.0, 0.0], time_from_start=rospy.Duration(17.0)),
        # JointTrajectoryPoint(positions=[-1.3, -0.20, 0.80, 0.70, 0.50], time_from_start=rospy.Duration(18.0)),
        # JointTrajectoryPoint(positions=[0.80, 0.0, 0.710, 0.80, 1.0], time_from_start=rospy.Duration(19.0)),
        # JointTrajectoryPoint(positions=[0.0, -0.730, 1.740, -1.170, -0.390], time_from_start=rospy.Duration(20.0)),
        # JointTrajectoryPoint(positions=[-2.0, -0.730, 1.740, -1.170, -0.390], time_from_start=rospy.Duration(21.0)),
        # JointTrajectoryPoint(positions=[0.10, 0.50, -2.120, 1.430, 1.0], time_from_start=rospy.Duration(22.0)),
        JointTrajectoryPoint(positions=[-1.88916670e+00,  1.95548909e+00, -1.97670153e+00,  3.19680376e-04], time_from_start=rospy.Duration(2)),
        JointTrajectoryPoint(positions=[-1.84677193, -0.43114061, 2.18072268, -1.24575745], time_from_start=rospy.Duration(4)),
        JointTrajectoryPoint(positions=[-1.78038571, 1.75924763, -2.13659485, 0.91090314], time_from_start=rospy.Duration(6)),
        JointTrajectoryPoint(positions=[-1.70154903, 1.83131266, -2.08036648, 0.70626059], time_from_start=rospy.Duration(8)),
        JointTrajectoryPoint(positions=[-1.61637789, -0.13031216, 2.01910645, -1.52826993], time_from_start=rospy.Duration(10)),
        JointTrajectoryPoint(positions=[-1.52948536, -0.07728521, 1.98921624, -1.60855413], time_from_start=rospy.Duration(12)),
        JointTrajectoryPoint(positions=[-1.44443691, -0.00954593, 1.94804, -1.73783211], time_from_start=rospy.Duration(14)),
        JointTrajectoryPoint(positions=[-1.36423634, 1.92802131, -1.73019735, -0.30526372], time_from_start=rospy.Duration(16)),
        JointTrajectoryPoint(positions=[-1.29938424, 1.9543038, -1.9542144, 0.0527922], time_from_start=rospy.Duration(18)),
        JointTrajectoryPoint(positions=[-1.25250626, 1.95291706, -2.02017939, 0.0963701], time_from_start=rospy.Duration(20)),




        # Añade más puntos según sea necesario
    ]

    # Asignar los puntos a la trayectoria
    trajectory.points = points
    goal.trajectory = trajectory

    return goal

def send_trajectory_goal():
    rospy.init_node('send_joint_trajectory')

    # Conectar al servidor de acción usando el nombre de acción correcto
    client = actionlib.SimpleActionClient('/arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    rospy.loginfo("Esperando al servidor de acción...")
    client.wait_for_server()

    # Enviar el objetivo de trayectoria
    goal = create_joint_trajectory_goal()
    rospy.loginfo("Enviando objetivo de trayectoria...")
    client.send_goal(goal)

    # Esperar a que la acción se complete
    client.wait_for_result()
    rospy.loginfo("Trayectoria completada.")

if __name__ == '__main__':
    send_trajectory_goal()
