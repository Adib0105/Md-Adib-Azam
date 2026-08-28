#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Payroll Calculator */
static double tax(double gross){return gross<=25000?0:(gross<=50000?(gross-25000)*.10:2500+(gross-50000)*.20);}
int main(void){double basic=42000,allowance=8000,overtime_hours=10,rate=250,gross=basic+allowance+overtime_hours*rate,t=tax(gross);
 printf("gross=%.2f tax=%.2f net=%.2f\n",gross,t,gross-t);return gross-t>0?0:1;}
