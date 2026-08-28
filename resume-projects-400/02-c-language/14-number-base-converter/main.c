#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Number Base Converter */
static void binary(unsigned n,char*out){int i=0;if(!n)out[i++]='0';while(n){out[i++]=(char)('0'+n%2);n/=2;}out[i]='\0';for(int a=0,b=i-1;a<b;a++,b--){char t=out[a];out[a]=out[b];out[b]=t;}}
int main(void){unsigned n=2026;char b[65];binary(n,b);printf("decimal=%u binary=%s octal=%o hex=%X\n",n,b,n,n);return 0;}
