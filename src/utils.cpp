#include "utils.hpp"
#include <iostream>

int dummy_task(int a) {
    std::cout << "Dummy Task, print args" << a << std::endl;
    return 0;
}

int add(int a, int b) {
    return a + b;
}
