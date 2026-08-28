#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Quiz Game */
int main(void){const char key[]={'B','A','C','D','B'},answers[]={'B','C','C','D','B'};int score=0;
 for(size_t i=0;i<5;i++){int correct=answers[i]==key[i];score+=correct;printf("q%zu %s\n",i+1,correct?"correct":"incorrect");}
 printf("score=%d/5 percentage=%.1f\n",score,score*20.0);return 0;}
