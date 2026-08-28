#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Contact Directory */
typedef struct{char name[24],phone[16];}Contact;
int main(void){Contact c[]={{"Riya","9999"},{"adib","9433"},{"Kabir","8888"}};
 for(size_t i=0;i<3;i++)for(size_t j=i+1;j<3;j++)if(strcasecmp(c[i].name,c[j].name)>0){Contact t=c[i];c[i]=c[j];c[j]=t;}
 for(size_t i=0;i<3;i++){printf("%s %s\n",c[i].name,c[i].phone);}return 0;}
