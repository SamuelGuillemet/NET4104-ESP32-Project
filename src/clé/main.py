import sys

sys.path.append("")

import uasyncio as asyncio
import aioble
import bluetooth
import hashlib

import random 
import struct


#######################################################################
#                               PASSWORD                              #
#######################################################################
# Key value
password = 1234

#######################################################################
#                               KEY                                   #
#######################################################################

#init UUID
UUID_KEY = bluetooth.UUID(0x181B)
UUID_DOOR = bluetooth.UUID(0x181A)

CHAR_DOOR_UUID = bluetooth.UUID(0x2A6E)
CHAR_KEY_HASH_UUID = bluetooth.UUID(0x1234)
CHAR_KEY_NOUCE_UUID = bluetooth.UUID(0x5678)

# Register GATT server.
key_service = aioble.Service(UUID_KEY)
key_characteristic_hash = aioble.BufferedCharacteristic(
    key_service, CHAR_KEY_HASH_UUID
)
key_characteristic_nonce = aioble.Characteristic(
    key_service, CHAR_KEY_NOUCE_UUID, read=True, notify=True
)
aioble.register_services(key_service)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

async def advertise():
    print(" --- Starting advertising --- ")
    while True:
        # Advertise our service and appearance.
        result = await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="Key",
            services=[UUID_KEY]
        ) 
        
        if result:
            print(" --- Advertising successful --- ")                        
                        
            door_service = await result.service(UUID_DOOR)
            print(" --- Got door service : ", door_service, "--- ")
            door_characteristic = await door_service.characteristic(CHAR_DOOR_UUID)
            print(" --- Got door characteristic : ", door_characteristic, "--- ")
            
            if door_characteristic is not None:
                print(" --- Reading to door characteristic with UUID:", door_characteristic.uuid, "--- ")
                val = await door_characteristic.read()
                if len(val) == 1:
                    val += b'\x00'
                nounce_door = struct.unpack("<l", val)[0]
                print(" --- Get nouce from door characteristic : ", nounce_door, "--- ")
                
                nounce_cle = random.randint(0, 100000000)
                print(" --- Writing to key characteristic hash with UUID:", key_characteristic_hash.uuid, "--- ")
                string_to_hash = str(nounce_door) + str(password) + str(nounce_cle)
                digest = hashlib.sha1(string_to_hash.encode()).digest()
                print(" --- Writing data:", digest, "--- ")
                key_characteristic_hash.write(digest)
                
                print(" --- Writing to key characteristic nounce with UUID:", key_characteristic_nonce.uuid, "--- ")
                val_nounce = struct.pack("<l", nounce_cle)
                print(" --- Writing data:", nounce_cle, "--- ")
                key_characteristic_nonce.write(val_nounce)
                
                print(" --- Notifying characteristic --- ")
                await door_characteristic.write(b'\x00\x00\x00\x00')

            print(" --- Sleeping --- ")
                    
async def main():
    await asyncio.create_task(advertise())
    
asyncio.run(main())