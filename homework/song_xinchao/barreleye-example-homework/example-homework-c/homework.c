/*********************************************************************
 * Created by Xinchao Song, contact@xinchaosong.com.                *
 * April 21, 2020                                                   *
 * Copyright © 2020 Xinchao Song. All rights reserved.              *
*********************************************************************/

#include "homework.h"

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include <stdio.h>
#include <stdlib.h>

int func_normal() {
    printf("A normal function.\n");

    return 0;
}

int func_error() {
    printf("A function with segmentation fault.\n");

    int *p = NULL;
    *p = 5;
    return 0;
}

int func_timeout() {
    printf("A function with a timeout issue.\n");

    sleep(3600);
    return 0;
}

int func_leak() {
    printf("A function with memory leak.\n");

    void *ptr = malloc(4);
    return 0;
}
