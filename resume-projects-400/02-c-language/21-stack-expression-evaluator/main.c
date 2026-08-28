#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Stack Expression Evaluator */
int main(void){const char*expr="12 3 4 * + 2 /";char copy[64];strcpy(copy,expr);double stack[32]={0};int top=0;char*tok=strtok(copy," ");
 while(tok){char*end;double v=strtod(tok,&end);if(*end=='\0')stack[top++]=v;else{if(top<2)return 2;double b=stack[--top],a=stack[--top];stack[top++]=*tok=='+'?a+b:*tok=='-'?a-b:*tok=='*'?a*b:a/b;}tok=strtok(NULL," ");}
 printf("expression=%s result=%.2f\n",expr,stack[0]);return top==1?0:3;}
