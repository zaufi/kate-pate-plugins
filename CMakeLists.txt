#
# Copyright 2012 by Alex Trubov <i.zaufi@gmail.com>
#
# TODO Detect that Kate and Pâté are installed!
#

#---------------------------------------------------------
# Section: Init cmake
#---------------------------------------------------------
cmake_minimum_required(VERSION 2.8)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/modules" ${CMAKE_MODULE_PATH})

project(kate-pate-plugins NONE)

# Set project version numbers
set(VERSION_MAJOR 2)
set(VERSION_MINOR 0)
set(VERSION_PATCH 0)
set(VERSION_STRING ${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH})

#---------------------------------------------------------
# Section: Find used stuff
#---------------------------------------------------------
find_package(PythonInterp REQUIRED)

file(TO_CMAKE_PATH "$ENV{KDEDIRS}" _KDEDIRS)

# NOTE For KDE4 kde-config has been renamed to kde4-config
find_program(
    KDE4_KDECONFIG_EXECUTABLE
    NAMES kde4-config
    # the suffix must be used since KDEDIRS can be a list of directories which don't have bin/ appended
    PATH_SUFFIXES bin
    HINTS
    ${_KDEDIRS}
    /opt/kde4
    ONLY_CMAKE_FIND_ROOT_PATH
  )
if(NOT KDE4_KDECONFIG_EXECUTABLE)
    message(FATAL_ERROR "ERROR: Could not find KDE4 kde4-config")
endif()
execute_process(
    COMMAND "${KDE4_KDECONFIG_EXECUTABLE}" --path data
    OUTPUT_VARIABLE _data_dir
    ERROR_QUIET
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )
file(TO_CMAKE_PATH "${_data_dir}" _data_dir)
execute_process(
    COMMAND "${KDE4_KDECONFIG_EXECUTABLE}" --path services
    OUTPUT_VARIABLE _services_dir
    ERROR_QUIET
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )
file(TO_CMAKE_PATH "${_services_dir}" _services_dir)

if(INSTALL_TYPE STREQUAL "user")
    find_path(
        KDE4_DATA_DIR
        NAMES kfileplaces/bookmarks.xml kabc/std.vcf kconf_update/log/update.log
        HINTS ${_data_dir}
      )
    list(GET _services_dir 0 KDE4_SERVICES_DIR)
else()
    # TODO Check some other systems: is this file require to install some devel packages?
    find_path(KDE4_DATA_DIR cmake/modules/FindKDE4Internal.cmake HINTS ${_data_dir})
     find_path(KDE4_SERVICES_DIR katepart.desktop HINTS ${_services_dir})
endif()
set(CMAKE_INSTALL_PREFIX "${KDE4_DATA_DIR}/kate/pate")

#---------------------------------------------------------
# Section: Install package files
#---------------------------------------------------------
include(PythonInstall)

set(
    PLUGIN_SOURCES
    mtbkpsc.py
  )
python_install(FILES ${PLUGIN_SOURCES} DESTINATION ${CMAKE_INSTALL_PREFIX})

install(FILES katepate_mtbkpsc.desktop DESTINATION ${KDE4_SERVICES_DIR})

#---------------------------------------------------------
# Section: Configure package options
#---------------------------------------------------------

# CPack version numbers for release tarball name.
set(CPACK_PACKAGE_VERSION_MAJOR ${VERSION_MAJOR})
set(CPACK_PACKAGE_VERSION_MINOR ${VERSION_MINOR})
set(CPACK_PACKAGE_VERSION_PATCH ${VERSION_PATCH})

set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Kate/Pâté plugins (mostly for C++)")
set(CPACK_PACKAGE_VENDOR "Alex Turbov")
set(CPACK_PACKAGE_DESCRIPTION_FILE ${CMAKE_CURRENT_SOURCE_DIR}/README.md)
set(CPACK_GENERATOR TGZ)

set(
    CPACK_SOURCE_PACKAGE_FILE_NAME
    "kate-pate-plugins-${VERSION_STRING}"
    CACHE INTERNAL "tarball basename"
  )
set(CPACK_SOURCE_GENERATOR TGZ)
# The following components are regex's to match anywhere (unless anchored)
# in absolute path + filename to find files or directories to be excluded
# from source tarball.
set(CPACK_SOURCE_IGNORE_FILES
    "\\\\.gitignore$"
    "\\\\.kate-swp$"
    "\\\\.pyc$"
    "\\\\.tar\\\\.gz$"
    "\\\\.expandc$"
    "^.*/\\\\.git.*$"
  )
include(CPack)
