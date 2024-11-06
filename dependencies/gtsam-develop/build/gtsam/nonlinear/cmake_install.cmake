# Install script for directory: /home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/nonlinear" TYPE FILE FILES
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/AdaptAutoDiff.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/BatchFixedLagSmoother.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/CustomFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/DoglegOptimizer.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/DoglegOptimizerImpl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/Expression-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/Expression.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ExpressionFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ExpressionFactorGraph.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ExtendedKalmanFilter-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ExtendedKalmanFilter.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/FixedLagSmoother.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/FunctorizedFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/GaussNewtonOptimizer.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/GncOptimizer.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/GncParams.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/GraphvizFormatting.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ISAM2-impl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ISAM2.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ISAM2Clique.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ISAM2Params.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ISAM2Result.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/ISAM2UpdateParams.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/LevenbergMarquardtOptimizer.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/LevenbergMarquardtParams.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/LinearContainerFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/Marginals.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/NonlinearConjugateGradientOptimizer.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/NonlinearEquality.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/NonlinearFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/NonlinearFactorGraph.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/NonlinearISAM.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/NonlinearOptimizer.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/NonlinearOptimizerParams.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/PriorFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/Symbol.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/Values-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/Values.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/WhiteNoiseFactor.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/expressionTesting.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/expressions.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/factorTesting.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/nonlinearExceptions.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/utilities.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/nonlinear/internal" TYPE FILE FILES
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/internal/CallRecord.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/internal/ChiSquaredInverse.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/internal/ExecutionTrace.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/internal/ExpressionNode.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/internal/JacobianMap.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/internal/LevenbergMarquardtState.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/nonlinear/internal/NonlinearOptimizerState.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/piyush/chall_ws/src/dependencies/gtsam-develop/build/gtsam/nonlinear/tests/cmake_install.cmake")
endif()

