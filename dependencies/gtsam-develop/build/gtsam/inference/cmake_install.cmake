# Install script for directory: /home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/inference" TYPE FILE FILES
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/BayesNet-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/BayesNet.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/BayesTree-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/BayesTree.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/BayesTreeCliqueBase-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/BayesTreeCliqueBase.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/ClusterTree-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/ClusterTree.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/Conditional-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/Conditional.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/DotWriter.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/EliminateableFactorGraph-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/EliminateableFactorGraph.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/EliminationTree-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/EliminationTree.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/Factor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/FactorGraph-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/FactorGraph.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/ISAM-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/ISAM.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/JunctionTree-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/JunctionTree.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/Key.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/LabeledSymbol.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/MetisIndex-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/MetisIndex.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/Ordering.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/Symbol.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/VariableIndex-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/VariableIndex.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/VariableSlots.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/graph-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/graph.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/inference-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/inference/inferenceExceptions.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/piyush/chall_ws/src/dependencies/gtsam-develop/build/gtsam/inference/tests/cmake_install.cmake")
endif()

