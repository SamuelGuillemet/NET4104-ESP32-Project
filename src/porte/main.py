import sys

sys.path.append("")

import uasyncio as asyncio
import aioble
import bluetooth
import hashlib

from machine import Pin, PWM

import time
import random
import struct


#######################################################################
#                               WHITELIST                             #
#######################################################################
# Whitelist of authorized keys
whitelist = [
    "7c:df:a1:e8:8c:aa",
]

#######################################################################
#                               PASSWORD                              #
#######################################################################
# Key value
password = 1234

#######################################################################
#                               DOOR                                  #
#######################################################################

# init servo
sg90 = PWM(Pin(37, mode=Pin.OUT))
sg90.freq(50)

# init UUID
UUID_DOOR = bluetooth.UUID(0x181A)
UUID_KEY = bluetooth.UUID(0x181B)

CHAR_DOOR_UUID = bluetooth.UUID(0x2A6E)
CHAR_KEY_HASH_UUID = bluetooth.UUID(0x1234)
CHAR_KEY_NOUCE_UUID = bluetooth.UUID(0x5678)

# Register GATT server.
door_service = aioble.Service(UUID_DOOR)
door_characteristic = aioble.Characteristic(
    door_service, CHAR_DOOR_UUID, read=True, notify=True, write=True, capture=True
)
aioble.register_services(door_service)


# The chalenge to verify the key
async def challenge(device):
    print(" --- Starting challenge --- ")

    # connect to the key
    try:
        connection = await device.connect()
    except asyncio.TimeoutError:
        print("Timeout during connection")
        return False

    # generate door_nonce
    door_nonce = random.randint(0, 10000000)
    print(" --- Generated door nonce : ", door_nonce, "--- ")
    # write door_nonce to client
    data = struct.pack("<l", door_nonce)
    door_characteristic.write(data)

    async with connection:
        key_service = await connection.service(UUID_KEY)
        key_chara_hash = await key_service.characteristic(CHAR_KEY_HASH_UUID)
        key_chara_nonce = await key_service.characteristic(CHAR_KEY_NOUCE_UUID)
        
        print(" --- Waiting for response --- ")
        await door_characteristic.written()
        
        key_hash = await key_chara_hash.read()
        print(" --- Got hash response : ", key_hash, "--- ")

        read = await key_chara_nonce.read()
        client_nonce = struct.unpack("<l", read)[0]
        print(" --- Got client nonce : ", client_nonce, "--- ")

        my_hash = hashlib.sha1(str(door_nonce) + str(password) + str(client_nonce)).digest()
        print(" --- Generated hash : ", my_hash, "--- ")
        if (my_hash == key_hash):
            print(" --- Challenge successful --- ")
            return True
        else:
            print(" --- Challenge failed --- ")
            return False

# Generate the list of devices to scan
def generate_key_devices_addr():
    key_devices = []
    for mac in whitelist:
        key_devices.append(aioble.device.Device(0, mac).addr)
        
    return key_devices

key_devices_addr = generate_key_devices_addr()


async def scan_device():
    async with aioble.scan(1000, interval_us=30000, window_us=30000, active=True) as scanner:
        reacheable = False
        async for result in scanner:
            if result.device.addr in key_devices_addr:
                reacheable = True
                print("Rssi of {} : {}".format(result.device.addr_hex(), result.rssi))
                if result.rssi > -10:
                    print(" --- Device " + result.device.addr_hex() + " is in range --- ")
                    res = await challenge(result.device)

                    if res:
                        print(" --- Door Unlocked --- ")
                        # open the door (moove the servo)
                        sg90.duty(26)
                        time.sleep(10)
                        # close the door (moove the servo)
                        sg90.duty(123)
                        time.sleep(1)
                        asyncio.sleep(2)
                        print(" --- Door Locked --- ")
                    return None
        if not reacheable:
            print("Waiting for device to be reachable...")
    return None

while True:
    asyncio.run(scan_device())
