#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Library Catalog */
typedef struct{int id;const char*title;int available;}Book;
int main(void){Book b[]={{1,"C Programming",1},{2,"Database Systems",0},{3,"Computer Networks",1}};const char *q="database";int found=0;
 for(size_t i=0;i<3;i++){char lower[64];size_t j=0;for(;b[i].title[j]&&j<63;j++)lower[j]=(char)tolower((unsigned char)b[i].title[j]);lower[j]='\0';
 if(strstr(lower,q)){printf("%d %s available=%d\n",b[i].id,b[i].title,b[i].available);found=1;}}return found?0:1;}
