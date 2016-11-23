#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include "thread_pool.h"

int* array_init(size_t n)
{
    int* arr = malloc(sizeof(int) * n);
    for (size_t i = 0; i < n; i++) arr[i] = rand();
    return arr;
}

bool is_sort(const int* arr, size_t n)
{
    for (size_t i = 1; i < n; i++)
        if (arr[i] < arr[i - 1]) return false;
    return true;
}

int intcmp(const void* a, const void* b)
{
    return (*((int*)a) - *((int*)b));
}

void swap(int* a, int *b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

void sort_f(void* param);

void add_tasks(ThreadPool* pool, Task* task, SData* data_l, SData* data_r)
{
    task_init(&data_l->task, sort_f, data_l);
    task_init(&data_r->task, sort_f, data_r);

    task->tasks = malloc(2 * sizeof(Task*));
    task->tasks[0] = &data_l->task;
    task->tasks[1] = &data_r->task;
    task->count = 2;

    thpool_submit(pool, &data_l->task);
    thpool_submit(pool, &data_r->task);
}

void sort_f(void* param)
{
    SData* data = (SData*) param;
    size_t n = data->n;
    int* arr = data->arr;
    size_t dpth = data->dpth;
    size_t max_dpth = data->max_dpth;
    Task* task = &data->task;
    ThreadPool* pool = data->pool;

    if (dpth == max_dpth)
    {
        qsort(arr, n, sizeof(int), intcmp);
        return;
    }

    if (n <= 1) return;

    int x = arr[0];
    int *l = arr;
    int *r = arr + n - 1;
    while (l < r)
    {
        while (*l < x && l < r) l++;
        while (*r >= x && r > l) r--;
        if (l < r) swap(l, r);
    }

    SData* data_l = malloc(sizeof(SData));
    SData* data_r = malloc(sizeof(SData));

    data_l->arr = arr;
    data_l->n = l - arr;
    data_l->dpth = dpth + 1;
    data_l->max_dpth = max_dpth;
    data_l->pool = pool;

    data_r->arr = l;
    data_r->n = n - (l - arr);
    data_r->dpth = dpth + 1;
    data_r->max_dpth = max_dpth;
    data_r->pool = pool;

    add_tasks(pool, task, data_l, data_r);
}

int main(int argc, char* argv[]) 
{
    srand(42);

    assert(argc == 4);
    size_t thrd_cnt = atoi(argv[1]);
    size_t arr_size = atoi(argv[2]);
    size_t rec_dpth = atoi(argv[3]);

    ThreadPool pool;
    int* arr = array_init(arr_size);

    SData* data = malloc(sizeof(SData));
    data->n = arr_size;
    data->arr = arr;
    data->dpth = 0;
    data->max_dpth = rec_dpth;
    data->pool = &pool;

    task_init(&data->task, sort_f, data);
    thpool_init(&pool, thrd_cnt);
    thpool_submit(&pool, &data->task);
    thpool_wait(&data->task);
    thpool_finit(&pool);

    if (is_sort(arr, arr_size)) printf("ok\n");
    else                        printf("failed\n");
    free(arr);

    return 0;
}
