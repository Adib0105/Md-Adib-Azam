#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_EMPLOYEES 200
#define TEXT_SIZE 80

typedef struct {
    int id;
    char name[TEXT_SIZE];
    char department[TEXT_SIZE];
    double score;
} Employee;

static void trim_newline(char *text) {
    text[strcspn(text, "\r\n")] = '\0';
}

static int load_employees(const char *filename, Employee employees[]) {
    FILE *file = fopen(filename, "r");
    char line[300];
    int count = 0;
    if (file == NULL) {
        fprintf(stderr, "Could not open %s\n", filename);
        return -1;
    }
    if (fgets(line, sizeof(line), file) == NULL) {
        fclose(file);
        return 0;
    }
    while (count < MAX_EMPLOYEES && fgets(line, sizeof(line), file) != NULL) {
        char *id = strtok(line, ",");
        char *name = strtok(NULL, ",");
        char *department = strtok(NULL, ",");
        char *score = strtok(NULL, ",");
        if (id == NULL || name == NULL || department == NULL || score == NULL) {
            continue;
        }
        trim_newline(score);
        employees[count].id = atoi(id);
        snprintf(employees[count].name, TEXT_SIZE, "%s", name);
        snprintf(employees[count].department, TEXT_SIZE, "%s", department);
        employees[count].score = atof(score);
        count++;
    }
    fclose(file);
    return count;
}

static void report(Employee employees[], int count, const char *department) {
    int selected = 0;
    double total = 0.0;
    Employee *top = NULL;
    for (int index = 0; index < count; index++) {
        Employee *employee = &employees[index];
        if (department != NULL && strcmp(employee->department, department) != 0) {
            continue;
        }
        selected++;
        total += employee->score;
        if (top == NULL || employee->score > top->score) {
            top = employee;
        }
    }
    printf("Employee report\n");
    printf("Records: %d\n", selected);
    if (selected == 0) {
        printf("No matching employees.\n");
        return;
    }
    printf("Average score: %.2f\n", total / selected);
    printf("Top performer: %s (%.1f)\n", top->name, top->score);
}

int main(int argc, char *argv[]) {
    Employee employees[MAX_EMPLOYEES];
    int count;
    if (argc < 2) {
        fprintf(stderr, "Usage: %s employees.csv [department]\n", argv[0]);
        return 1;
    }
    count = load_employees(argv[1], employees);
    if (count < 0) {
        return 1;
    }
    report(employees, count, argc >= 3 ? argv[2] : NULL);
    return 0;
}
