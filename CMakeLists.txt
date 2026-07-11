cmake_minimum_required(VERSION 3.10.0)
project(long-text-simplifier VERSION 0.1.0 LANGUAGES C CXX)

set(PYBIND11_FINDPYTHON ON)
set(Python_EXECUTABLE "${CMAKE_CURRENT_SOURCE_DIR}/.venv/bin/python" CACHE PATH "Python" FORCE)
set(pybind11_DIR "${CMAKE_CURRENT_SOURCE_DIR}/.venv/lib/python3.12/site-packages/pybind11/share/cmake/pybind11")

find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

add_executable(long-text-simplifier main.cpp)
target_link_libraries(long-text-simplifier PRIVATE pybind11::headers Python::Python)