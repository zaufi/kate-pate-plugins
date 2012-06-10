#
# Copyright 2012 by Alex Trubov <i.zaufi@gmail.com>
#
# TODO Detect that Kate and Pâté are installed!
#

#---------------------------------------------------------
# Section: Init cmake
#---------------------------------------------------------
cmake_minimum_required(VERSION 2.6)
cmake_policy(SET CMP0002 OLD)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})

project(kate-pate-plugins NONE)

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

if(INSTALL_TYPE STREQUAL "user")
    find_path(
        KDE4_DATA_DIR
        NAMES kfileplaces/bookmarks.xml kabc/std.vcf kconf_update/log/update.log
        HINTS ${_data_dir}
      )
else()
    find_path(KDE4_DATA_DIR cmake/modules/FindKDE4Internal.cmake HINTS ${_data_dir})
endif()
set(CMAKE_INSTALL_PREFIX "${KDE4_DATA_DIR}/kate/pate")


#---------------------------------------------------------
# Section: Install package files
#---------------------------------------------------------
include(PythonMacros)

set(LIBKATEPATE_DIR libkatepate)
set(LIBKATEPATE_SOURCES ${LIBKATEPATE_DIR}/__init__.py ${LIBKATEPATE_DIR}/ui.py)
python_install(${CMAKE_INSTALL_PREFIX}/${LIBKATEPATE_DIR} ${LIBKATEPATE_SOURCES})

set(PLUGIN_SOURCES format.py block.py commentar.py expand/expand.py)
python_install(${CMAKE_INSTALL_PREFIX} ${PLUGIN_SOURCES})

set(EXPAND_DIR expand)
set(
    EXPAND_SOURCES
    expand/text_x-c++src.expand
    expand/text_x-c++hdr.expand
    expand/text_x-chdr.expand
  )
python_install(${CMAKE_INSTALL_PREFIX}/${EXPAND_DIR} ${EXPAND_SOURCES})
