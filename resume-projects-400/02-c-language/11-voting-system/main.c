#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Voting System */
int main(void){char votes[]={'A','B','A','C','X','B','A'};int count[3]={0},invalid=0;
 for(size_t i=0;i<sizeof votes;i++){if(votes[i]>='A'&&votes[i]<='C')count[votes[i]-'A']++;else invalid++;}
 int winner=0;for(int i=1;i<3;i++){if(count[i]>count[winner])winner=i;}printf("A=%d B=%d C=%d invalid=%d winner=%c\n",count[0],count[1],count[2],invalid,'A'+winner);return 0;}
