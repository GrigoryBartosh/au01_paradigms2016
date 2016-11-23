
CC       ?= gcc
CFLAGS   ?= -Wall -Wextra -Werror -std=c99 -g
LDFLAGS  ?= -lpthread
SRCS     ?= main.c thread_pool.c linkedlist.c queue.c squeue.c wsqueue.c
INCLUDES ?= -I include
OBJS     ?= $(SRCS:.c=.o)
NAME     ?= pqsort

all: create main

main: $(addprefix bin/, $(OBJS))
	$(CC) $(addprefix bin/, $(OBJS)) $(LDFLAGS) -o $(NAME)

create:
	mkdir -p bin

run:
	./$(NAME) 4 100000000 3
	./$(NAME) 1 100000000 3

bin/main.o: src/main.c include/*.h
	$(CC) -c src/main.c $(CFLAGS) -o bin/main.o $(INCLUDES)

bin/thread_pool.o: src/thread_pool.c include/*.h
	$(CC) -c src/thread_pool.c $(CFLAGS) -o bin/thread_pool.o $(INCLUDES)

bin/linkedlist.o: src/linkedlist.c include/*.h
	$(CC) -c src/linkedlist.c $(CFLAGS) -o bin/linkedlist.o $(INCLUDES)

bin/queue.o: src/queue.c include/*.h
	$(CC) -c src/queue.c $(CFLAGS) -o bin/queue.o $(INCLUDES)

bin/squeue.o: src/squeue.c include/*.h
	$(CC) -c src/squeue.c $(CFLAGS) -o bin/squeue.o $(INCLUDES)

bin/wsqueue.o: src/wsqueue.c include/*.h
	$(CC) -c src/wsqueue.c $(CFLAGS) -o bin/wsqueue.o $(INCLUDES)

clean:
	rm -rf bin
	rm -rf $(NAME)
