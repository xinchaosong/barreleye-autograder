/*********************************************************************
 * Created by Xinchao Song, contact@xinchaosong.com.                *
 * April 21, 2020                                                   *
 * Copyright © 2020 Xinchao Song. All rights reserved.              *
*********************************************************************/

#include "homework.hpp"
#include <iostream>

#define TEST_RESULT _test_result
#define TEST_INIT int TEST_RESULT = 1
#define TEST_ASSERT(expression) TEST_RESULT = (TEST_RESULT) && (expression)

// Test Case #1
int test_func_normal() {
    TEST_INIT;

    Homework hw;
    TEST_ASSERT(0 == hw.func_normal());

    return TEST_RESULT;
}

// Test Case #2
int test_func_error() {
    TEST_INIT;

    Homework hw;
    TEST_ASSERT(0 == hw.func_error());

    return TEST_RESULT;
}

// Test Case #3
int test_func_timeout() {
    TEST_INIT;

    Homework hw;
    TEST_ASSERT(0 == hw.func_timeout());

    return TEST_RESULT;
}

// Test Case #4
int test_func_leak() {
    TEST_INIT;

    Homework hw;
    TEST_ASSERT(0 == hw.func_leak());

    return TEST_RESULT;
}

double unit_test(int (*fun_ptr)(), double pts) {
    return fun_ptr() * pts;
}

double unit_test_ptf(int (*fun_ptr)(), double pts, const char *title) {
    double score = fun_ptr() * pts;

    printf("Test case %s: ", title);
    printf("%.2f / %.2f", score, pts);

    if (score == 0) {
        printf("  ##FAIL##");
    }

    printf("\n");

    return score;
}

int main(int argc, const char *argv[]) {
    double score = 0;
    int test_id = 0;

    if (argc == 2) {
        try {
            test_id = std::stoi(argv[1]);
        } catch (std::exception &e) {
            std::cerr << "The argument received is not a integer." << std::endl;
            exit(1);
        }
    }
    if (argc > 2) {
        std::cerr << "Too many arguments." << std::endl;
        exit(1);
    }

    switch (test_id) {
        case 0:
            printf("Example Assignment C++\n");
            printf("Auto grading...\n\n");

            score += unit_test_ptf(&test_func_normal,
                                   25.0,
                                   "#1 test_func_normal");
            score += unit_test_ptf(&test_func_error,
                                   25.0,
                                   "#2 test_func_error");
            score += unit_test_ptf(&test_func_timeout,
                                   25.0,
                                   "#3 test_func_timeout");
            score += unit_test_ptf(&test_func_leak,
                                   25.0,
                                   "#4 test_func_leak");

            printf("\nTotal grade: %.2f\n", score);
            break;

        case 1:
            score = unit_test(&test_func_normal, 25.0);
            break;

        case 2:
            score = unit_test(&test_func_error, 25.0);
            break;

        case 3:
            score = unit_test(&test_func_timeout, 25.0);
            break;

        case 4:
            score = unit_test(&test_func_leak, 25.0);
            break;

        default:
            std::cerr << "Invalid test id." << std::endl;
            exit(1);
    }

    if (test_id != 0) {
        printf("Score: %.2f\n", score);
    }

    return 0;
}
