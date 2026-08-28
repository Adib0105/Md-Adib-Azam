#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

/* Employee Record System */
typedef struct { int id; const char *name; double salary; } Employee;
int main(void) {
    Employee a[]={{101,"Asha",32000},{102,"Kabir",28500},{103,"Riya",41000}};
    size_t n=sizeof a/sizeof a[0], best=0; double total=0;
    for(size_t i=0;i<n;i++){ total+=a[i].salary; if(a[i].salary>a[best].salary) best=i; }
    printf("employees=%zu payroll=%.2f highest=%s:%.2f\n",n,total,a[best].name,a[best].salary); return 0;
}
