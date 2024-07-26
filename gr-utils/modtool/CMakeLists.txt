# Copyright 2018,2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

GR_PYTHON_INSTALL(FILES
    __init__.py
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/modtool
)

set(GR_PKG_MODTOOL_DATA_DIR ${GR_PKG_DATA_DIR}/modtool/templates)


########################################################################
# Create and install the modtool conf file
########################################################################
file(TO_NATIVE_PATH ${CMAKE_INSTALL_PREFIX}/${GR_PKG_MODTOOL_DATA_DIR}/gr-newmod newmoddir)

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/modtool.conf.in
    ${CMAKE_CURRENT_BINARY_DIR}/modtool.conf
@ONLY)

install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/modtool.conf
    DESTINATION ${GR_PREFSDIR}
)

GR_PYTHON_INSTALL(
    PROGRAMS    gr_modtool
    DESTINATION ${GR_RUNTIME_DIR}
)

if(ENABLE_POSTINSTALL)
    if(ENABLE_COMPLETION_BASH)
        install(DIRECTORY DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/bash-completion)
        install(CODE
            "execute_process(\
                COMMAND env _GR_MODTOOL_COMPLETE=bash_source \
                    ${CMAKE_INSTALL_PREFIX}/${GR_RUNTIME_DIR}/gr_modtool \
                OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/bash-completion/gr_modtool \
                COMMAND_ERROR_IS_FATAL ANY\
            )")
        install(
            FILES ${CMAKE_CURRENT_BINARY_DIR}/bash-completion/gr_modtool
            DESTINATION ${GR_DATA_DIR}/bash-completion/completions/
        )
    endif(ENABLE_COMPLETION_BASH)

    if(ENABLE_COMPLETION_ZSH)
        install(DIRECTORY DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/zsh-completion)
        install(CODE
            "execute_process(\
                COMMAND env _GR_MODTOOL_COMPLETE=zsh_source \
                    ${CMAKE_INSTALL_PREFIX}/${GR_RUNTIME_DIR}/gr_modtool \
                OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/zsh-completion/_gr_modtool \
                COMMAND_ERROR_IS_FATAL ANY\
            )")
        install(
            FILES ${CMAKE_CURRENT_BINARY_DIR}/zsh-completion/_gr_modtool
            DESTINATION ${GR_DATA_DIR}/zsh/vendor-completions/
        )
    endif(ENABLE_COMPLETION_ZSH)

    if(ENABLE_COMPLETION_FISH)
        install(DIRECTORY DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/fish-completion)
        install(CODE
            "execute_process(\
                COMMAND env _GR_MODTOOL_COMPLETE=fish_source \
                    ${CMAKE_INSTALL_PREFIX}/${GR_RUNTIME_DIR}/gr_modtool \
                OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/fish-completion/gr_modtool.fish \
                COMMAND_ERROR_IS_FATAL ANY\
            )")
        install(
            FILES ${CMAKE_CURRENT_BINARY_DIR}/fish-completion/gr_modtool.fish
            DESTINATION ${GR_DATA_DIR}/fish/vendor-completions.d/
        )
    endif(ENABLE_COMPLETION_FISH)
endif(ENABLE_POSTINSTALL)

########################################################################
# Add subdirectories
########################################################################
add_subdirectory(core)
add_subdirectory(cli)
add_subdirectory(tools)
add_subdirectory(templates)
add_subdirectory(tests)
