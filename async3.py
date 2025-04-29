import asyncio
import time


async def handle_interview(canditate):
    name, prep_time_1, defend_time_1, prep_time_2, defend_time_2 = canditate

    print(f"{name} started the 1 task.")
    await asyncio.sleep(prep_time_1 / 100)
    print(f"{name} moved on to the defense of the 1 task.")
    await asyncio.sleep(defend_time_1 / 100)
    print(f"{name} completed the 1 task.")

    print(f"{name} is resting.")
    await asyncio.sleep(5/100)

    print(f"{name} started the 2 task.")
    await asyncio.sleep(prep_time_2 / 100)
    print(f"{name} moved on to the defense of the 2 task.")
    await asyncio.sleep(defend_time_2 / 100)
    print(f"{name} completed the 2 task.")


async def interviews(*candidates):
    tasks = [handle_interview(candidate) for candidate in candidates]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    data = [('Ivan', 5, 2, 7, 2), ('John', 3, 4, 5, 1), ('Sophia', 4, 2, 5, 1)]
    t0 = time.time()
    asyncio.run(interviews(*data))
    print(time.time()-t0)