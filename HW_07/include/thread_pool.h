#pragma once

#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <stdbool.h>
#include "wsqueue.h"

#define container_of(ptr, type, member) (type*)((char*)(ptr) - offsetof(type, member))

typedef struct Task_t 
{
	volatile bool done;

	pthread_cond_t cond;
	pthread_mutex_t mutex;

	struct list_node node;
	size_t count;
	struct Task_t** tasks;

	void (*foo)(void *); 
	void* data; 
} Task;

typedef struct ThreadPool_t
{
	size_t count;
	pthread_t* threads;
	struct wsqueue tasks;
	volatile bool cont;
} ThreadPool;

typedef struct SData_t
{
	size_t n;
	int* arr;
	size_t dpth, max_dpth;

	Task task;
	ThreadPool* pool;
} SData;

void task_init(Task* task, void (*f) (void*), void* data);
void task_wait(Task* task);
void task_finit(Task* task);

void *worker(void* data);

void thpool_init(ThreadPool* pool, size_t threads_nm); 
void thpool_submit(ThreadPool* pool, Task* task);
void thpool_wait(Task* task); 
void thpool_finit(ThreadPool* pool);
