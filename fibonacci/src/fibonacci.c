#include <stdio.h>
#include <stdlib.h>
#include "fibonacci.h"

 /* Get the nth fibonacci number */
unsigned long long int fibonacci(int num) {
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

unsigned long long int fast_fibonacci(int num) {
  unsigned long long int a = 0;
  unsigned long long int b = 1;
  int number = 1;
  unsigned long long int c = 0;
  if (num < 2) {
    return num;
  }
  while (number != num) {
    c = b;
    b = b + a;
    a = c;
    number += 1;
  }
  
  return b;
}
