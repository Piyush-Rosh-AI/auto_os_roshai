#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "metis-gtsam" for configuration "Release"
set_property(TARGET metis-gtsam APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(metis-gtsam PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmetis-gtsam.a"
  )

list(APPEND _cmake_import_check_targets metis-gtsam )
list(APPEND _cmake_import_check_files_for_metis-gtsam "${_IMPORT_PREFIX}/lib/libmetis-gtsam.a" )

# Import target "cephes-gtsam" for configuration "Release"
set_property(TARGET cephes-gtsam APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(cephes-gtsam PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libcephes-gtsam.so.1.0.0"
  IMPORTED_SONAME_RELEASE "libcephes-gtsam.so.1"
  )

list(APPEND _cmake_import_check_targets cephes-gtsam )
list(APPEND _cmake_import_check_files_for_cephes-gtsam "${_IMPORT_PREFIX}/lib/libcephes-gtsam.so.1.0.0" )

# Import target "CppUnitLite" for configuration "Release"
set_property(TARGET CppUnitLite APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(CppUnitLite PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libCppUnitLite.a"
  )

list(APPEND _cmake_import_check_targets CppUnitLite )
list(APPEND _cmake_import_check_files_for_CppUnitLite "${_IMPORT_PREFIX}/lib/libCppUnitLite.a" )

# Import target "gtsam" for configuration "Release"
set_property(TARGET gtsam APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(gtsam PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libgtsam.so.4.3a0"
  IMPORTED_SONAME_RELEASE "libgtsam.so.4"
  )

list(APPEND _cmake_import_check_targets gtsam )
list(APPEND _cmake_import_check_files_for_gtsam "${_IMPORT_PREFIX}/lib/libgtsam.so.4.3a0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
