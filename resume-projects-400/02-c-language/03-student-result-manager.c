/* Student Result Manager - safe, standalone C portfolio project. */
#include <stdio.h>
#include <string.h>
typedef struct { int id; char name[40]; double value; } Record;
int main(void) {
    Record records[] = {{3, "Alpha", 103.0}, {4, "Beta", 153.0}};
    double total = 0; size_t count = sizeof(records) / sizeof(records[0]);
    printf("Student Result Manager\n%-5s %-20s %10s\n", "ID", "NAME", "VALUE");
    for (size_t n = 0; n < count; n++) { total += records[n].value; printf("%-5d %-20s %10.2f\n", records[n].id, records[n].name, records[n].value); }
    printf("Total: %.2f | Average: %.2f\n", total, count ? total / count : 0);
    return 0;
}
