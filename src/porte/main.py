import struct
import random
import bluetooth
import aioble
import uasyncio as asyncio
from micropython import const

import sys

sys.path.append("")

UUID = bluetooth.UUID(0x181A)
_ENV_CHALL_DOOR_UUID = bluetooth.UUID(0x2A6E)
_ENV_CHALL_KEY_UUID = bluetooth.UUID(0x1234)

server = aioble.device.Device(0, "7c:df:a1:e8:8c:aa")

key = 1234

# Register GATT server.
door_service = aioble.Service(UUID)
door_characteristic = aioble.Characteristic(
    door_service, _ENV_CHALL_DOOR_UUID, read=True, notify=True
)
aioble.register_services(door_service)


async def challenge(device):
    print(" --- Starting challenge --- ")
    try:
        print("Connecting to", device)
        connection = await device.connect()
    except asyncio.TimeoutError:
        print("Timeout during connection")
        return False

    # generate a nonce
    nonce1 = random.randint(0, 10000000)
    print("nonce1: {}".format(nonce1))
    # write nonce to server
    await door_characteristic.write(struct.pack("<h", nonce1))

    async with connection:
        # wait for response
        await asyncio.sleep(1)
        # read response from key at _ENV_CHALL_KEY_UUID
        res = await connection.read(_ENV_CHALL_KEY_UUID)
        # check if response is correct
        hash = res[0:12]
        nonce2 = res[12:14]
        print("hash: {}".format(hash))
        print("nonce2: {}".format(nonce2))
        if (hash(nonce1 + key + nonce2) == hash):
            print(" --- Challenge successful --- ")
            return True
        else:
            print(" --- Challenge failed --- ")
            return False


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
                    res = await challenge(result.device)
                    if res:
                        print("Door Unlocked")
                        await asyncio.sleep(10)
                        print("Door Locked")
                    return None
        if not rechable:
            print("Too Far")
            return None

    return None

while True:
    asyncio.run(scan_device())
