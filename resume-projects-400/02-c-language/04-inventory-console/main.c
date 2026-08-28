#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Inventory Console */
typedef struct {const char *sku; int qty,reorder,target; double cost;} Item;
int main(void){Item x[]={{"A1",4,5,20,80},{"B2",15,8,25,120},{"C3",2,4,12,45}};double value=0;
 for(size_t i=0;i<3;i++){value+=x[i].qty*x[i].cost;if(x[i].qty<=x[i].reorder)printf("reorder %s qty=%d\n",x[i].sku,x[i].target-x[i].qty);}
 printf("stock_value=%.2f\n",value);return 0;}
