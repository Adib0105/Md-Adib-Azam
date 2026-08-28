#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Sparse Matrix Toolkit */
typedef struct{int row,col,value;}Entry;int main(void){int m[3][4]={{0,5,0,0},{2,0,0,7},{0,0,3,0}};Entry e[12];int n=0;
 for(int r=0;r<3;r++)for(int c=0;c<4;c++)if(m[r][c])e[n++]=(Entry){r,c,m[r][c]};
 printf("nonzero=%d\n",n);for(int i=0;i<n;i++){printf("original=(%d,%d,%d) transpose=(%d,%d,%d)\n",e[i].row,e[i].col,e[i].value,e[i].col,e[i].row,e[i].value);}return 0;}
