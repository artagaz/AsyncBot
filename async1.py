import asyncio


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(0.1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")


async def main():
    tasks = [
        asyncio.create_task(factorial("A", 15)),
        asyncio.create_task(factorial("B", 7)),
        asyncio.create_task(factorial("C", 4))
    ]

    # Ждем завершения всех задач
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())