#!/usr/bin/env python
from SimpleInterfaz import *
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState  # Importa JointState
from arbotix_msgs.srv import Relax
import roboticstoolbox as rtb
from roboticstoolbox import *
import numpy as np
from numpy import pi
from spatialmath import SE3
from spatialmath.base import tr2rpy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math
from math import radians, degrees

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.ReEna.clicked.connect(self.relaxAllServos)
        self.Home.clicked.connect(self.Set_Home)
        self.Calculate.clicked.connect(self.calculate_inverse_kinematics)

        
        self.publishers = {
            "gripper_joint": rospy.Publisher('gripper_joint/command', Float64, queue_size=10),
            "arm_wrist_flex_joint": rospy.Publisher('arm_wrist_flex_joint/command', Float64, queue_size=10),
            "arm_elbow_flex_joint": rospy.Publisher('arm_elbow_flex_joint/command', Float64, queue_size=10),
            "arm_shoulder_lift_joint": rospy.Publisher('arm_shoulder_lift_joint/command', Float64, queue_size=10),
            "arm_shoulder_pan_joint": rospy.Publisher('arm_shoulder_pan_joint/command', Float64, queue_size=10)
        }

        self.control_info = {
            self.Gripper: ("gripper_joint", self.LabelGripper, self.ButtonGrip),
            self.Wrist: ("arm_wrist_flex_joint", self.LabelWrist, self.ButtonWrist),
            self.Elbow: ("arm_elbow_flex_joint", self.LabelElbow, self.ButtonElbow),
            self.Shoulder: ("arm_shoulder_lift_joint", self.LabelShoulder, self.ButtonShoulder),
            self.Pan: ("arm_shoulder_pan_joint", self.LabelPan, self.ButtonPan),
        }

        self.joint_names_of_interest = [
            'arm_shoulder_pan_joint',
            'arm_shoulder_lift_joint',
            'arm_elbow_flex_joint',
            'arm_wrist_flex_joint'
        ]
        
        self.Home = [
            JointTrajectoryPoint(positions=[0.0, 0.0, 0.0, 0.0, 0.0], time_from_start=rospy.Duration(2.0))
        ]
       
        for slider, (joint_name, label, button) in self.control_info.items():
            slider.valueChanged.connect(lambda value, s=slider, j=joint_name, l=label: self.updateJointPosition(s, j, l))
            button.clicked.connect(lambda checked, b=button, s=slider: self.toggleControl(b, s))
            slider.setEnabled(False)
            slider.setStyleSheet("background-color: rgb(200, 200, 200);")
            button.setText("OFF")

        # Suscribir al tópico /joint_states
        rospy.Subscriber("/joint_states", JointState, self.jointStateCallback)
        self.joint_positions = {}  # Almacena las últimas posiciones conocidas de las articulaciones
        self.joint_kinematics = {}  # Almacena las últimas posiciones conocidas de las articulaciones
        self.robot = self.define_robot()
        self.soluctionINV = []


    def define_robot(self):
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
    
    
    def jointStateCallback(self, msg):
        # Actualiza el diccionario con las posiciones actuales de las articulaciones
        for name, position in zip(msg.name, msg.position):
            self.joint_positions[name] = position
            if name in self.joint_names_of_interest:
                self.joint_kinematics[name] = position
                #print(f"Updated {name} to {position}")
        # Actualiza los labels con las nuevas posiciones
        self.updateLabels()
        self.updateDirectKinematicsLabels()

    def updateLabels(self):
        # Actualiza los labels con las posiciones actuales de las articulaciones
        for control, (joint_name, label, button) in self.control_info.items():
            if joint_name in self.joint_positions:
                # Obtiene la posición actual de la articulación
                position = self.joint_positions[joint_name]
                position_deg = math.degrees(position)
                # Actualiza el texto del label con la posición
                readable_name = ' '.join(word.capitalize() for word in joint_name.split('_')[0:-1])
                label.setText(f"{readable_name}: {position_deg:.3f}°")
                
                # Si el botón asociado al slider está en "OFF", actualiza la posición del slider
                if button.text() == "OFF":
                    slider_value = int(position * 100)
                    control.setValue(slider_value)
                
    
    def updateJointPosition(self, slider, joint_name, label):
        # Solo publica si el slider está habilitado
        if slider.isEnabled():
            value = slider.value() / 100.0
            self.publishers[joint_name].publish(Float64(value))

                
    
    def toggleControl(self, button, slider):
        if button.text() == "OFF":
            button.setText("ON")
            button.setStyleSheet("QPushButton{\n"
"    font: 81 8pt \"Rockwell Extra Bold\";\n"
"    text-decoration: underline;\n"
"    border: 1.5px solid black;\n"
"    border-top-right-radius :10px;\n"
"    border-bottom-right-radius : 15px;\n"
"    min-width: 1em;\n"
"    padding: 5px;\n"
"    background-color: red;\n"
"}\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"}")
            slider.setEnabled(True)
            slider.setStyleSheet("background-color: rgb(255, 180, 75);")
        else:
            button.setText("OFF")
            button.setStyleSheet("QPushButton{\n"
"    font: 81 8pt \"Rockwell Extra Bold\";\n"
"    text-decoration: underline;\n"
"    border: 1.5px solid black;\n"
"    border-top-right-radius :10px;\n"
"    border-bottom-right-radius : 15px;\n"
"    min-width: 1em;\n"
"    padding: 5px;\n"
"    background-color: rgb(223, 223, 223);\n"
"}\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"}")
            slider.setEnabled(False)
            slider.setStyleSheet("background-color: rgb(200, 200, 200);")

    def relaxAllServos(self):
        rospy.wait_for_service('/servos/relax_all')
        try:
            relax_all = rospy.ServiceProxy('/servos/relax_all', Relax)
            resp = relax_all()  # Llama al servicio sin argumentos
            rospy.loginfo("Todos los servos han sido relajados.")
            # Después de relajar los servos, desactiva los controles
            for _, (_, _, button) in self.control_info.items():
                if button.text() == "ON":
                    button.click()  # Simula un clic en el botón para cambiar su estado a OFF
            
        except rospy.ServiceException as e:
            rospy.logerr("El servicio relax_all falló: " + str(e))


    def updateDirectKinematicsLabels(self):
        positions = [self.joint_kinematics.get(joint) for joint in self.joint_names_of_interest]
        # Verifica si alguna de las posiciones es None (indicando que no todos los datos han sido recibidos aún)
        if None in positions:
            print("Aún faltan datos de algunas articulaciones.")
            return
        # Continúa con el cálculo si todas las posiciones están presentes
        try:
            
            T = self.robot.fkine(positions)
            x, y, z = T.t
            ypr = tr2rpy(T.A, unit='deg')  # Asume que deseas los ángulos en grados. Usa 'rad' para radianes.
            yaw, pitch, roll = ypr
            self.Directa_X.setText(f"{x:.2f}")
            self.Directa_Y.setText(f"{y:.2f}")
            self.Directa_Z.setText(f"{z:.2f}")
            self.Directa_Roll.setText(f"{roll:.2f}")
            self.Directa_Pitch.setText(f"{pitch:.2f}")
            self.Directa_Yawl.setText(f"{yaw:.2f}")
        except Exception as e:
            print(f"Error al actualizar la cinemática directa: {e}")


    
        
    def create_joint_trajectory_goal(self, trajectory_points):
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
        # Asignar los puntos a la trayectoria
        trajectory.points = trajectory_points
        goal.trajectory = trajectory
        return goal
    

    def Set_Home(self):
        # Conectar al servidor de acción usando el nombre de acción correcto
        for _, (_, _, button) in self.control_info.items():
                if button.text() == "ON":
                    button.click()  # Simula un clic en el botón para cambiar su estado a OFF
        client = actionlib.SimpleActionClient('/arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
        rospy.loginfo("Esperando al servidor de acción...")
        client.wait_for_server()
        # Enviar el objetivo de trayectoria
        goal = self.create_joint_trajectory_goal(self.Home)
        rospy.loginfo("Enviando objetivo de trayectoria...")
        client.send_goal(goal)
        # Esperar a que la acción se complete
        client.wait_for_result()
        rospy.loginfo("Trayectoria completada.")
        
    def execute_trajectory(self):
        for _, (_, _, button) in self.control_info.items():
            if button.text() == "ON":
                button.click()  # Simula un clic en el botón para cambiar su estado a OFF  # Una función para deshabilitar botones durante la ejecución
        try:
            client = actionlib.SimpleActionClient('/arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
            client.wait_for_server()
            trajectoria = self.soluctionINV + [0.0]  # Asumiendo que quieres mantener el gripper estático
            Trajectory_calculated = [JointTrajectoryPoint(positions=trajectoria, time_from_start=rospy.Duration(2.0))]
            goal = self.create_joint_trajectory_goal(Trajectory_calculated)
            client.send_goal(goal)
            client.wait_for_result()
            rospy.loginfo("Trajectory executed successfully.")
        except Exception as e:
            rospy.logerr(f"Failed to execute trajectory: {e}")
        finally:
            self.clear_inputs_and_labels()  # Reactivar botones después de la ejecución



    def calculate_inverse_kinematics(self):
    # Inicialización de variables
        x = y = z = pitch = 0
        yaw = np.radians(90)
        roll_min = radians(-150)
        roll_max = radians(150)
        roll_step = radians(5)
        menor_error = 2
        mejor_solucion = None
        soluciones_validas = []
        # Validación y conversión de entradas
        try:
            x = float(self.Inverse_X.text())
            y = float(self.Inverse_Y.text())
            z = float(self.Inverse_Z.text())
            # Definir yaw, pitch, roll aquí si son obtenidos de la interfaz de usuario
        except ValueError as e:
            self.Advertencia.setText(f"Input error: {e}")
            return

        # Cálculo de la cinemática inversa
        try:
            for roll in np.arange(roll_min, roll_max, roll_step):
                T = SE3(x, y, z) * SE3.RPY([yaw, pitch, roll], order='zyx')
                solution = self.robot.ikine_LM(T, [0, 0, 0, 0], 15, 5, 0.01, True)
                if solution.success and solution.residual < menor_error:
                    mejor_solucion = solution
                    menor_error = solution.residual
            #T = SE3(x, y, z) * SE3.RPY([roll, pitch, yaw], order='zyx')
            #solution = self.robot.ikine_LM(T, [0, 0, 0, 0], 70, 120,1.5, True, None, None)   # Ajusta los argumentos según necesites
            #print(solution)
            #if solution.success:
            solution = mejor_solucion
            print(solution)
            if solution is not None:
                q_formatted = ", ".join([f"{q:.3f}" for q in solution.q])
                self.Advertencia.setText(f"Success! q: \n{q_formatted}")
                self.soluctionINV = solution.q
                self.Star.clicked.connect(self.execute_trajectory)
            else:
                raise ValueError("Failed to find a solution.")
            
        except Exception as e:
            self.Advertencia.setText(f"Calculation error:\n {e}")
            print(f"Calculation error:\n {e}")
            self.Star.setText("Clear")
            self.Star.clicked.connect(self.clear_inputs_and_labels)


    def clear_inputs_and_labels(self):
        self.Inverse_X.clear()
        self.Inverse_Y.clear()
        self.Inverse_Z.clear()
        self.Advertencia.setText("...")
        self.Star.setText("Star")
        
        
    
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    rospy.init_node('InterfazPincher', anonymous=True)
    window = MainWindow()
    window.show()
    app.exec_()
