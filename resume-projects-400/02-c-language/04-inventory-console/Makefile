CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Werror -O2

all: app
app: main.c
	$(CC) $(CFLAGS) main.c -lm -o app
run: app
	./app
clean:
	$(RM) app
