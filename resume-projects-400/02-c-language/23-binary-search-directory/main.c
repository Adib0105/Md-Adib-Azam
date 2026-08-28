#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Binary Search Directory */
typedef struct{int id;const char*name;}Record;int main(void){Record r[]={{40,"Riya"},{10,"Adib"},{30,"Kabir"},{20,"Asha"}};
 for(int i=0;i<4;i++){for(int j=i+1;j<4;j++){if(r[j].id<r[i].id){Record t=r[i];r[i]=r[j];r[j]=t;}}}int key=30,lo=0,hi=3,found=-1;
 while(lo<=hi){int mid=(lo+hi)/2;if(r[mid].id==key){found=mid;break;}if(r[mid].id<key)lo=mid+1;else hi=mid-1;}if(found<0)return 1;printf("found id=%d name=%s\n",r[found].id,r[found].name);return 0;}
