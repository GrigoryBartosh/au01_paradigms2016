#include "thread_pool.h"

void task_init(Task* task, void (*foo) (void*), void* data)
{
    task->foo = foo;
    task->data = data;
    task->done = false;
    pthread_cond_init(&task->cond, NULL);
    pthread_mutex_init(&task->mutex, NULL);
    task->count = 0;
    task->tasks = NULL;
}

void task_wait(Task* task)
{
    pthread_mutex_lock(&task->mutex);
    while (!task->done)
        pthread_cond_wait(&task->cond, &task->mutex);
    pthread_mutex_unlock(&task->mutex);
}

void task_finit(Task* task)
{
    pthread_cond_destroy(&task->cond);
    pthread_mutex_destroy(&task->mutex);
    if (task->count) free(task->tasks);
}

void *worker(void* data)
{
    ThreadPool* pool = (ThreadPool*)data;

    while (pool->cont || queue_size(&pool->tasks.squeue.queue))
    {
        struct list_node *node;

        pthread_mutex_lock(&pool->tasks.squeue.mutex);
        while (pool->cont && !queue_size(&pool->tasks.squeue.queue))
            pthread_cond_wait(&pool->tasks.cond, &pool->tasks.squeue.mutex);

        node = queue_pop(&pool->tasks.squeue.queue);
        pthread_mutex_unlock(&pool->tasks.squeue.mutex);

        if (node)
        {
            Task* task = container_of(node, Task, node);

            pthread_mutex_lock(&task->mutex);
            task->foo(task->data);
            task->done = true;
            pthread_cond_broadcast(&task->cond);
            pthread_mutex_unlock(&task->mutex);
        }
    }
    return NULL;
}

void thpool_init(ThreadPool* pool, size_t thrd_cnt)
{
    wsqueue_init(&pool->tasks);
    pool->count = thrd_cnt;
    pool->threads = malloc(sizeof(pthread_t) * thrd_cnt);
    pool->cont = true;

    for (size_t i = 0; i < thrd_cnt; i++)
        pthread_create(pool->threads + i, NULL, worker, pool);
}

void thpool_submit(ThreadPool* pool, Task* task)
{
    wsqueue_push(&pool->tasks, &task->node);
}

void thpool_wait(Task* task)
{
    task_wait(task);
    for (size_t i = 0; i < task->count; i++)
        thpool_wait(task->tasks[i]);
    task_finit(task);
    free(container_of(task, SData, task));
}

void thpool_finit(ThreadPool* pool)
{
    pthread_mutex_lock(&pool->tasks.squeue.mutex);
    pool->cont = false;
    pthread_mutex_unlock(&pool->tasks.squeue.mutex);

    size_t thrd_cnt = pool->count;
    wsqueue_notify_all(&pool->tasks);
    for (size_t i = 0; i < thrd_cnt; i++)
        pthread_join(pool->threads[i], NULL);
    wsqueue_finit(&pool->tasks);
    free(pool->threads);
}
