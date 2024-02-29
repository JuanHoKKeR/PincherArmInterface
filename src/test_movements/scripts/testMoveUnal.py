import numpy as np
from spatialmath import SE3
from roboticstoolbox import DHRobot, RevoluteDH


# Longitudes de los eslabones
L1, L2, L3, L4 = 138, 108, 108, 110

# Límites de los ángulos de las articulaciones
qlim1, qlim2, qlim3, qlim4 = [-2.6, 2.6], [-2.0, 2.0], [-2.5, 2.5], [-1.8, 1.8]

# Matriz objetivo T_target
T = np.array([
    [0.04609, 0.2846, 0.9575, 32.25],
    [0.1531, 0.9452, -0.2883, 107.1],
    [-0.9871, 0.1599, 0, 165.4],
    [0, 0, 0, 1]
])

# Creación de la pose objetivo como un objeto SE3
T_target = SE3(T, check=False)

# Definición del robot
robot = DHRobot([
    RevoluteDH(d=L1, a=0, alpha=np.pi/2, qlim=qlim1),
    RevoluteDH(a=L2, alpha=0, qlim=qlim2),
    RevoluteDH(a=L3, alpha=0, qlim=qlim3),
    RevoluteDH(d=0, a=L4, alpha=0, qlim=qlim4)
], name='CustomRobot')

# Uso de ikine_LM para resolver la cinemática inversa
sol = robot.ikine_LM(T_target)

if sol.success:
    print(f"Solución encontrada: {sol.q}")
    # Verificación con cinemática directa
    T_result = robot.fkine(sol.q)
    print("Resultado de T con cinemática directa:\n", T_result)
else:
    print("No se pudo encontrar una solución.")