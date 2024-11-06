# Install script for directory: /home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/gtsam/geometry" TYPE FILE FILES
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/BearingRange.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Cal3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Cal3Bundler.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Cal3DS2.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Cal3DS2_Base.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Cal3Fisheye.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Cal3Unified.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Cal3_S2.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Cal3_S2Stereo.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/CalibratedCamera.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/CameraSet.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Cyclic.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/EssentialMatrix.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Line3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/OrientedPlane3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/PinholeCamera.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/PinholePose.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/PinholeSet.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Point2.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Point3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Pose2.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Pose3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Quaternion.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Rot2.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Rot3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/SO3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/SO4.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/SOn-inl.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/SOn.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Similarity2.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Similarity3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/SimpleCamera.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/SphericalCamera.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/StereoCamera.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/StereoPoint2.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/Unit3.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/concepts.h"
    "/home/piyush/chall_ws/src/dependencies/gtsam-develop/gtsam/geometry/triangulation.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/home/piyush/chall_ws/src/dependencies/gtsam-develop/build/gtsam/geometry/tests/cmake_install.cmake")
endif()

