# Version chosen arbitrarily
CMAKE_MINIMUM_REQUIRED(VERSION 3.0)

# maybe widgets too
FIND_PACKAGE(Qt5LinguistTools)
INCLUDE(PyQt5TranslationMacros.cmake)
PYQT5_CREATE_TRANSLATION(form43checker_translations_qm ${CMAKE_SOURCE_DIR}/src ${CMAKE_SOURCE_DIR}/src/Form43Checker_en.ts)

add_custom_target(translations ALL DEPENDS ${form43checker_translations_qm})

###############
## Installation

INSTALL(FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/Form43Checker.py
        DESTINATION bin/plugins)