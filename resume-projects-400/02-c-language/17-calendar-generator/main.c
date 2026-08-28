#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Calendar Generator */
static int leap(int y){return y%400==0||(y%4==0&&y%100!=0);}static int weekday(int y,int m,int d){if(m<3){m+=12;y--;}int k=y%100,j=y/100;return (d+13*(m+1)/5+k+k/4+j/4+5*j)%7;}
int main(void){int y=2028,m=2,days=leap(y)?29:28,start=(weekday(y,m,1)+6)%7;printf("Mon Tue Wed Thu Fri Sat Sun\n");for(int i=0;i<start;i++){printf("    ");}for(int d=1;d<=days;d++){printf("%3d ",d);if((start+d)%7==0)puts("");}puts("");return 0;}
