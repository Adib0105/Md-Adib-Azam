#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Linked List Playlist */
typedef struct Node{const char*song;struct Node*next;}Node;int main(void){Node c={"Track C",NULL},b={"Track B",&c},a={"Track A",&b},*head=&a,*prev=NULL;
 while(head){Node*next=head->next;head->next=prev;prev=head;head=next;}for(Node*n=prev;n;n=n->next){printf("%s\n",n->song);}return 0;}
