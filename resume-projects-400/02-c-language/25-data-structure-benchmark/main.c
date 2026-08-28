#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Data Structure Benchmark */
int main(void){enum{N=1000};int stack[N],queue[N],top=0,head=0,tail=0,count=0;
 for(int i=0;i<N;i++){stack[top++]=i;queue[tail]=i;tail=(tail+1)%N;count++;}
 long stack_sum=0,queue_sum=0;while(top)stack_sum+=stack[--top];while(count){queue_sum+=queue[head];head=(head+1)%N;count--;}
 printf("operations=%d stack_sum=%ld queue_sum=%ld equal=%d\n",N*4,stack_sum,queue_sum,stack_sum==queue_sum);return stack_sum==queue_sum?0:1;}
