/*********************************************************************
 * Created by Xinchao Song, contact@xinchaosong.com.                *
 * April 21, 2020                                                   *
 * Copyright © 2020 Xinchao Song. All rights reserved.              *
*********************************************************************/

#include "homework.hpp"

int main() {
    Homework hw;

    hw.func_normal();

    hw.func_error();

    hw.func_timeout();

    hw.func_leak();

    return 0;
}
