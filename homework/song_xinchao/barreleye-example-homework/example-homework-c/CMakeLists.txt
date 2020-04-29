cmake_minimum_required(VERSION 3.16)
project(example)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(c_main
        main.c
        homework.h
        homework.c)

add_executable(c_grade
        grading_tests.c
        homework.h
        homework.c)
