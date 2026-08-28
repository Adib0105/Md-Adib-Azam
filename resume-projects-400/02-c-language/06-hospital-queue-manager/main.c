#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Hospital Queue Manager */
typedef struct{const char*name;int priority,arrival;}Patient;
int main(void){Patient q[]={{"Asha",3,1},{"Kabir",1,2},{"Riya",2,3}};
 for(size_t i=0;i<3;i++)for(size_t j=i+1;j<3;j++)if(q[j].priority<q[i].priority||(q[j].priority==q[i].priority&&q[j].arrival<q[i].arrival)){Patient t=q[i];q[i]=q[j];q[j]=t;}
 for(size_t i=0;i<3;i++){printf("%zu %s priority=%d\n",i+1,q[i].name,q[i].priority);}return 0;}
