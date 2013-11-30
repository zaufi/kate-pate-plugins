# Python3 modules install helper
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Copyright (c) 2013, Alex Turbov <i.zaufi@gmail.com>
#
# Redistribution and use is allowed according to the terms of the BSD license.
# For details see the accompanying COPYING-CMAKE-SCRIPTS file.
#
# This file defines the following function:
#
# python_install(FILES <python-sources> DESTINATION <dst> COMPONENT <name>)
#     Install source files, which is a Python .py files, into the
#     destination directory during install. The file will be byte compiled
#     and both the .py file and .pyc file will be installed.
#

include(CMakeParseArguments)

set(PYTHON_INSTALL_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")

function(python_install)
    if(NOT PYTHON_EXECUTABLE)
        message(FATAL_ERROR "You have to find python executable before call this function")
        return()
    endif()
    if(PYTHON_VERSION_MAJOR VERSION_LESS 3)
        message(FATAL_ERROR "python_install() require Python version >= 3")
        return()
    endif()

    # Parse function arguments
    set(options "")
    set(one_value_args COMPONENT DESTINATION)
    set(multi_value_args FILES)
    cmake_parse_arguments(python_install "${options}" "${one_value_args}" "${multi_value_args}" ${ARGN})

    # Check mandatory arguments
    if(NOT python_install_FILES)
        message(FATAL_ERROR "python_install given no FILES")
        return()
    endif()
    if(NOT python_install_DESTINATION)
        message(FATAL_ERROR "python_install given no DESTINATION")
        return()
    endif()

    add_custom_target(compile_python_files ALL)

    # Install the source files.
    if(python_install_COMPONENT)
        install(
            FILES ${python_install_FILES}
            DESTINATION ${python_install_DESTINATION}
            COMPONENT "${python_install_COMPONENT}"
          )
    else()
        install(
            FILES ${python_install_FILES}
            DESTINATION "${python_install_DESTINATION}"
          )
    endif()

    foreach(_py_file ${python_install_FILES})
        set(_py_src "${python_install_DESTINATION}/${_py_file}")
        set(_py_install_script "${CMAKE_CURRENT_BINARY_DIR}/${_py_file}.install.cmake")
        configure_file(
            ${PYTHON_INSTALL_MODULE_PATH}/PythonSourceInstallTemplate.cmake.in
            ${_py_install_script}
            @ONLY
          )
        install(SCRIPT ${_py_install_script})
    endforeach()

endfunction(python_install)

# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
# X-Chewy-Path: PythonInstall.cmake
# X-Chewy-Version: 2.1
# X-Chewy-Description: Helper to install Python 3.x scripts
# X-Chewy-AddonFile: PythonSourceInstallTemplate.cmake.in
