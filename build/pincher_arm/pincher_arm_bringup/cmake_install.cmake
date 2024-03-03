# Install script for directory: /home/juancruz/PincherArm_catkin_ws/src/pincher_arm/pincher_arm_bringup

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/juancruz/PincherArm_catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/juancruz/PincherArm_catkin_ws/build/pincher_arm/pincher_arm_bringup/catkin_generated/installspace/pincher_arm_bringup.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pincher_arm_bringup/cmake" TYPE FILE FILES
    "/home/juancruz/PincherArm_catkin_ws/build/pincher_arm/pincher_arm_bringup/catkin_generated/installspace/pincher_arm_bringupConfig.cmake"
    "/home/juancruz/PincherArm_catkin_ws/build/pincher_arm/pincher_arm_bringup/catkin_generated/installspace/pincher_arm_bringupConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pincher_arm_bringup" TYPE FILE FILES "/home/juancruz/PincherArm_catkin_ws/src/pincher_arm/pincher_arm_bringup/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pincher_arm_bringup" TYPE DIRECTORY FILES "/home/juancruz/PincherArm_catkin_ws/src/pincher_arm/pincher_arm_bringup/config")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pincher_arm_bringup" TYPE DIRECTORY FILES "/home/juancruz/PincherArm_catkin_ws/src/pincher_arm/pincher_arm_bringup/launch")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pincher_arm_bringup" TYPE PROGRAM FILES "/home/juancruz/PincherArm_catkin_ws/build/pincher_arm/pincher_arm_bringup/catkin_generated/installspace/fake_joint_pub")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pincher_arm_bringup" TYPE PROGRAM FILES "/home/juancruz/PincherArm_catkin_ws/build/pincher_arm/pincher_arm_bringup/catkin_generated/installspace/gripper_controller")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pincher_arm_bringup" TYPE PROGRAM FILES "/home/juancruz/PincherArm_catkin_ws/build/pincher_arm/pincher_arm_bringup/catkin_generated/installspace/gripper_transmission")
endif()

