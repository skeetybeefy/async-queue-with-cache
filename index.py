import asyncio
from cache import cache
from async_queue import queue, counter, timeout, threshold

def add(*args, **kwargs):
  sum = 0
  for arg in args:
    sum += arg
  for key, value in kwargs.items():
    print(f"key: {key}, value: {value}")
  print(sum)
  return sum

DELAY_BEFORE_DELETE = 10

def delete_from_cache(item):
  cache.remove(item)

async def put_in_queue_with_cache(item):
  if item not in cache:
    cache.append(item)
    await queue.put(item)
    loop.call_later(DELAY_BEFORE_DELETE, delete_from_cache, item)
  else:
    print("Item in cache!!!")
    print(cache)


async def consumer(id, queue):
  global counter, threshold, timeout
  while True:
    if counter > threshold:
      await asyncio.sleep(timeout)
      counter = 0
    print(f"Consumer {id} trying to get from queue")
    item = await queue.get()
    if item is None:
      break
    else:
      (f, *args, kwargs) = item
      f(*args, **kwargs)
      counter += 1
    print(f"Consumer {id} consumed {item}")

async def producer(queue):
  while True:
    await asyncio.sleep(1)
    print("Putting new item onto the queue")
    # await queue.put([add, 2, 3, 5, {"test": 1}])
    await put_in_queue_with_cache([add, 2, 3, 5, {"test": 1}])


async def main():
  await asyncio.wait([
    producer(queue), 
    consumer(1, queue), 
    # consumer(2, queue)
  ])

loop = asyncio.new_event_loop()
loop.run_until_complete(main())



