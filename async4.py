import asyncio


async def fertilize(plant):
    print(f"7 Application of fertilizers for {plant}")
    await asyncio.sleep(3 / 1000)
    print(f"7 Fertilizers for the {plant} have been introduced")


async def treat_pests(plant):
    print(f"8 Treatment of {plant} from pests")
    await asyncio.sleep(5 / 1000)
    print(f"8 The {plant} is treated from pests")


async def process_plant(plant, soak_time, grow_time, acclimation_time):
    print(f"0 Beginning of sowing the {plant} plant")
    print(f"1 Soaking of the {plant} started")

    fert_task = asyncio.create_task(fertilize(plant))
    pest_task = asyncio.create_task(treat_pests(plant))

    await asyncio.sleep(soak_time / 1000)
    print(f"2 Soaking of the {plant} is finished")

    print(f"3 Shelter of the {plant} is supplied")
    await asyncio.sleep(grow_time / 1000)
    print(f"4 Shelter of the {plant} is removed")

    print(f"5 The {plant} has been transplanted")
    await asyncio.sleep(acclimation_time / 1000)
    print(f"6 The {plant} has taken root")

    await fert_task
    await pest_task

    print(f"9 The seedlings of the {plant} are ready")


async def sowing(*plants):
    tasks = [process_plant(*plant) for plant in plants]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    data = [('carrot', 7, 18, 2), ('cabbage', 2, 6, 10), ('onion', 5, 12, 7)]
    asyncio.run(sowing(*data))
