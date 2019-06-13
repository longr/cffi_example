#include <stdio.h>
#include <stdlib.h>
#include "fibonacci.h"

/* Get the nth fibonacci number */
int fibonacci(int num) {
  if (num == 0) {
    return 0;
  }
  else if (num == 1) {
    return 1;
  }
  else {
    return(fibonacci(num - 1) + fibonacci(num - 2));
  }
}

int fast_fibonacci(int num) {
  int a = 0;
  int b = 1;
  int number = 1;
  int c = 0;
  while (number != num) {
    c = b;
    b = b + a;
    a = c;
    number += 1;
  }
  
  return b;
}
