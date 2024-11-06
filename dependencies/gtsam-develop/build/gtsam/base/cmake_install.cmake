# Install script for directory: /home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/base" TYPE FILE FILES
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/ConcurrentMap.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/DSFMap.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/DSFVector.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/FastDefaultAllocator.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/FastList.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/FastMap.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/FastSet.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/FastVector.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/GenericValue.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/Group.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/Lie.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/Manifold.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/Matrix.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/MatrixSerialization.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/OptionalJacobian.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/ProductLieGroup.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/SymmetricBlockMatrix.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/Testable.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/TestableAssertions.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/ThreadsafeException.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/Value.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/Vector.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/VectorSerialization.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/VectorSpace.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/VerticalBlockMatrix.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/WeightedSampler.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/chartTesting.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/cholesky.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/concepts.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/debug.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/kruskal-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/kruskal.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/lieProxies.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/make_shared.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/numericalDerivative.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/serialization.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/serializationTestHelpers.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/std_optional_serialization.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/testLie.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/timing.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/treeTraversal-inst.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/types.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/utilities.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/base/treeTraversal" TYPE FILE FILES
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/treeTraversal/parallelTraversalTasks.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/base/treeTraversal/statistics.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/piyush/chall_ws/src/dependencies/gtsam-develop/build/gtsam/base/tests/cmake_install.cmake")
endif()

