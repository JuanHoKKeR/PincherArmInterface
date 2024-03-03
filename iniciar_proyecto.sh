#!/bin/bash

# Función para manejar el cierre de los procesos
cleanup() {
    echo "Cerrando nodos y roscore..."
    # Envía señal de terminación a los procesos iniciados
    killall -q roslaunch
    killall -q rosrun
    killall -q roscore
    exit 0
}

# Captura las señales SIGINT y SIGTERM y las redirige a la función 'cleanup'
trap cleanup SIGINT SIGTERM

echo "Iniciando roscore..."
roscore &
roscore_pid=$!
sleep 5

echo "Iniciando el roslaunch para el robot..."
roslaunch pincher_arm_bringup arm.launch &
roslaunch_pid=$!
sleep 10

echo "Iniciando visualización para el robot..."
roslaunch pincher_arm_moveit_config pincher_arm_moveit.launch sim:=false &
roslaunch_pid=$!
sleep 10

echo "Iniciando el proyecto..."
rosrun test_movements Interface.py &
rosrun_pid=$!

# Espera a que el script de Python finalice
wait $rosrun_pid

# Limpieza final
cleanup
