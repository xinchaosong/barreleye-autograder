cmake_minimum_required(VERSION 3.16)
project(example)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(cpp_main
        main.cpp
        homework.hpp
        homework.cpp)

add_executable(cpp_grade
        grading_tests.cpp
        homework.hpp
        homework.cpp)
