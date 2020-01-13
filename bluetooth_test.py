import asyncio
import datetime
import random
import bluetooth

sleep_time = 1


async def server(num, loop):
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        await asyncio.sleep(sleep_time)

async def client(num, loop):
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        await asyncio.sleep(sleep_time)



def main():
    loop = asyncio.get_event_loop()
    loop.create_task(server(1, loop))
    loop.create_task(client(2, loop))
    loop.run_forever()

main()