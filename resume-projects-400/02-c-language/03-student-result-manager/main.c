#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Student Result Manager */
typedef struct { const char *name; double theory,lab; } Student;
int main(void){ Student s[]={{"Asha",84,92},{"Kabir",72,78},{"Riya",91,95}};
 for(size_t i=0;i<3;i++){double score=.6*s[i].theory+.4*s[i].lab; char grade=score>=90?'A':score>=80?'B':score>=70?'C':score>=60?'D':'F'; printf("%s %.1f %c\n",s[i].name,score,grade);} return 0;}
