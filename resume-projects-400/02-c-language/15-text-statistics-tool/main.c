#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Text Statistics Tool */
int main(void){const char*t="C makes systems fast.\nProject 15 has tests!";int lines=1,words=0,letters=0,digits=0,punct=0,inword=0;
 for(size_t i=0;t[i];i++){unsigned char c=(unsigned char)t[i];if(c=='\n')lines++;if(isalpha(c))letters++;if(isdigit(c))digits++;if(ispunct(c))punct++;if(isspace(c))inword=0;else if(!inword){words++;inword=1;}}
 printf("lines=%d words=%d letters=%d digits=%d punctuation=%d\n",lines,words,letters,digits,punct);return 0;}
