import struct
import random
import bluetooth
import aioble
import uasyncio as asyncio
from micropython import const
import hashlib
from machine import Pin, PWM
import time

import sys

sys.path.append("")

# init servo
sg90 = PWM(Pin(37, mode=Pin.OUT))
sg90.freq(50)


UUID = bluetooth.UUID(0x181A)
_ENV_CHALL_DOOR_UUID = bluetooth.UUID(0x2A6E)
KEY_UUID = bluetooth.UUID(0x181B)
_ENV_CHALL_KEY_UUID = bluetooth.UUID(0x1234)

# Create key device object to compare mac adress
key_device = aioble.device.Device(0, "7c:df:a1:e8:8c:aa")

key = "1234"

# Register GATT server.
door_service = aioble.Service(UUID)
door_characteristic = aioble.Characteristic(
    door_service, _ENV_CHALL_DOOR_UUID, read=True, notify=True
)
aioble.register_services(door_service)


async def challenge(device):
    print(" --- Starting challenge --- ")

    # connect to the key
    try:
        print("Connecting to", device)
        connection = await device.connect()
    except asyncio.TimeoutError:
        print("Timeout during connection")
        return False

    # generate nonce1
    nonce1 = random.randint(0, 10000000)
    print("nonce1: {}".format(nonce1))
    # write nonce1 to server
    data = struct.pack("<l", nonce1)
    door_characteristic.write(data)
    # waiting the key to catch the nonce1
    await asyncio.sleep(2)

    async with connection:
        # wait for response
        # await asyncio.sleep(1)
        # read response from key at _ENV_CHALL_KEY_UUID
        key_service = await connection.service(KEY_UUID)
        key_chara = await key_service.characteristic(_ENV_CHALL_KEY_UUID)
        res = await key_chara.read()
        # check if response is correct
        #hash = struct.unpack("<l", res)[0]
        hash = res
        print("hash: {}".format(hash))

        asyncio.sleep(2)

        res = await key_chara.read()
        nonce2 = struct.unpack("<l", res)[0]
        print("nonce2: {}".format(nonce2))

        my_hash = hashlib.sha1(str(nonce1) + key + str(nonce2)).digest()
        print("my_hash: {}".format(my_hash))
        if (my_hash == hash):
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
            if result.device.addr == key_device.addr:
                print("rssi: {}".format(result.rssi))
                rechable = True
                if result.rssi > -10:
                    print("Device in place")
                    print("initiating challenge")
                    res = await challenge(result.device)

                    if res:
                        print("Door Unlocked")
                        # open the door (moove the servo)
                        sg90.duty(26)
                        time.sleep(10)
                        # close the door (moove the servo)
                        sg90.duty(123)
                        time.sleep(1)
                        await asyncio.sleep(10)
                        print("Door Locked")
                    return None
        if not rechable:
            print("Waiting for device to be reachable...")
            # exemple hash
            # hash = hashlib.sha1("password")
            # print(hash.digest())
            # exemple open door
            # sg90.duty(26)
            # time.sleep(100)
            # sg90.duty(123)
            # time.sleep(1)
            return None

    return None

while True:
    asyncio.run(scan_device())
