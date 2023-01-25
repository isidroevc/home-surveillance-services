import asyncio
import random

async def do_something(i :int):
    await asyncio.sleep(random.randint(1, 3))
    return i
futures = []
for i in range(3):
    futures.append(do_something(i))

async def main():
    results = await asyncio.gather(*futures)
    print(results)


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")


