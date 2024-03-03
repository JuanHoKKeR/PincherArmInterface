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
        JointTrajectoryPoint(positions=[0.830, -1.083, -1.545, 1.057], time_from_start=rospy.Duration(1)),
        JointTrajectoryPoint(positions=[0.834, -1.089, -1.528, 1.046], time_from_start=rospy.Duration(2)),
        JointTrajectoryPoint(positions=[0.842, -1.108, -1.475, 1.013], time_from_start=rospy.Duration(3)),
        JointTrajectoryPoint(positions=[0.847, -1.141, -1.388, 0.958], time_from_start=rospy.Duration(4)),
        JointTrajectoryPoint(positions=[0.844, -1.186, -1.276, 0.891], time_from_start=rospy.Duration(5)),
        JointTrajectoryPoint(positions=[0.831, -1.236, -1.154, 0.819], time_from_start=rospy.Duration(6)),
        JointTrajectoryPoint(positions=[0.808, -1.282, -1.045, 0.756], time_from_start=rospy.Duration(7)),
        JointTrajectoryPoint(positions=[0.778, -1.315, -0.970, 0.714], time_from_start=rospy.Duration(8)),
        JointTrajectoryPoint(positions=[0.745, -1.324, -0.948, 0.702], time_from_start=rospy.Duration(9)),
        JointTrajectoryPoint(positions=[0.712, -1.307, -0.988, 0.724], time_from_start=rospy.Duration(10)),
        JointTrajectoryPoint(positions=[0.685, -1.267, -1.082, 0.777], time_from_start=rospy.Duration(11)),
        JointTrajectoryPoint(positions=[0.664, -1.211, -1.213, 0.854], time_from_start=rospy.Duration(12)),
        JointTrajectoryPoint(positions=[0.651, -1.150, -1.365, 0.944], time_from_start=rospy.Duration(13)),
        JointTrajectoryPoint(positions=[0.644, -1.091, -1.520, 1.041], time_from_start=rospy.Duration(14)),
        JointTrajectoryPoint(positions=[0.640, -1.041, -1.667, 1.137], time_from_start=rospy.Duration(15)),
        JointTrajectoryPoint(positions=[0.636, -1.001, -1.796, 1.226], time_from_start=rospy.Duration(16)),
        JointTrajectoryPoint(positions=[0.629, -0.974, -1.899, 1.302], time_from_start=rospy.Duration(17)),
        JointTrajectoryPoint(positions=[0.619, -0.957, -1.973, 1.359], time_from_start=rospy.Duration(18)),
        JointTrajectoryPoint(positions=[0.607, -0.949, -2.018, 1.395], time_from_start=rospy.Duration(19)),
        JointTrajectoryPoint(positions=[0.599, -0.945, -2.036, 1.411], time_from_start=rospy.Duration(20)),
        JointTrajectoryPoint(positions=[0.599, -0.945, -2.037, 1.411], time_from_start=rospy.Duration(21)),
        JointTrajectoryPoint(positions=[0.611, -0.947, -2.029, 1.404], time_from_start=rospy.Duration(22)),
        JointTrajectoryPoint(positions=[0.636, -0.948, -2.021, 1.398], time_from_start=rospy.Duration(23)),
        JointTrajectoryPoint(positions=[0.673, -0.948, -2.021, 1.398], time_from_start=rospy.Duration(24)),
        JointTrajectoryPoint(positions=[0.722, -0.946, -2.030, 1.405], time_from_start=rospy.Duration(25)),
        JointTrajectoryPoint(positions=[0.778, -0.945, -2.040, 1.414], time_from_start=rospy.Duration(26)),
        JointTrajectoryPoint(positions=[0.839, -0.944, -2.046, 1.419], time_from_start=rospy.Duration(27)),
        JointTrajectoryPoint(positions=[0.898, -0.946, -2.035, 1.410], time_from_start=rospy.Duration(28)),
        JointTrajectoryPoint(positions=[0.950, -0.952, -2.000, 1.381], time_from_start=rospy.Duration(29)),
        JointTrajectoryPoint(positions=[0.987, -0.965, -1.937, 1.331], time_from_start=rospy.Duration(30)),
        JointTrajectoryPoint(positions=[1.007, -0.986, -1.850, 1.265], time_from_start=rospy.Duration(31)),
        JointTrajectoryPoint(positions=[1.009, -1.016, -1.746, 1.191], time_from_start=rospy.Duration(32)),
        JointTrajectoryPoint(positions=[0.996, -1.049, -1.641, 1.120], time_from_start=rospy.Duration(33)),
        JointTrajectoryPoint(positions=[0.973, -1.080, -1.551, 1.061], time_from_start=rospy.Duration(34)),
        JointTrajectoryPoint(positions=[0.942, -1.103, -1.490, 1.022], time_from_start=rospy.Duration(35)),
        JointTrajectoryPoint(positions=[0.908, -1.112, -1.466, 1.007], time_from_start=rospy.Duration(36)),
        JointTrajectoryPoint(positions=[0.876, -1.109, -1.474, 1.012], time_from_start=rospy.Duration(37)),
        JointTrajectoryPoint(positions=[0.851, -1.098, -1.502, 1.030], time_from_start=rospy.Duration(38)),
        JointTrajectoryPoint(positions=[0.835, -1.087, -1.532, 1.048], time_from_start=rospy.Duration(39)),
        JointTrajectoryPoint(positions=[0.830, -1.083, -1.545, 1.057], time_from_start=rospy.Duration(40)),








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
