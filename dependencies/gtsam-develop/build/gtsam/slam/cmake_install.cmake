# Install script for directory: /home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
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

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/slam" TYPE FILE FILES
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/AntiFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/BearingFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/BearingRangeFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/BetweenFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/BoundingConstraint.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/EssentialMatrixConstraint.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/EssentialMatrixFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/FrobeniusFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/GeneralSFMFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/InitializePose.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/InitializePose3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/JacobianFactorQ.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/JacobianFactorQR.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/JacobianFactorSVD.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/KarcherMeanFactor-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/KarcherMeanFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/OrientedPlane3Factor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/PoseRotationPrior.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/PoseTranslationPrior.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/PriorFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/ProjectionFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/RangeFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/ReferenceFrameFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/RegularImplicitSchurFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/RotateFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/SmartFactorBase.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/SmartFactorParams.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/SmartProjectionFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/SmartProjectionPoseFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/SmartProjectionRigFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/StereoFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/TriangulationFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/dataset.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/expressions.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/slam/lago.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/piyush/chall_ws/src/dependencies/gtsam-develop/build/gtsam/slam/tests/cmake_install.cmake")
endif()

