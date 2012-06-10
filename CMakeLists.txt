#
# Copyright 2012 by Alex Trubov <i.zaufi@gmail.com>
#

cmake_minimum_required(VERSION 2.6)
cmake_policy(SET CMP0002 OLD)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})

project(kate-pate-plugins NONE)

find_package(PythonInterp REQUIRED)
include(PythonMacros)

if(INSTALL_TYPE STREQUAL "user")
    set(CMAKE_INSTALL_PREFIX "~/.kde4/share/apps/kate/pate")
else()
    set(CMAKE_INSTALL_PREFIX "/usr/share/apps/kate/pate")
endif()

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

# install(
#     FILES expand/text_x-c++hdr.expand expand/text_x-chdr.expand
#     DESTINATION ${CMAKE_INSTALL_PREFIX}/${EXPAND_DIR}
#   )
