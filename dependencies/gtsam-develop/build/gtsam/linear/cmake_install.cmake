# Install script for directory: /home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/linear" TYPE FILE FILES
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/AcceleratedPowerMethod.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/BinaryJacobianFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/ConjugateGradientSolver.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/Errors.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianBayesNet.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianBayesTree-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianBayesTree.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianConditional-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianConditional.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianDensity.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianEliminationTree.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianFactorGraph.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianISAM.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/GaussianJunctionTree.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/HessianFactor-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/HessianFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/IterativeSolver.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/JacobianFactor-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/JacobianFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/KalmanFilter.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/LossFunctions.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/NoiseModel.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/PCGSolver.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/PowerMethod.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/Preconditioner.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/RegularHessianFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/RegularJacobianFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/Sampler.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/Scatter.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/SparseEigen.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/SubgraphBuilder.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/SubgraphPreconditioner.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/SubgraphSolver.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/VectorValues.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/iterative-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/iterative.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/linearAlgorithms-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/linear/linearExceptions.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/piyush/chall_ws/src/dependencies/gtsam-develop/build/gtsam/linear/tests/cmake_install.cmake")
endif()

