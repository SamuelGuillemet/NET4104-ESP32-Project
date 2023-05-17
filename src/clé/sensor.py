import sys

sys.path.append("")

from micropython import const
# from Crypto.Cipher import AES

import uasyncio as asyncio
import aioble
import bluetooth

import random 
import struct

_ENV_LOCK_UUID = bluetooth.UUID(0x1234)
_ENV_LOCK_CHAR_UUID = bluetooth.UUID(0x5678)

_ADV_APPEARANCE = const(576) # Generic keyring

_ENV_KEY_UUID = bluetooth.UUID(0x5678)
_ENV_KEY_CHAR_UUID = bluetooth.UUID(0x9012)

# # org.bluetooth.service.environmental_sensing
# _ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# # org.bluetooth.characteristic.temperature
# _ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
# # org.bluetooth.characteristic.gap.appearance.xml

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000


# Register GATT server.
# lock_service = aioble.Service(_ENV_LOCK_UUID)
# lock_characteristic = aioble.Characteristic(
#     lock_service, _ENV_LOCK_CHAR_UUID, read=True, notify=True
# )
# aioble.register_services(lock_service)
key_service = aioble.Service(_ENV_KEY_UUID)
key_characteristic = aioble.Characteristic(
    key_service, _ENV_KEY_CHAR_UUID, read=True, notify=True
)
aioble.register_services(key_service)


# Helper to encode the temperature characteristic encoding (sint16, hundredths of a degree).
def _encode_data(data):
    return struct.pack("<H", data)


# # This would be periodically polling a hardware sensor.
# async def sensor_task():
#     t = 24.5
#     while True:
#         lock_characteristic.write(_encode_temperature(t))
#         t += random.uniform(-0.5, 0.5)
#         await asyncio.sleep_ms(1000)


# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="key",
            services=[_ENV_KEY_CHAR_UUID],
            appearance=_ADV_APPEARANCE,
        ) as connection:
            print("Connection from", connection.device)
            #Print data
            print(connection.read(_ENV_LOCK_CHAR_UUID))
            await connection.disconnected()


# Run both tasks.
async def main():
    #t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t2)


asyncio.run(main())