#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Bus Reservation System */
int main(void){int seats[10]={0},requests[]={3,5,3,11,1},ok=0,bad=0;
 for(size_t i=0;i<5;i++){int s=requests[i];if(s<1||s>10||seats[s-1])bad++;else{seats[s-1]=1;ok++;}}
 printf("reserved=%d rejected=%d available=%d\n",ok,bad,10-ok);return 0;}
