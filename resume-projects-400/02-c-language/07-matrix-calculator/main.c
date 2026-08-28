#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Matrix Calculator */
int main(void){int a[2][3]={{1,2,3},{4,5,6}},b[3][2]={{7,8},{9,10},{11,12}},c[2][2]={{0}};
 for(int i=0;i<2;i++)for(int j=0;j<2;j++)for(int k=0;k<3;k++)c[i][j]+=a[i][k]*b[k][j];
 for(int i=0;i<2;i++){printf("%d %d\n",c[i][0],c[i][1]);}return c[0][0]==58&&c[1][1]==154?0:1;}
