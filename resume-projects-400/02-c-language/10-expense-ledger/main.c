#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Expense Ledger */
typedef enum{FOOD,TRAVEL,LEARNING,CATEGORY_COUNT}Category;typedef struct{Category c;double amount;}Expense;
int main(void){Expense e[]={{FOOD,450},{TRAVEL,120},{FOOD,260},{LEARNING,900}};double total[CATEGORY_COUNT]={0};const char*n[]={"food","travel","learning"};
 for(size_t i=0;i<4;i++){total[e[i].c]+=e[i].amount;}for(int i=0;i<CATEGORY_COUNT;i++){printf("%s=%.2f\n",n[i],total[i]);}return 0;}
