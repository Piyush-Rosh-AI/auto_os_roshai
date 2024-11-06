# Install script for directory: /home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/CCOLAMD" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/CCOLAMD/Include/ccolamd.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/SuiteSparse_config" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/SuiteSparse_config/SuiteSparse_config.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/Cholesky")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/CholmodSupport")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/Core")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/Dense")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/Eigen")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/Eigenvalues")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/Geometry")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/Householder")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/IterativeLinearSolvers")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/Jacobi")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/KLUSupport")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/LU")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/MetisSupport")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/OrderingMethods")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/PaStiXSupport")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/PardisoSupport")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/QR")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/QtAlignedMalloc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/SPQRSupport")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/SVD")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/Sparse")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/SparseCholesky")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/SparseCore")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/SparseLU")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/SparseQR")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/StdDeque")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/StdList")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/StdVector")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/SuperLUSupport")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen/Eigen" TYPE FILE FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen/UmfPackSupport")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/3rdparty/Eigen" TYPE DIRECTORY FILES "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/3rdparty/Eigen/Eigen" FILES_MATCHING REGEX "/[^/]*\\.h$")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/piyush/chall_ws/src/dependencies/gtsam-develop/build/gtsam/3rdparty/ceres/cmake_install.cmake")
endif()

