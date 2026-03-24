# asyncio

## What and why

`asyncio` provides **single-threaded concurrency** in Python. Not parallelism (that's `multiprocessing`), but the ability to do something else while waiting for a response (network, file, sleep, etc).

**Without** asyncio — we just wait:

```python
import time

def fetch(url):
    time.sleep(1)  # simulates a network call
    return f"done: {url}"

results = [fetch(u) for u in ["url1", "url2", "url3"]]
# ⏱ ~3 seconds
```

**With** asyncio — everything runs concurrently:

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)  # simulates a network call
    return f"done: {url}"

async def main():
    results = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3"),
    )
    print(results)

asyncio.run(main())
# ⏱ ~1 second
```

!!! tip "When to use asyncio"
    **I/O-bound** (network, files, DB) → asyncio is made for this.
    **CPU-bound** (heavy computation) → use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`.

## The basics

### `async def` and `await`

`async def` declares a **coroutine**. Calling a coroutine doesn't execute it — it returns a coroutine object. You need `await` to run it:

```python
async def greet():
    return "hello"

# ❌ coro = greet()    → returns a coroutine object, does nothing
# ✅ result = await greet()  → executes and returns "hello"
```

`await` can only be used inside an `async def` function. It's the point where Python can "pause" this coroutine and run another one.

### `asyncio.run()`

The entry point for running async code from synchronous code:

```python
import asyncio

async def main():
    print("hello")

asyncio.run(main())
```

!!! warning "One event loop only"
    `asyncio.run()` creates an event loop, runs the coroutine, then closes the loop.
    Don't call `asyncio.run()` from already-async code — use `await` directly.

## Concurrent execution

### `asyncio.gather()` — run multiple coroutines concurrently

```python
async def fetch_user(user_id):
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"user_{user_id}"}

async def main():
    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
    # users = [{"id": 1, ...}, {"id": 2, ...}, {"id": 3, ...}]
```

Results are returned **in argument order**, even if coroutines finish in a different order.

### `asyncio.create_task()` — run in the background

```python
async def background_job():
    await asyncio.sleep(2)
    print("background done")

async def main():
    task = asyncio.create_task(background_job())
    # do other work while background_job runs
    print("doing other work...")
    await asyncio.sleep(1)
    print("still working...")
    await task  # wait for the task to finish
```

### `asyncio.TaskGroup` — gather with error handling (Python 3.11+)

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_user(1))
        task2 = tg.create_task(fetch_user(2))
        task3 = tg.create_task(fetch_user(3))
    # all tasks are done here
    print(task1.result(), task2.result(), task3.result())
```

!!! tip "`TaskGroup` vs `gather`"
    `TaskGroup` is safer: if one task raises an exception, the others are automatically cancelled. With `gather`, by default the others keep running.

## Common patterns

### Concurrent HTTP with `aiohttp`

```shell
$ pip install aiohttp
```

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            fetch(session, "https://api.example.com/users/1"),
            fetch(session, "https://api.example.com/users/2"),
            fetch(session, "https://api.example.com/users/3"),
        )
        print(results)

asyncio.run(main())
```

!!! warning "`requests` is not async"
    `requests.get()` is blocking — it blocks the entire event loop. Use `aiohttp` or `httpx.AsyncClient` for async HTTP.

### Limit concurrency with a `Semaphore`

If you fire 500 HTTP calls with `gather`, you'll overwhelm the server. A `Semaphore` limits concurrent tasks:

```python
async def fetch_limited(sem, session, url):
    async with sem:  # max N tasks at the same time
        async with session.get(url) as response:
            return await response.json()

async def main():
    sem = asyncio.Semaphore(10)  # max 10 concurrent requests
    async with aiohttp.ClientSession() as session:
        urls = [f"https://api.example.com/items/{i}" for i in range(500)]
        tasks = [fetch_limited(sem, session, url) for url in urls]
        results = await asyncio.gather(*tasks)

asyncio.run(main())
```

### Timeout

```python
async def slow_operation():
    await asyncio.sleep(10)
    return "done"

async def main():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=3.0)
    except asyncio.TimeoutError:
        print("timed out!")

asyncio.run(main())
```

### Iterate as results arrive with `as_completed`

Unlike `gather` which waits for everything, `as_completed` yields results as they come in:

```python
async def fetch(url, delay):
    await asyncio.sleep(delay)
    return f"{url} done"

async def main():
    coros = [fetch("fast", 0.5), fetch("slow", 2), fetch("medium", 1)]
    for coro in asyncio.as_completed(coros):
        result = await coro
        print(result)
        # "fast done"    (after 0.5s)
        # "medium done"  (after 1s)
        # "slow done"    (after 2s)

asyncio.run(main())
```

## Common pitfalls

### Forgetting `await`

```python
# ❌ Does nothing (no error, just a warning)
async def main():
    fetch("url1")  # coroutine created but never executed

# ✅
async def main():
    await fetch("url1")
```

### Calling blocking code in a coroutine

```python
import time

# ❌ Blocks the entire event loop
async def bad():
    time.sleep(5)  # nothing else can run for 5s

# ✅ Use run_in_executor for blocking code that can't be made async
async def good():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, time.sleep, 5)
```

### `asyncio.run()` inside already-async code

```python
# ❌ RuntimeError: cannot run nested event loops
async def handler():
    asyncio.run(some_coroutine())

# ✅
async def handler():
    await some_coroutine()
```
