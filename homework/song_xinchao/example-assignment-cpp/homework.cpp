/*********************************************************************
 * Created by Xinchao Song, contact@xinchaosong.com.                *
 * April 21, 2020                                                   *
 * Copyright © 2020 Xinchao Song. All rights reserved.              *
*********************************************************************/

#include "homework.hpp"

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include <iostream>
#include <cstdlib>

int Homework::func_normal() {
    std::cout << "A normal method." << std::endl;

    return 0;
}

int Homework::func_error() {
    std::cout << "A method with segmentation fault." << std::endl;

    int *p = 0;
    *p = 5;
    return 0;
}

int Homework::func_timeout() {
    std::cout << "A method with a timeout issue." << std::endl;

    sleep(3600);
    return 0;
}

int Homework::func_leak() {
    std::cout << "A method with memory leak." << std::endl;

    void *ptr = malloc(4);
    return 0;
}
