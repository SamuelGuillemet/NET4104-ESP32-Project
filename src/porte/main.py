import struct
import random
import bluetooth
import aioble
import uasyncio as asyncio
from micropython import const

import sys

sys.path.append("")

_ENV_CHALL_UUID = bluetooth.UUID(0x181A)

server = aioble.device.Device(0, "7c:df:a1:e8:8c:aa")


async def challenge(device):
    print(" --- Starting challenge --- ")
    try:
        print("Connecting to", device)
        connection = await device.connect()
    except asyncio.TimeoutError:
        print("Timeout during connection")
        return False

    async with connection:
        # read challenge values from server
        return
    # Compare values and return True if correct

    return True


async def scan_device():
    # print("scaning...")
    async with aioble.scan(1000, interval_us=30000, window_us=30000, active=True) as scanner:
        rechable = False
        async for result in scanner:
            target = b'7c:df:a1:e8:8c:aa'
            if result.device.addr == server.addr:
                print("rssi: {}".format(result.rssi))
                rechable = True
                if result.rssi > -11:
                    print("Device in place")
                    print("initiating challenge")
                    res = challenge(result.device)
                    if res:
                        print("challenge successful")
                        print("Door Unlocked")
                        await asyncio.sleep(10)
                        print("Door Locked")
                        return None
                    else:
                        print("challenge failed")
                        return None
        if not rechable:
            print("Too Far")
            return None

    return None

while True:
    asyncio.run(scan_device())
