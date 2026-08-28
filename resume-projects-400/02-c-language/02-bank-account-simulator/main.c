#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Bank Account Simulator */
int main(void) {
    double balance=5000, tx[]={1200,-850,-6000,300}; size_t accepted=0,rejected=0;
    for(size_t i=0;i<sizeof tx/sizeof tx[0];i++){ if(tx[i]<0 && balance+tx[i]<0){rejected++;continue;} balance+=tx[i];accepted++; }
    printf("balance=%.2f accepted=%zu rejected=%zu\n",balance,accepted,rejected); return 0;
}
