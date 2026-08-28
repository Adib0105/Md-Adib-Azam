#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Sorting Benchmark */
int main(void){int a[]={9,4,1,8,3,7,2,6,5},comparisons=0,moves=0;size_t n=sizeof a/sizeof a[0];
 for(size_t i=1;i<n;i++){int key=a[i];size_t j=i;while(j>0&&(comparisons++,a[j-1]>key)){a[j]=a[j-1];j--;moves++;}a[j]=key;}
 for(size_t i=0;i<n;i++){printf("%d%c",a[i],i+1==n?'\n':' ');}printf("comparisons=%d moves=%d\n",comparisons,moves);return 0;}
