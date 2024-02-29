#!/bin/bash
# Este script inicia roscore, el roslaunch para el robot, y luego ejecuta un script de Python.

echo "Iniciando roscore..."
roscore &
# Espera un poco para asegurarse de que roscore esté completamente iniciado
sleep 5

echo "Iniciando el roslaunch para el robot..."
# Asegúrate de reemplazar 'tu_paquete' y 'arm.launch' con los nombres correctos
roslaunch pincher_arm_bringup arm.launch & 
sleep 10 # Ajusta este tiempo según lo que necesite tu sistema para iniciar completamente

echo "Iniciando el proyecto..."
# Asegúrate de reemplazar 'test_movements' y 'Interface.py' con los nombres correctos
rosrun test_movements Interface.py

