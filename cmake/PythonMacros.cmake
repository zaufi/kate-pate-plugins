# Python macros
# ~~~~~~~~~~~~~
# Copyright (c) 2007, Simon Edwards <simon@simonzone.com>
# Copyright (c) 2012, Alex Turbov <i.zaufi@gmail.com>
#
# Redistribution and use is allowed according to the terms of the BSD license.
# For details see the accompanying COPYING-CMAKE-SCRIPTS file.
#
# This file defines the following macros:
#
# python_install(DESINATION_DIR SOURCE_FILE0[ SOURCE_FILE1[ ... [SOURCE_FILEn]]])
#     Install source files, which is a Python .py files, into the
#     destination directory during install. The file will be byte compiled
#     and both the .py file and .pyc file will be installed.
#
# Changelog:
#   Mon Jun 11 02:49:02 MSK 2012, by Alex Turbov
#       Refactoring to support variadic number of source files
#       Prevent excecution w/ incorrect arguments count
#       Support for symlinked source files has been added
#       Generalise work w/ file extensions
#

get_filename_component(PYTHON_MACROS_MODULE_PATH ${CMAKE_CURRENT_LIST_FILE} PATH)

macro(python_install DESINATION_DIR)
    set(SOURCE_FILES ${ARGN})

    # Make sure that we have smth to do...
    if(${ARGC} LESS 2)
        message(FATAL_ERROR "At least one source file required for python_install()")
        return()
    endif()

    add_custom_target(compile_python_files ALL)

    # Install the source files.
    install(FILES ${SOURCE_FILES} DESTINATION ${DESINATION_DIR})

    foreach(_py_file ${SOURCE_FILES})
        # Byte compile and install the .pyc file.
        get_filename_component(_absfilename ${_py_file} ABSOLUTE)
        get_filename_component(_filename ${_py_file} NAME)
        get_filename_component(_filenamebase ${_py_file} NAME_WE)
        get_filename_component(_basepath ${_py_file} PATH)
        get_filename_component(_ext ${_py_file} EXT)
        set(_bin_py ${CMAKE_CURRENT_BINARY_DIR}/${_basepath}/${_filename})
        set(_bin_pyc ${CMAKE_CURRENT_BINARY_DIR}/${_basepath}/${_filenamebase}${_ext}c)

        file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/${_basepath})

        get_filename_component(_abs_bin_py ${_bin_py} ABSOLUTE)
        # Don't copy the file onto itself.
        if(_abs_bin_py STREQUAL ${_absfilename})
            add_custom_command(
                TARGET compile_python_files
                COMMAND ${PYTHON_EXECUTABLE} ${PYTHON_MACROS_MODULE_PATH}/PythonCompile.py ${_bin_py}
                DEPENDS ${_absfilename}
                COMMENT "Byte-compiling ${_py_file}"
            )
        else()
            if(IS_SYMLINK ${_absfilename})
                set(_copy_cmd ${CMAKE_COMMAND} -E copy ${_absfilename} ${_bin_py})
            else()
                set(_copy_cmd ${CMAKE_COMMAND} -E create_symlink ${_absfilename} ${_bin_py})
            endif()
            add_custom_command(
                TARGET compile_python_files
                COMMAND ${_copy_cmd}
                COMMAND ${PYTHON_EXECUTABLE} ${PYTHON_MACROS_MODULE_PATH}/PythonCompile.py ${_bin_py}
                DEPENDS ${_absfilename}
                COMMENT "Byte-compiling ${_py_file}"
            )
        endif()
        install(FILES ${_bin_pyc} DESTINATION ${DESINATION_DIR})
    endforeach()

endmacro(python_install)

# kate: hl cmake;
