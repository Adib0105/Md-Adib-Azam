#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Caesar Cipher Demo */
static void shift(char*s,int k){for(size_t i=0;s[i];i++){char c=s[i];if(isalpha((unsigned char)c)){char base=isupper((unsigned char)c)?'A':'a';s[i]=(char)(base+(c-base+k+26)%26);}}}
int main(void){char text[64]="Portfolio Project 8";shift(text,5);printf("encoded=%s\n",text);shift(text,-5);printf("decoded=%s\n",text);return strcmp(text,"Portfolio Project 8");}
