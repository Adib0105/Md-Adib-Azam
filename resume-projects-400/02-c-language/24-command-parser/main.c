#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Command Parser */
int main(void){char input[]="deploy --env \"staging west\" --dry-run",tokens[8][32];int count=0,inquote=0,pos=0;
 for(size_t i=0;;i++){char c=input[i];if(c=='"'){inquote=!inquote;continue;}if((c==' '&&!inquote)||c=='\0'){if(pos){tokens[count][pos]='\0';count++;pos=0;}if(c=='\0'||count==8)break;}else if(pos<31)tokens[count][pos++]=c;}
 printf("argc=%d\n",count);for(int i=0;i<count;i++){printf("argv[%d]=%s\n",i,tokens[i]);}return inquote?1:0;}
