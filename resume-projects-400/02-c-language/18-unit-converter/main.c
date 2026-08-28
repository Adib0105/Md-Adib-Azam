#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Unit Converter */
static double c_to_f(double x){return x*9/5+32;}static double km_to_mi(double x){return x*.621371;}static double kg_to_lb(double x){return x*2.20462;}
int main(void){printf("30C=%.1fF\n",c_to_f(30));printf("10km=%.3fmi\n",km_to_mi(10));printf("5kg=%.3flb\n",kg_to_lb(5));return 0;}
